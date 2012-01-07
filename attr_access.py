# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

class A(object):
    def __getattribute__(self, name):
        print 'called getattribute'
        return object.__getattribute__(self, name)
        
a = A()

# end_setup_code
print a.__class__
print type(a)

# <codecell>

import sys
import inspect
import attr_access

source = inspect.getsource(attr_access)
setup_code = source.split('# end_setup_code')[0]


from timeit import timeit

print source

