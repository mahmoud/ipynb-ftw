# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

# hw5 cs171

import requests, json
from pprint import pprint

#api account information
api_key = '8556b3ac919e1575cd05f49fb9d6fe08'
secret = '9ed0596f7ad4ceae66bac1561d1b5451'
num_tracks = 5

#request authentification
t_json_1 = requests.get('http://ws.audioscrobbler.com/2.0/?method=chart.gethypedtracks&api_key='+api_key+'&limit='+str(num_tracks)+'&format=json')
response = json.loads(t_json_1.text)
hyped_tracks = response['tracks']['track']

a_t_pairs = [(t['artist']['name'], t['name']) for t in hyped_tracks]

# <codecell>

pprint(response)
pprint(hyped_tracks[0].keys())

# <codecell>

#get names for hyped tracks
hyped = str([(track['name']) for track in hyped_tracks])

t_json_2 = requests.get('http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key='+api_key+'&artist=cher&track='+hyped+'')
tracks = json.loads(t_json_2.text)

#get information for hyped tracks
track_text = str([(track['name'], track['listeners'], track['playcount'], track['album position'], track['toptags/tag/name'], track['favoritings_count']) for track in tracks])

#copy information to csv file
with open( "last_fm_hyped.csv", "w" ) as txt_file:
    for track in tracks:
        txt_file.write( track_text )

with open('../tracks.json', 'w') as f:
    json.dump(tracks, f, indent=2, sort_keys=True)

with open('../tracks.json') as f:
    tracks = json.load(f)

