#!/usr/bin/env python3
"""Check AppMessage buffers cover the largest generated settings payload."""
import json
import re
from pathlib import Path
from generate_settings import configuration
ROOT=Path(__file__).resolve().parents[1]
keys=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['messageKeys']
key_index={name:i for i,name in enumerate(keys)}
# Pebble dictionary tuples include key/type/length overhead. Use a conservative
# estimate: 7 bytes overhead per tuple, integer values 4 bytes, booleans 1 byte,
# and strings at their configured max/default length plus terminator.
def item_size(item):
    t=item.get('type')
    if 'messageKey' not in item:return 0
    if t in ('toggle','checkbox'): return 7+1
    if t=='input':
        default=str(item.get('defaultValue',''))
        return 7+max(len(default)+1,16)
    return 7+4

def walk(items):
    total=0;names=[]
    for item in items:
        if 'items' in item:
            subtotal,subnames=walk(item['items']);total+=subtotal;names+=subnames
        else:
            total+=item_size(item)
            if 'messageKey' in item:names.append(item['messageKey'])
    return total,names
sizes=[]
for edition in range(5):
    size,names=walk(configuration(edition))
    assert all(name in key_index for name in names), (edition, sorted(set(names)-set(key_index)))
    sizes.append(size)
source=(ROOT/'watchface/src/c/watchface.c').read_text()
match=re.search(r'app_message_open\((\d+),(\d+)\)',source)
assert match, 'app_message_open not found'
inbox,outbox=map(int,match.groups())
assert max(sizes) < inbox, {'sizes':sizes,'inbox':inbox}
assert max(sizes) < outbox, {'sizes':sizes,'outbox':outbox}
assert 'MESSAGE_KEY_GlobeCustomColors' in source
assert 'globe_custom_colors ? globe_colors[0] : 0' in source
assert 'globe_custom_colors ? globe_colors[1] : 7' in source
report={'status':'pass','estimated_payload_bytes_by_edition':sizes,'app_message_open':[inbox,outbox],'largest':'Meridian','globe_custom_color_toggle':'pass'}
(ROOT/'.tmp/message-buffer-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
