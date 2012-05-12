# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

#import gevent

import requests
import json
import random
from pyquery import PyQuery as pq

from collections import namedtuple

API_URL = "http://en.wikipedia.org/w/api.php"

# <codecell>

class WikiException(Exception): pass

def api_get(action, params=None, raise_exc=False, **kwargs):
    all_params = {'format': 'json',
                  'servedby': 'true'}
    all_params.update(kwargs)
    all_params.update(params)
    all_params['action'] = action
    
    resp = requests.Response()
    resp.results = None
    try:
        resp = requests.get(API_URL, params=all_params)
    except Exception as e:
        if raise_exc:
            raise
        else:
            resp.error = e
            return resp
    
    mw_error = resp.headers.get('MediaWiki-API-Error')
    if mw_error:
        if raise_exc:
            raise WikiException(mw_error)
        else:
            resp.error = mw_error
            return resp    
    
    try:
        resp.results = json.loads(resp.text)
    except Exception as e:
        if raise_exc:
            raise
        else:
            resp.error = e
            return resp
    
    return resp

# <codecell>

def get_category(cat_name, count=500):
    params = {'list': 'categorymembers', 
              'cmtitle': 'Category:'+cat_name, 
              'prop': 'info', 
              'cmlimit': count}
    return api_get('query', params)
    
def get_dab_page_ids(date=None):
    cat_res = get_category("Articles_with_links_needing_disambiguation_from_June_2011")
    # TODO: Continue query?
    # TODO: Get subcategory of Category:Articles_with_links_needing_disambiguation
    return [ a['pageid'] for a in 
             cat_res.results['query']['categorymembers'] ]

tmp_ids = get_dab_page_ids()

# <codecell>

import time
Page = namedtuple("ParsedPage", "pageid, title, revisionid, revisiontext, is_parsed, fetch_date")

def get_articles(page_id=None, title=None, parsed=True): #TODO: support lists
    ret = []
    params = {'prop':    'revisions',  
              'rvprop':  'content|ids' }

    if page_id:
        if not isinstance(page_id, (str,unicode)):
            try:
                page_id = "|".join([str(p) for p in page_id])
            except:
                pass
        params['pageids'] = str(page_id)
    elif title:
        params['titles'] = title
    else:
        raise Exception('You need to pass in a page id or a title.')
    if parsed:
        params['rvparse'] = 'true'
    # ret=return, req=request, resp=response, res=result(s)
    parse_resp = api_get('query', params)
    if parse_resp.results:
        ret = [Page( pageid = page['pageid'],
                     title  = page['title'],
                     revisionid = page['revisions'][0]['revid'],
                     revisiontext = page['revisions'][0]['*'],
                     is_parsed = parsed,
                     fetch_date = time.time())
               for page in parse_resp.results['query']['pages'].values()]
    return ret

articles_parsed = get_articles(tmp_ids[:10])

# <codecell>

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

DabOption = namedtuple("DabOption", "title, text, dab_title")

def get_dab_options(dab_page_title):
    ret = []
    parsed_dab_page = get_articles(title=dab_page_title)[0].revisiontext
    
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

import random
def get_random_articles(sample=10):
    page_range = random.sample(get_dab_page_ids(), sample)
    return get_articles(page_range)

get_random_articles(3)

# <codecell>

class Dabblet(object):
    def __init__(self):
        pass

# <codecell>

get_dab_options('Born to Lose')

