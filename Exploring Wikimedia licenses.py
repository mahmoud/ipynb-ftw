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
print len([l[0] for l in license_totals])
total_files = 26674464.0
licenses_percent = [(l[0], l[1]/total_files * 100) for l in license_totals]
licenses_percent[:100]

# <codecell>

def print_license_stats(name, pattern):
    total_licenses = len([l for l in license_totals if pattern in l[0].lower()])
    total_licensed_files = sum([l[1] for l in license_totals if pattern in l[0].lower()])
    percent_total = total_licensed_files/total_files * 100
    print '%s: %s licenses, %s files (%s of Commons)' % (name,
                                                          total_licenses,
                                                          total_licensed_files, 
                                                          percent_total)
print_license_stats('Public Domain', 'pd-')
print_license_stats('Creative Commons', 'cc-')
print_license_stats('GNU Free Document License', 'gfdl')
print_license_stats('No known restrictions', 'no_known')

# <codecell>

len([(l[0], l[1]) for l in license_totals if l[1] > 100000])

# <codecell>

[(l[0], l[1], l[1]/total_files * 100) for l in license_totals if 'pd-' not in l[0].lower() and 'cc-' not in l[0].lower() and 'gfdl' not in l[0].lower()][:10]

