# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

import requests, json
from pprint import pprint

article_title = 'Coffee'
rev_json = requests.get('http://ortellius.toolserver.org:8089/revisions/'+article_title)
revs = json.loads(rev_json.text)

# <codecell>

print sorted(tracks[0].keys())

#pprint([(track['id'], track['title'], track['playback_count'], track['permalink_url']) for track in tracks])

# <codecell>

with open('../tracks.json', 'w') as f:
    json.dump(tracks, f, indent=2, sort_keys=True)

# <codecell>

with open('../tracks.json') as f:
    tracks = json.load(f)

# <codecell>

sorted(tracks, key=lambda x: int(x['playback_count']), reverse=True)[0]['permalink_url']

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


