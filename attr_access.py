# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

class A(object):
    def __getattribute__(self, name):
        print 'called getattribute'
        return object.__getattribute__(self, name)
        
a = A()
print a.__class__
print type(a)

# <codecell>

# stop_import_stop_import
cur_file_str = open(__file__, 'r').read()
from timeit import timeit

# <codecell>

import sys
import attr_access
inspect.getsource(sys.modules['attr_access'])

