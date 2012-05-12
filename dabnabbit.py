# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

#import gevent

import requests
import json

#import pyquery

API_URL = "http://en.wikipedia.org/w/api.php"

# <codecell>

def get_dab_page_ids(date=None):
    params = {'action': 'query', 
              'list': 'categorymembers', 
              'cmtitle': 'Category:Articles_with_links_needing_disambiguation_from_June_2011', 
              'prop': 'info', 
              'cmlimit': '500', 
              'format': 'json'}
    try:
        a_list_json = requests.get(API_URL, params=params).text
    except Exception as e:
        # TODO: Connection error
        raise
    # TODO: Continue query?
    return [ a['pageid'] for a in 
             json.loads(a_list_json)['query']['categorymembers'] ]

tmp_ids = get_dab_page_ids()

# <codecell>

def get_article_parsed(page_id=None, title=None): #TODO: support lists
    params = {'action':  'query',
              'prop':    'revisions', 
              'rvparse': 'true', 
              'rvprop':  'content|ids', 
              'format':  'json' }
    if page_id:
        params['pageids'] = page_id
    elif title:
        params['titles'] = title
    else:
        raise Exception('You need to pass in a page id or a title.')
        
    try:
        a_json = requests.get(API_URL, params=params).text
    except Exception as e:
        raise
    return json.loads(a_json)['query']['pages'].values()[0]['revisions'][0]['*']

#article_parsed = get_article_parsed(tmp_ids[0])

# <codecell>

from pyquery import PyQuery as pq

def is_fixable_dab_link(parsed_page):
    # Check for redirect
    # Check for hat notes
    pass

# TODO: find context
def find_dab_links(parsed_page):
    ret = []
    d = pq(parsed_page)
    
    dab_link_markers = d('span:contains("disambiguation needed")')
    for dlm in dab_link_markers:
        try:
            dab_link = d(dlm).parents("sup")[0].getprevious() # TODO: remove extra d?
        except Exception as e:
            print 'nope', e
            continue

        if dab_link.tag == 'a':
            ret.append(dab_link.text)
            
    return ret

# <codecell>

from collections import namedtuple
DabOption = namedtuple("DabOption", "title, text, dab_title")

def get_dab_options(dab_page_title):
    ret = []
    parsed_dab_page = get_article_parsed(title=dab_page_title)
    
    d = pq(parsed_dab_page)
    liasons = d('li:contains(a)')

    for lia in liasons:
        # TODO: better heuristic than ":first" link?
        # URL decode necessary? special character handlin'
        title = d(lia).find('a:first').attr('href').split('/')[-1] 
        text = lia.text_content().strip()
        ret.append(DabOption(title, text, dab_page_title))
    
    return ret
    

# <codecell>

get_dab_options('Born to Lose')

