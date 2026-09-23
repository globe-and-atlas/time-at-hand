#!/usr/bin/env python3
"""Build independently installable editions, restoring the original manifest."""
import json
import os
from pathlib import Path
import subprocess
from generate_settings import configuration
ROOT=Path(__file__).resolve().parents[1]
SPLIT_UUID='a12bd695-9b47-4a44-b416-43006dc54b9f'
MERIDIAN_UUID='bf118b38-aaf3-438d-8c91-0e92c4f757e3'

def build_editions():
    manifest=ROOT/'watchface/package.json';original=manifest.read_text()
    config=ROOT/'watchface/src/pkjs/config.json';original_config=config.read_text()
    env=os.environ.copy();env.pop('TAH_TEST_MINUTE',None);env.pop('TAH_EDITION',None)
    (ROOT/'dist').mkdir(exist_ok=True)
    def build(edition):
        config.write_text(json.dumps(configuration(edition),indent=2)+'\n')
        subprocess.run(['pebble','clean'],cwd=ROOT/'watchface',env=env,check=True,capture_output=True)
        result=subprocess.run(['pebble','build'],cwd=ROOT/'watchface',env={**env,'TAH_EDITION':str(edition)},capture_output=True,text=True)
        (ROOT/'.tmp'/f'build-edition-{edition}.log').write_text(result.stdout+result.stderr)
        result.check_returncode()
    try:
        globe=json.loads(original);globe['pebble']['uuid']=MERIDIAN_UUID
        globe['pebble']['displayName']='G&A Meridian'
        globe['pebble']['capabilities']=['configurable','location']
        manifest.write_text(json.dumps(globe,indent=2)+'\n')
        build(2)
        (ROOT/'.tmp/meridian.elf').write_bytes((ROOT/'watchface/build/emery/pebble-app.elf').read_bytes())
        (ROOT/'dist/meridian-hemisphere.pbw').write_bytes((ROOT/'watchface/build/watchface.pbw').read_bytes())
        split=json.loads(original);split['pebble']['uuid']=SPLIT_UUID
        split['pebble']['displayName']='Time as Hand: Two Hands'
        manifest.write_text(json.dumps(split,indent=2)+'\n')
        build(1)
        (ROOT/'dist/time-as-hand-two-hands.pbw').write_bytes((ROOT/'watchface/build/watchface.pbw').read_bytes())
    finally:
        manifest.write_text(original)
        build(0)
        config.write_text(original_config)
    (ROOT/'dist/time-as-hand-original.pbw').write_bytes((ROOT/'watchface/build/watchface.pbw').read_bytes())
    print('Built three editions in dist/; restored default original build.')
if __name__=='__main__':build_editions()
