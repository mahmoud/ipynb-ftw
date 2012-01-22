# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

from collections import namedtuple, Counter, defaultdict
from itertools import islice

# <codecell>

f = open('/home/makuro/catamaran/data/simplewiki_categorylinks.csv')
cat_link_csv = f.read()
cat_lines = cat_link_csv.split('\n')
print cat_lines[0]

# <codecell>

f = open('/home/makuro/catamaran/data/simplewiki_page.csv')
page_csv = f.read()
page_lines = page_csv.split('\n')

print page_lines[0]
print page_lines[1]
print page_lines[2]
print
print repr(page_lines[0])
print repr(page_lines[1])

# <codecell>

#namespaces = set(line.split('\t')[1] for line in islice(page_lines, 1, None) if line)
#print namespaces

id_names = {}
for line in islice(page_lines, 1, None):
    if not line:
        continue
    fields = line.split('\t')
    id_names[int(fields[0])] = name = fields[2].strip()
    
print id_names.items()[:10]
#id_names = dict((fields[0],fields[2]) for fields in line.split('\t') for line in islice(page_lines, 1, None) if line)

# <codecell>

CatLink = namedtuple('CatLink', 'from_name to_name link_type')

page_links = {}
subcat_links = {}
for line in islice(cat_lines, 1, None):
    if not line:
        continue
    fields = line.split('\t')
        
    from_id   = fields[0]
    from_name = id_names.get(int(from_id), None)
    if from_name is None:
        # TODO: record this crap
        continue
    to_name   = fields[1]
    sortkey   = fields[2] # probably ignore
    link_type = fields[6]
    
    if link_type == 'page':
        page_links[from_name] = to_name
    elif link_type == 'subcat':
        subcat_links[from_name] = to_name
    
print 'page links:',len(page_links)
print 'subcategory links:',len(subcat_links)

# <codecell>

explicit_cats = defaultdict(set)
all_cats = defaultdict(set)

article_cats = defaultdict(set)

for from_link, to_link in page_links.items():
    if to_link in subcat_links:
        explicit_cats[to_link].add(from_link)
        all_cats[to_link].add(from_link)
        
        article_cats[from_link].add(to_link)
        
        for parent in parents[from_link]:
            all_cats[parent].add(from_link)
        
print len(explicit_cats), 'explicitly used categories.'
print len(all_cats),'implicitly used categories.'

print len(article_cats), 'articles with categories.'
print sum(len(cats) for article,cats in article_cats.items())/len(article_cats), 'average categories per article.'

# <codecell>

explicit_cats = defaultdict(set)
all_cats = defaultdict(set)

for from_link, to_link in page_links.items():
    if to_link in subcat_links:
        explicit_cats[to_link].add(from_link)
        all_cats[to_link].add(from_link)
        for parent in parents[from_link]:
            all_cats[parent].add(from_link)
        
print len(explicit_cats), 'explicitly used categories.'
print len(all_cats),'implicitly used categories.'

