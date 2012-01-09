# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

print 'Hello, world!'

# <codecell>

def kurt(greeting='hi'):
    print greeting

# <markdowncell>

# $ a _ { \epsilon 0 } $

# <codecell>

def chris(n):
    if n < 2:
        return 1
    else:
        return chris(n-1)+chris(n-2)
chris(5)

# <codecell>

chris(6)

# <codecell>

class PrintMeta(type):
    def __repr__(cls):
        return "Hello, world!"
    
class A(object):
    __metaclass__ = PrintMeta

print A
print A()
print object

# <codecell>

def global_var():
    return a

def nonlocal_var():
    b = 2
    def ret():
        return b
    return ret

def local_var():
    c = 3
    return 3

import dis
dis.dis(global_var)
print '---'
dis.dis(nonlocal_var)
print '---'
dis.dis(local_var)

