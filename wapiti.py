# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

from wapiti import WapitiClient
from pprint import pprint as pp

client = WapitiClient('mahmoudrhashemi@gmail.com')

# <codecell>

client.get_ancient_pages(limit=5)

# <codecell>

client.get_category_articles('Africa', limit=5)

# <codecell>

es_client = WapitiClient('mahmoud@paypal.com', api_url='http://es.wikipedia.org/w/api.php')
# a handy mapping of namespace name translations
dict([(x.canonical, x.title) for x in es_client.source_info.namespace_map])

# <codecell>

client.print_usage()

