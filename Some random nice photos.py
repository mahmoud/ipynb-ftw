# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

import urllib2
from urllib import urlencode
import json

url = 'https://commons.wikimedia.org/w/api.php'
params = {'action': 'query',
          'generator': 'categorymembers',
          'gcmtitle': None,
          'gcmsort': 'timestamp',
          'cmdir': 'desc',
          'gcmtype': 'file',
          'prop': 'imageinfo',
          'iiprop': 'url|user|extmetadata',
          'format': 'json',
          'gcmlimit': 150}

categories = ['Category:Featured pictures of astronomy',
 'Category:Featured pictures of fish',
 'Category:Featured pictures of Charadriiformes',
 'Category:Featured pictures of Passeriformes',
 'Category:Featured pictures of Accipitriformes',
 'Category:Featured pictures of mammals',
 'Category:Featured pictures of architecture',
 'Category:Featured pictures of flowers',
 'Category:Featured pictures of landscapes',
 'Category:Featured night shots',
 'Category:Featured pictures of art',
 'Category:Featured maps',
 'Category:Featured pictures of lighthouses',
 'Category:Featured pictures of churches',
 'Category:Featured pictures of fortresses',
 'Category:Featured pictures of bridges',
 'Category:Featured pictures of the International Space Station',
 'Category:Featured pictures of rolling stock',
 'Category:Featured pictures of motorcycles',
 'Category:Featured pictures of ships',
 'Category:Featured pictures of aircraft',
 'Category:Pictures of the Year (2008)',
 'Category:Pictures of the Year (2009)',
 'Category:Pictures of the Year (2010)',
 'Category:Pictures of the Year (2011)',
 'Category:Pictures of the Year (2012)',
 'Category:Pictures of the Year (2013)']

ret = {}

for category in categories:
    params['gcmtitle'] = category
    encoded_params = urlencode(params)
    resp = urllib2.urlopen(url, data=encoded_params).read()
    resp_data = json.loads(resp)
    print category
    ret.update(resp_data['query']['pages'])

# <codecell>

import random
rand = random.sample(ret.values(), 1000)
print json.dumps(rand)

