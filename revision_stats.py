# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

import requests, json
from pprint import pprint

article_title = 'Coffee'
rev_json = requests.get('http://ortelius.toolserver.org:8089/revisions/'+article_title)
revs = json.loads(rev_json.text)['result']

# <codecell>

print sorted(revs[0].keys())

# <codecell>

sorted(revs, key=lambda x: int(x['rev_id']), reverse=True)[0]

from datetime import timedelta, datetime
def parse_date(d):
    return datetime.strptime(d, '%Y%m%d%H%M%S')
def get_time_diffs(times):
    ret = []
    dtimes = []
    tds = []
    tds_seconds = []
    for t in times:
        dtimes.append(parse_date(t))
        
    for x, y in zip(dtimes, dtimes[1:]):
        tds.append(y - x)
        tds_seconds.append(tds[-1].total_seconds())
    return tds_seconds
    

# <codecell>

import numpy
import matplotlib.pyplot
from scipy import stats
import json

#sorted_revs = sorted(revs, key=lambda x: x['rev_len'], reverse=True)
data_unsorted = get_time_diffs([x['rev_timestamp'] for x in revs])
data = sorted(data, reverse=True)

print stats.kurtosis(data, fisher=False)
print stats.skew(data)

print stats.describe(data)

plot(data_unsorted)

# <codecell>

plot(data)

# <codecell>


