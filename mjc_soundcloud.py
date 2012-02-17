# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import requests, json
from pprint import pprint


CLIENT_ID = '4c2d540368cee6f46196a41e6bf67255'

t_json = requests.get('http://api.soundcloud.com/tracks.json?client_id='+CLIENT_ID+'&limit=10&order=hotness')
tracks = json.loads(t_json.text)

# <codecell>

#pprint(sorted(tracks[0].keys()))

pprint([(track['id'], track['title'], track['playback_count'], track['permalink_url']) for track in tracks])

