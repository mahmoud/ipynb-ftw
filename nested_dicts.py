# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import json

with open('/home/ipy/notebooks/weirdnesteddicts.json') as di:
    stuff = json.load(di)

revisions = stuff['revisions']

print revisions.keys()[0]
print revisions.values()[0]

# <codecell>

from collections import defaultdict

mega_dict = defaultdict(lambda: defaultdict(list))

for rev_date, sec_data in revisions.items():
    for section, data in sec_data.items():
        mega_dict[rev_date][section].append(data)
    
print mega_dict.values()[0]

