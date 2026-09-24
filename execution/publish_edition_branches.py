#!/usr/bin/env python3
"""Generate one CloudPebble-importable branch per non-Original edition from main.

Each edition-<slug> branch is main plus one generated commit that sets the edition's
manifest (uuid, display name, capabilities), phone settings and edition.h. The branches are
build artifacts: edit main, then re-run this script, which rewrites them.

Before anything is pushed, every branch is built with CloudPebble's import rules
(execution/cloudpebble.py) and compared with the locally built edition in dist/: identical
phone JS and manifest identity, and an identical app binary apart from its CRC, timestamp and
build ID. Run execution/build_editions.py first so dist/ matches main.

  python3 execution/publish_edition_branches.py          # generate and verify only
  python3 execution/publish_edition_branches.py --push   # then force-push the edition branches
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_editions import EDITIONS, ROOT, manifest_for  # noqa: E402
from cloudpebble import simulate  # noqa: E402
from generate_settings import configuration  # noqa: E402

WORK = ROOT / '.tmp/edition-branches'
IMPORT = 'https://cloudpebble.repebble.com/ide/import/github/globe-and-atlas/time-at-hand/{branch}'


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def branch_name(edition: int) -> str:
    return f"edition-{EDITIONS[edition]['slug']}"


def comparable_binary(data: bytes) -> bytes:
    """App binary with the fields that change on every build zeroed: CRC (bytes 20-23),
    resource timestamp (124-127) and the 20-byte GNU build ID."""
    blob = bytearray(data)
    blob[20:24] = bytes(4)
    blob[124:128] = bytes(4)
    note = blob.find(b'GNU\x00')
    if note < 0:
        raise ValueError('GNU build-id note not found')
    blob[note + 4:note + 24] = bytes(20)
    return bytes(blob)


def bundle(pbw: Path) -> tuple[bytes, bytes, dict]:
    with zipfile.ZipFile(pbw) as z:
        return z.read('emery/pebble-app.bin'), z.read('pebble-js-app.js'), json.loads(z.read('appinfo.json'))


def generate(edition: int, main_sha: str) -> Path:
    spec, branch = EDITIONS[edition], branch_name(edition)
    tree = WORK / spec['slug']
    if tree.exists():
        git('worktree', 'remove', '--force', str(tree))
    git('worktree', 'add', '--force', '-B', branch, str(tree), main_sha)
    watch = tree / 'watchface'
    original = (watch / 'package.json').read_text()
    (watch / 'package.json').write_text(manifest_for(edition, original))
    (watch / 'src/pkjs/config.json').write_text(json.dumps(configuration(edition), indent=2) + '\n')
    header = watch / 'src/c/edition.h'
    text = header.read_text()
    if '#define TAH_EDITION 0' not in text:
        raise ValueError('edition.h no longer has the expected default')
    header.write_text(text.replace('#define TAH_EDITION 0', f'#define TAH_EDITION {edition}'))
    readme = tree / 'README.md'
    banner = (f"> **Generated branch: {spec['name']} edition.** CloudPebble builds {spec['name']} from "
              f"`watchface/` ([import]({IMPORT.format(branch=branch)})). Don't edit here: change `main`, "
              f"then run `python3 execution/publish_edition_branches.py --push`. Generated from main {main_sha[:7]}.\n\n")
    readme.write_text(banner + readme.read_text())
    git('add', '-A', cwd=tree)
    git('commit', '-q', '-m', f"Edition: {spec['name']} (generated from main {main_sha[:7]})", cwd=tree)
    return tree


def verify(edition: int, tree: Path) -> dict:
    spec = EDITIONS[edition]
    pbw, dropped = simulate(tree / 'watchface', WORK / f"cloudpebble-{spec['slug']}")
    assert not dropped, (spec['slug'], dropped)
    built_bin, built_js, built_info = bundle(pbw)
    local_bin, local_js, local_info = bundle(ROOT / 'dist' / spec['pbw'])
    for key in ('uuid', 'displayName', 'capabilities'):
        assert built_info.get(key) == local_info.get(key), (spec['slug'], key, built_info.get(key), local_info.get(key))
    assert built_js == local_js, (spec['slug'], 'phone JS differs from dist')
    assert comparable_binary(built_bin) == comparable_binary(local_bin), (spec['slug'], 'app binary differs from dist')
    return {'branch': branch_name(edition), 'uuid': built_info['uuid'], 'name': built_info['displayName'],
            'import': IMPORT.format(branch=branch_name(edition))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--push', action='store_true', help='force-push the verified edition branches to origin')
    args = parser.parse_args()
    if git('status', '--porcelain', '--untracked-files=no'):
        sys.exit('Commit main first: branches are generated from a committed main.')
    if git('rev-parse', '--abbrev-ref', 'HEAD') != 'main':
        sys.exit('Run from main.')
    main_sha = git('rev-parse', 'HEAD')
    WORK.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        for edition in sorted(EDITIONS):
            tree = generate(edition, main_sha)
            results.append(verify(edition, tree))
            print(json.dumps(results[-1]), flush=True)
        if args.push:
            branches = [branch_name(e) for e in sorted(EDITIONS)]
            subprocess.run(['git', 'push', '--force-with-lease', 'origin', *branches], cwd=ROOT, check=True)
    finally:
        for edition in EDITIONS:
            tree = WORK / EDITIONS[edition]['slug']
            if tree.exists():
                git('worktree', 'remove', '--force', str(tree))
        git('worktree', 'prune')
    (ROOT / '.tmp/edition-branches.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
