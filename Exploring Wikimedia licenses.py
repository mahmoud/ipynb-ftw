# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

import urllib2
import json
from pprint import pprint

# <codecell>

licenses_req = urllib2.urlopen('http://gist.githubusercontent.com/slaporte/3192231ee787409fbec7/raw/8c061c2de6b472186ef5f74f42284daf8b77cfb1/all_licenses.json')
licenses = json.load(licenses_req)

# <codecell>

license_totals = sorted([(l, sum(t.values())) for l, t in licenses.items()], key=lambda l: l[1], reverse=True)
total_files = 26674464.0
licenses_percent = [(l[0], l[1]/total_files * 100) for l in license_totals]
licenses_percent[:100]

# <codecell>

len([l for l in license_totals if 'pd' in l[0].lower()])

