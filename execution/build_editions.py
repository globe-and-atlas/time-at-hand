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
FOUR_POINTS_UUID='f05945f9-3cd9-462b-88e7-0fef77271d49'
CLEAR_UUID='9f13e2a2-8cce-4163-a5e0-0f5455679749'
# Single source of truth for editions: local builds here and CloudPebble branches
# (execution/publish_edition_branches.py). Origin (0) keeps the manifest as committed.
EDITIONS={
    1:{'slug':'two-hands','name':'Vector','uuid':SPLIT_UUID,'capabilities':None,'pbw':'time-at-hand-two-hands.pbw'},
    2:{'slug':'meridian','name':'Meridian','uuid':MERIDIAN_UUID,'capabilities':['configurable','location'],'pbw':'meridian-hemisphere.pbw'},
    3:{'slug':'four-points','name':'Cardinal','uuid':FOUR_POINTS_UUID,'capabilities':['configurable'],'pbw':'four-points.pbw'},
    4:{'slug':'clear','name':'Clarity','uuid':CLEAR_UUID,'capabilities':['configurable'],'pbw':'clear.pbw'},
}

def manifest_for(edition,original):
    """Manifest text for an edition, derived from the committed (Origin) manifest."""
    spec=EDITIONS[edition];data=json.loads(original)
    data['pebble']['uuid']=spec['uuid'];data['pebble']['displayName']=spec['name']
    if spec['capabilities'] is not None:data['pebble']['capabilities']=spec['capabilities']
    return json.dumps(data,indent=2)+'\n'

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
        # Build order matches the historical script (Meridian first, keeps its ELF for diagnosis).
        for edition in (2,1,3,4):
            manifest.write_text(manifest_for(edition,original))
            build(edition)
            if edition==2:(ROOT/'.tmp/meridian.elf').write_bytes((ROOT/'watchface/build/emery/pebble-app.elf').read_bytes())
            (ROOT/'dist'/EDITIONS[edition]['pbw']).write_bytes((ROOT/'watchface/build/watchface.pbw').read_bytes())
    finally:
        manifest.write_text(original)
        build(0)
        config.write_text(original_config)
    (ROOT/'dist/time-at-hand-original.pbw').write_bytes((ROOT/'watchface/build/watchface.pbw').read_bytes())
    print('Built five editions in dist/; restored default original build.')
if __name__=='__main__':build_editions()
