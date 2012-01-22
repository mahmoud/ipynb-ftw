# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

from collections import namedtuple
from itertools import islice

# <codecell>

CatLink = namedtuple('CatLink', 'from_id to_name link_type')

f = open('/home/makuro/catamaran/data/simplewiki_categorylinks.csv')
cat_link_csv = f.read()
cat_lines = cat_link_csv.split('\n')

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

namespaces = set(line.split('\t')[1] for line in islice(page_lines, 1, None) if line)
print namespaces

line.split('\t')[1] for line in islice(page_lines, 1, None) if line

# <codecell>

cat_links = []
for line in islice(cat_lines, 1, None):
    if not line:
        continue
    fields = line.split('\t')
        
    from_id   = fields[0]
    to_name   = fields[1]
    sortkey   = fields[2] # probably ignore
    link_type = fields[6]

    cat_links.append(CatLink(from_id, to_name, link_type))
    
print cat_links[0]

