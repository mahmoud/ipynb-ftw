# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

import requests
from collections import Counter

# <codecell>

r = requests.get('http://tools.wmflabs.org/hashtags/get/freebassel/en/10')

# <codecell>

import pprint
pprint.pprint(r.json[0])

# <codecell>

stats = {
    'top users': Counter([edit['rc_user_text'] for edit in r.json if edit['rc_namespace'] == 0]),
    'user count': len(set([edit['rc_user_text'] for edit in r.json if edit['rc_namespace'] == 0])),
    'top articles': Counter([edit['rc_title'] for edit in r.json if edit['rc_namespace'] == 0]),
    'article count': len(set([edit['rc_title'] for edit in r.json])),
    'bytes': sum([(edit['rc_new_len'] - edit['rc_old_len']) for edit in r.json if edit['rc_new_len'] > edit['rc_old_len']]),
    'total edits': len(r.json)
}

pprint.pprint(stats)

