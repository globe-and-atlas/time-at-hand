#!/usr/bin/env python3
"""Verify native status overlay avoids the date bands."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'watchface/src/c/watchface.c').read_text()
assert 'int status_top=(date_mask && date_position==1);' in source
assert 'battery_text_y=status_top ? 20 : 205' in source
assert 'battery_bar_y=status_top ? 27 : 213' in source
assert 'bluetooth_y=status_top ? 20 : 204' in source
# Date bands from face.c: top 4..17, bottom 210..223. Status top band starts below
# top date; status bottom band is only used when bottom date is not visible.
for y,h in [(20,18),(27,6)]:
    assert y > 17, (y,h,'top status collides with top date')
for y,h in [(205,18),(213,6),(204,18)]:
    assert y < 224, (y,h,'sanity')
report={'status':'pass','bottom_date_status':'top safe band','top_status_rows':[20,37],'bottom_status_rows':[204,222]}
(ROOT/'.tmp/status-layout-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
