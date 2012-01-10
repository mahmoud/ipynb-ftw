# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

def nonlocal_var():
    b = 2
    def ret():
        return b
    return ret

# <codecell>

#print nonlocal_var().func_globals
print dir(nonlocal_var().func_closure[0])
print nonlocal_var().func_closure[0]
[x for x in nonlocal_var().__class__.__dict__ if 'func_' in x]

nonlocal_var().func_globals

