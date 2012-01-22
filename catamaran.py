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
    
print page_links.items()[:10]
print
print subcat_links.items()[:10]

# <codecell>

parents = defaultdict(list)

cycles = 0
for subcat,parent in subcat_links.items():
    parents[subcat].append(parent)
    while parent in subcat_links:
        parent = subcat_links[parent]
        if parent in parents[subcat]:
            cycles += 1
            break
        parents[subcat].append(parent)
        
print 'categories with parents:', len(parents)
print 'categories without parents:', len(subcat_links)-len(parents)
print 'average depth:',sum([len(ps) for cat, ps in parents.items() ])/len(parents)
print 'cycles detected:', cycles

