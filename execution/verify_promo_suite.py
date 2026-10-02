#!/usr/bin/env python3
"""Check real-renderer provenance, format integrity, media timing and gallery links."""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import subprocess
import zipfile
from PIL import Image
from generate_promo_suite import OUT, ROOT, SPECS, face_image
from preview import load_renderer


def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    assert manifest['editions']==['origin','vector','meridian','cardinal']
    lib=load_renderer()
    for shot in manifest['screenshots']:
        path=OUT/shot['path']
        with Image.open(path) as im:
            assert im.size==(200,228),path
            expected=face_image(lib,SPECS[shot['edition']],**shot['config'])
            assert im.convert('RGB').tobytes()==expected.tobytes(),path
    assert len(manifest['screenshots'])==20
    counts={'png':0,'gif':0,'mp4':0}
    for record in manifest['files']:
        path=OUT/record['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],path
        ext=path.suffix[1:]
        if ext in counts: counts[ext]+=1
        if ext=='png':
            with Image.open(path) as im:
                expected_sizes={'banner-720x320.png':(720,320),'cover-1200x630.png':(1200,630),
                                'square-1080.png':(1080,1080),'portrait-1080x1350.png':(1080,1350),
                                'story-1080x1920.png':(1080,1920),'contact-sheet.png':(1600,1100),
                                'suite-cover-1600x900.png':(1600,900)}
                if path.name in expected_sizes: assert im.size==expected_sizes[path.name],path
                if path.name.startswith('thumbnail-'):
                    size=int(path.stem.split('-')[1]);assert im.size==(size,size),path
                im.verify()
        elif ext=='gif':
            with Image.open(path) as im:
                assert im.n_frames==48,(path,im.n_frames)
                assert im.info.get('loop')==0,path
                duration=0;hashes=set()
                for n in range(im.n_frames):
                    im.seek(n);duration+=im.info['duration'];hashes.add(hashlib.sha256(im.convert('RGB').tobytes()).hexdigest())
                    if path.name=='timelapse-200x228.gif':
                        assert im.size==(200,228),path
                        spec=next(s for s in SPECS if s['slug']==path.parent.parent.name)
                        minutes=600+n*(30 if spec['id']==2 else 15)
                        instant=datetime(2026,9,23,15,0,tzinfo=timezone.utc)+timedelta(minutes=n*30)
                        opts={'utc':instant.timestamp()} if spec['id']==2 else {}
                        expected=face_image(lib,spec,h=(minutes//60)%24,m=minutes%60,**opts)
                        assert im.convert('RGB').tobytes()==expected.tobytes(),(path,n)
                    else: assert im.size==(600,600),path
                assert duration==12000,(path,duration)
                assert len(hashes)>24,(path,len(hashes))
        elif ext=='mp4':
            metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
            stream=metadata['streams'][0]
            assert (stream['width'],stream['height'])==((1080,1920) if 'vertical' in path.name else (1080,1080)),path
            assert stream['pix_fmt']=='yuv420p',path
            assert abs(float(metadata['format']['duration'])-12)<.05,path
            assert stream['codec_name']=='h264',path
    assert counts==dict(png=58,gif=8,mp4=8),counts
    for link in re.findall(r'(?:href|src|poster)="([^"]+)"',(OUT/'index.html').read_text()):
        if not link.startswith('#'): assert (OUT/link).is_file(),link
    with zipfile.ZipFile(ROOT/'assets/pebble-promo-suite.zip') as archive:
        assert archive.testzip() is None
        for record in manifest['files']:
            assert hashlib.sha256(archive.read('promo-suite/'+record['path'])).hexdigest()==record['sha256']
    print(json.dumps(dict(result='PASS',renderer_identical_screenshots=20,media=counts,gallery_links='PASS',zip='PASS'),indent=2))


if __name__=='__main__':
    main()
