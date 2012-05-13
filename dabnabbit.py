# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import gevent
import socket
from gevent import monkey
monkey.patch_all()
urls = ['en.wikipedia.org', 'example.com']
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=2)
[job.value for job in jobs]

# <codecell>

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

def get_articles(page_id=None, title=None, parsed=True, follow_redirects=False): #TODO: support lists
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
    if follow_redirects:
        params['redirects'] = 'true'
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

#articles_parsed = get_articles(tmp_ids[:10])
import time
start = time.time()
ajobs = [gevent.spawn(get_articles, tmp_ids[i:i+10]) for i in range(0, len(tmp_ids), 10)]
gevent.joinall(ajobs, timeout=30)
end = time.time()

# <codecell>

articles_parsed = []
for aj in ajobs:
    articles_parsed.extend([at for at in aj.value if at])
    
revsize = sum(len(v.revisiontext) for v in articles_parsed)

print len(vals), 'articles'
print revsize, 'bytes'
print end - start, 'seconds'

len(tmp_ids)

# <codecell>

def is_fixable_dab_link(parsed_page):
    # Check for redirect
    # Check for hat notes
    pass

DabOption = namedtuple("DabOption", "title, text, dab_title")

def get_dab_options(dab_page_title):
    ret = []
    dab_page = get_articles(title=dab_page_title, follow_redirects=True)[0]
    dab_text = dab_page.revisiontext
    
    d = pq(dab_text)
    
    liasons = set([ d(a).parents('li')[-1] for a in d('li a') ])
    
    for lia in liasons:
        # TODO: better heuristic than ":first" link?
        title = d(lia).find('a:first').attr('title') 
        text = lia.text_content().strip()
        ret.append(DabOption(title, text, dab_page.title))
    
    return ret

class Dabblet(object):
    def __init__(self, dab_title, link_context, source_page, source_order):
        self.dab_title    = dab_title
        self.context = link_context
        self.source_page  = source_page
        self.source_order = source_order
        
        self.options = get_dab_options(dab_title)
        
def get_context(dab_a):
    d = dab_a(dab_a.parents()[0])
    link_parents = dab_a.parents()
    cand_contexts = [ p for p in link_parents if p.text_content() and len(p.text_content().split()) > 30 ]
    chosen_context = cand_contexts[-1]
    d(chosen_context).addClass('dab-context')
    # add upperbound/wrapping div
    return d(chosen_context)
    
def get_dabblets(parsed_page):
    ret = []
    d = pq(parsed_page.revisiontext)
    
    dab_link_markers = d('span:contains("disambiguation needed")')
    for i, dlm in enumerate(dab_link_markers):
        try:
            dab_link = d(dlm).parents("sup")[0].getprevious() # TODO: remove extra d?
            dab_link = d(dab_link)
        except Exception as e:
            print 'nope', e
            continue
        if dab_link.is_('a'):
            dab_title = dab_link.attr('title')
            d(dab_link).addClass('dab-link')
            context = get_context(dab_link)
            ret.append( Dabblet(dab_title, context.outerHtml(), parsed_page, i) )
            
    return ret

from itertools import chain
dabblets = []

#dabblets.extend(chain(*[get_dabblets(ap) for ap in articles_parsed]))

# <codecell>

dabblets[0].options

# <codecell>


# <codecell>

import random
def get_random_articles(sample=10):
    page_range = random.sample(get_dab_page_ids(), sample)
    return get_articles(page_range)

get_random_articles(3)

# <codecell>

get_dab_options('Born to Lose')

