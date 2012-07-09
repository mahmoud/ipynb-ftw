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

with open('../tracks.json', 'w') as f:
    json.dump(tracks, f, indent=2, sort_keys=True)

# <codecell>

with open('../tracks.json') as f:
    tracks = json.load(f)

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

plot(range(0,len(data)), data_unsorted)

# <codecell>

import numpy
import matplotlib.pyplot
import json

colors = {}

x_val = lambda t: int(t['playback_count'])
y_val = lambda t: int(t['favoritings_count'])
c_val = lambda t: colors.get(t['genre'], 'blue')
s_val = lambda t: 50

x_label = 'Plays'
y_label = 'Downloads'

print [(x_val(t), y_val(t)) for t in tracks]
print set(t['genre'] for t in tracks)

props = dict( alpha=0.5, edgecolors = 'none')

plot = matplotlib.pyplot.scatter(
        [ x_val(t) for t in tracks ],
        [ y_val(t) for t in tracks ],
        c=[ c_val(t) for t in tracks ],
        s=[ s_val(t) for t in tracks ],
        **props)

matplotlib.pyplot.title( "SoundCloud tracks" )
matplotlib.pyplot.xlabel( x_label )
matplotlib.pyplot.ylabel( y_label )
matplotlib.pyplot.grid( True, color = "yellow", which = 'both' )

matplotlib.pyplot.show()

# <codecell>


