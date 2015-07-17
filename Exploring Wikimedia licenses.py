# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

import urllib2
import json
from pprint import pprint

# <codecell>

# Get the licenses
licenses_req = urllib2.urlopen('http://gist.githubusercontent.com/slaporte/3192231ee787409fbec7/raw/8c061c2de6b472186ef5f74f42284daf8b77cfb1/all_licenses.json')
licenses = json.load(licenses_req)

# <codecell>

# How many unique licenses are there?
print len(licenses), 'unique permission templates'

# <codecell>

# How many files have each license?
total_files = 26674464.0
excluded_templates = ['Self']
license_totals = [(l, sum(t.values()), sum(t.values())/total_files) for l, t in licenses.items() if l not in excluded_templates]
license_totals = sorted(license_totals, key=lambda l: l[1], reverse=True)

# <codecell>

# How many tags appear on 500+ files?
print len([l for l in license_totals if l[1] > 500])

# <codecell>

# How many tags appear on 10,000+ files?
print len([l for l in license_totals if l[1] > 10000])

# <codecell>

# How many tags appear on 100,000+ files?
print len([l for l in license_totals if l[1] > 100000])

# <codecell>

# What are the top licenses?
pprint(license_totals[:10])

# <codecell>

def license_stats(name, pattern):
    '''How many permission tags match this pattern?'''
    tags = [l for l in license_totals if pattern in l[0].lower()]
    file_count = sum([l[1] for l in tags])
    percent_tagged = file_count / total_files * 100
    data = (name, len(tags), file_count, percent_tagged)
    return '%s: %s licenses, %s files (%s of Commons)' % data

# <codecell>

# How many tags are related to the public domain?
print license_stats('Public Domain', 'pd-')

# <codecell>

# How many tags are related to Creative Commons?
print license_stats('Creative Commons', 'cc-')

# <codecell>

# How many tags are related to GFDL?
print license_stats('GNU Free Document License', 'gfdl')

# <codecell>

# How many tags are "no known copyright restrictions"?
print license_stats('No known restrictions', 'no_known')

# <codecell>

def license_stats(name, pattern):
    '''How many permission tags match this pattern?'''
    tags = [l for l in license_totals if pattern in l[0].lower()]
    file_count = sum([l[1] for l in tags])
    percent_tagged = file_count / total_files * 100
    data = (name, len(tags), file_count, percent_tagged)
    return '%s: %s licenses, %s files (%s of Commons)' % data
[(l[0], l[1], l[1]/total_files * 100) for l in license_totals if 'pd-' not in l[0].lower() and 'cc-' not in l[0].lower() and 'gfdl' not in l[0].lower()][:10]

# <codecell>

# How many licenses are there?
license_totals = sorted([(l, sum(t.values())) for l, t in licenses.items()], key=lambda l: l[1], reverse=True)
print len(license_totals)

