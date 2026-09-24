---
generated_by: "Claude Code CLI (claude-opus-5-5)"
timestamp: "2026-09-24T11:30:00-05:00"
---
# Publish CloudPebble edition branches

1. Commit changes on `main` and push.
2. `python3 execution/build_editions.py`, so `dist/` matches main.
3. `python3 execution/publish_edition_branches.py` generates the `edition-*` worktrees under `.tmp/edition-branches/`. It builds each with `execution/cloudpebble.py` and compares it against `dist/`.
4. `python3 execution/publish_edition_branches.py --push` force-pushes (with lease) `edition-two-hands`, `edition-meridian`, `edition-four-points` and `edition-clear`.

Gotchas (from the CloudPebble source, coredevices/cloudpebble @ 08298a2):
- An empty branch in the import form becomes `master`. Always link `/ide/import/github/<owner>/<repo>/<branch>`.
- Only `.c`/`.h` (`src/c`) and `.js`/`.json` (`src/pkjs`) are imported, and anything else is silently dropped.
- Our `wscript` is replaced, so the edition must come from source (`edition.h`), not `-D` flags.
- Branch names avoid `/`, since they go into GitHub's archive-zip URL.
