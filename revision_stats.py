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

import numpy
import matplotlib.pyplot
from scipy import stats
import json

# <codecell>

sorted(revs, key=lambda x: int(x['rev_id']), reverse=True)[0]

DATE_FORMAT = '%Y%m%d%H%M%S'
from datetime import timedelta, datetime, date
from collections import defaultdict

def parse_date(d_or_dlist):
    try:
        return datetime.strptime(d_or_dlist, DATE_FORMAT)
    except TypeError:
        try:
            return [datetime.strptime(d, DATE_FORMAT) for d in d_or_dlist]
        except TypeError:
            raise TypeError('parse_date() expects a date string or iterable of date strings')

            
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

DEFAULT_CUTOFF = 2010
def edits_by_day(edits, cutoff=DEFAULT_CUTOFF):
    ed_dict = defaultdict(list)
    for ed in edits:
        dt = parse_date(ed['rev_timestamp'])
        ed_dict[dt.utctimetuple()[:3]].append(ed)
    return [(date(*dtup), len(eds)) for (dtup,eds) in ed_dict.iteritems()
                if dtup[0] >= cutoff]

# <codecell>

def get_reverted_by_summary(revs):
    reverted_revs = []
    for rev in revs:
        if 'revert' in rev['rev_comment'].lower():
            reverted_revs.append(rev['rev_comment'])
    return reverted_revs

get_reverted_by_summary(revs)

# <codecell>

REVERT_LOOKAHEAD = 1
REVERT_THRESHOLD = 0
from __builtin__ import sum, any
def get_diff_sizes(revs, absolute=False):
    if absolute:
        return [(b['rev_user_text'], abs(b['rev_len']-a['rev_len'])) 
                        for a,b in 
                        zip(revs, revs[1:])]
    else:
        return [(b['rev_user_text'], b['rev_len']-a['rev_len'])
                        for a,b in 
                        zip(revs, revs[1:])]
         
def get_editor_bytes(revs):
    editors = {}
    reverted_revs = []
    diff_sizes = get_diff_sizes(revs, absolute=True)
        
    for editor, size in diff_sizes:
        tot_size, count = editors.get(editor, (0,0))
        editors[editor] = ((tot_size + size), (count + 1))
    return editors

def get_reverted_revs(revs):
    reverted_revs = []
    diff_sizes = get_diff_sizes(revs)
    for rev_num, (editor, size) in enumerate(diff_sizes):
        rev_range = [x[1] for x in diff_sizes[rev_num:rev_num+REVERT_LOOKAHEAD+1]]
        if any([ r != 0 for r in rev_range ]) and sum(rev_range) == REVERT_THRESHOLD:
            reverted_revs.append(rev_num)
    return reverted_revs
    
print 'User, (bytes, edits)'
sorted(get_editor_bytes(revs).items(), key=lambda x: x[1], reverse=True)

reverted_revs = get_reverted_revs(revs)
len(reverted_revs)

# <codecell>

revs[9:12]

# <codecell>

ed_data_unsorted = edits_by_day(revs, 2005)
ed_data = sorted(ed_data_unsorted, key=lambda x: x[1], reverse=True)
ed_counts = [e[1] for e in ed_data]

def print_stats(datums):
    print 'Mean:', stats.tmean(datums)
    print 'Median:', stats.cmedian(datums)
    print 'Std Dev:', stats.tstd(datums)
    print 'Variation:', stats.variation(datums)
    print 'Kurtosis:', stats.kurtosis(datums, fisher=False)
    print 'Skewness:', stats.skew(datums)

print_stats(ed_counts)
plot(ed_counts)

# <codecell>

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


