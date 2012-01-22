# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

from collections import namedtuple
from itertools import islice

# <codecell>

f = open('/home/makuro/catamaran/data/simplewiki_categorylinks.csv')
csv = f.read()
cat_lines = csv.split('\n')
print cat_lines[0]
print cat_lines[1]

CatLink = namedtuple('CatLink', 'from_id to_name link_type')

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

