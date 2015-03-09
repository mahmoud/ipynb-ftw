# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

import requests
from collections import Counter

# <codecell>

r = requests.get('http://tools.wmflabs.org/hashtags/get/artandfeminism/en/3')

# <codecell>

import pprint
pprint.pprint(r.json[0])

# <codecell>

new = len([edit for edit in r.json if edit['rc_old_len'] == 0])
users = len(set([edit['rc_user_text'] for edit in r.json]))
user_count = Counter([edit['rc_user_text'] for edit in r.json])
print user_count
bytes = sum([(edit['rc_new_len'] - edit['rc_old_len']) for edit in r.json if edit['rc_new_len'] > edit['rc_old_len']])
print 'total edits: %s' % len(r.json)
print 'users: %s' % users
print 'new articles: %s' % new
print 'bytes: %s' % bytes

