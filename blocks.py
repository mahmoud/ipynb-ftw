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

# proving http://code.activestate.com/recipes/440515-changing-a-closed-over-value-in-a-cell/?in=user-2551140
import new, dis

cell_changer_code = new.code(
    1, 1, 2, 0,
    ''.join([
        chr(dis.opmap['LOAD_FAST']), '\x00\x00',
        chr(dis.opmap['DUP_TOP']),
        chr(dis.opmap['STORE_DEREF']), '\x00\x00',
        chr(dis.opmap['RETURN_VALUE'])
    ]), 
    (), (), ('newval',), '<nowhere>', 'cell_changer', 1, '', ('c',), ()
)

def change_cell_value(cell, newval):
    return new.function(cell_changer_code, {}, None, (), (cell,))(newval)

def change_cell_value_mh(cell, newval):
    cell.cell_contents = newval

def constantly(n):
    def return_n():
        return n
    return return_n

f = constantly("Hi, Mom.")
print f()
print f.func_closure
change_cell_value(f.func_closure[0], "Hi, Dad.")
print f()
try:
    change_cell_value_mh(f.func_closure[0], "Hi again, Mom.")
except AttributeError as e:
    print 'No can do:',e,'(Try making a copy and returning a new function instead.)'

# <codecell>

#print nonlocal_var().func_globals
print dir(nonlocal_var().func_closure[0])
print nonlocal_var().func_closure[0]
[x for x in nonlocal_var().__class__.__dict__ if 'func_' in x]

# <codecell>

# Using the exec statement and calling eval() result in the same stack depth.
# Neither one is itself on the stack. PDW: What function call isn't added to the stack?
# Furthermore: eval(f.func_code) == f()
outside = True
def raiser():
    import sys
    try:
        print sys._getframe().f_locals['outside']
    except:
        print 'nope'
    print sys._getframe(1).f_locals['outside']
#let's look at the stack
eval(raiser.func_code)
print ''
exec raiser.func_code

# <codecell>

code = raiser.func_code.co_code
len(raiser.func_code.co_code)

