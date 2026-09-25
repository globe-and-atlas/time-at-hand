#!/usr/bin/env python3
"""Validate manifest and embedded native identity for all five editions."""
import json
import hashlib
import os
from pathlib import Path
from zipfile import ZipFile
from urllib.request import urlopen
from libpebble2.util.bundle import PebbleBundle
from libpebble2.util.hardware import PebbleHardware
ROOT=Path(__file__).resolve().parents[1]
PORT=int(os.environ.get('TAH_PREVIEW_PORT','4286'))
for name, filename in (('origin','origin.pbw'),('vector','vector.pbw'),('meridian','meridian.pbw'),('cardinal','cardinal.pbw'),('clarity','clarity.pbw')):
    path=ROOT/'dist'/filename
    with ZipFile(path) as z:
        info=json.loads(z.read('appinfo.json'))
    bundle=PebbleBundle(str(path),hardware=PebbleHardware.OBELIX_PVT)
    metadata=bundle.get_app_metadata()
    assert 0 < len(metadata['app_name']) <= 10, 'Watchface display names must fit ten characters'
    print(name,info['uuid'],metadata)
    assert info['uuid'].lower()==str(metadata['uuid'])
    assert 'configurable' in info['capabilities']
    route=filename
    with urlopen(f'http://127.0.0.1:{PORT}/'+route,timeout=5) as r:download=r.read()
    assert hashlib.sha256(download).digest()==hashlib.sha256(path.read_bytes()).digest()
    print('Preview download matches bundle:',route)
