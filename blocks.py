# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

def nonlocal_var():
    b = 2
    def ret():
        return b
    return ret

# <codecell>

# debunking http://code.activestate.com/recipes/439096-get-the-value-of-a-cell-from-a-closure/?in=user-2551140

def get_cell_value(cell):
    return type(lambda: 0)(
        (lambda x: lambda: x)(0).func_code, {}, None, None, (cell,)
    )()
    
def get_cell_value_mh(cell):
    return cell.cell_contents

# test

def make_list_appender(mylist):
    def append_to_mylist(newval):
        mylist.append(newval)
        return newval
    return append_to_mylist

somelist = []
somelist_appender = make_list_appender(somelist)
somelist_appender(2)
somelist_appender(3)
print somelist

cell = somelist_appender.func_closure[0]
print get_cell_value(cell)
print get_cell_value_mh(cell)

print get_cell_value(cell) is somelist
print get_cell_value_mh(cell) is somelist

# <codecell>

#print nonlocal_var().func_globals
print dir(nonlocal_var().func_closure[0])
print nonlocal_var().func_closure[0]
[x for x in nonlocal_var().__class__.__dict__ if 'func_' in x]

# <codecell>

eval(nonlocal_var.func_code)

