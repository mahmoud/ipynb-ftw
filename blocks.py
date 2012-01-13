# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <markdowncell>

# Link cache:
# 
# * http://docs.python.org/library/inspect.html
# * http://hg.python.org/cpython/file/2.7/Lib/opcode.py
# * http://hg.python.org/cpython/file/2.7/Lib/dis.py
# * http://docs.python.org/library/dis.html
# * http://stackoverflow.com/questions/1609716/i-need-closure
# * http://www.voidspace.org.uk/python/articles/code_blocks.shtml#using-anonymouscodeblock
#     

# <codecell>

import traceback

a = 'global_a'
b = 'global_b'
c = 'global_c'
def nonlocal_var():
    b = 'deref_b'
    c = 'deref_c'
    def ret():
        print 'inside',lulu
        lulu = 99
        c = 'local_c'
        return (a,b,c)
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

x = 3
codestr = 'print x\nx=7'
codeobj = compile(codestr, '<codestr>', 'exec')
eval(codeobj)
print x

# <codecell>

import inspect
from byteplay import Code, opmap

LOAD_FAST = opmap['LOAD_FAST']
STORE_FAST = opmap['STORE_FAST']
LOAD_NAME = opmap['LOAD_NAME']
STORE_NAME = opmap['STORE_NAME']
LOAD_DEREF = opmap['LOAD_DEREF']
STORE_DEREF = opmap['STORE_DEREF']
LOAD_GLOBAL = opmap['LOAD_GLOBAL']
STORE_GLOBAL = opmap['STORE_GLOBAL']

def AnonymousCodeBlock(function):
    argSpec = inspect.getargspec(function)
    if [i for x in argSpec if x is not None for i in x]:
        raise TypeError("Function '%s' takes arguments" % function.func_name)

    code = Code.from_code(function.func_code)
    newBytecode = []
    for opcode, arg in code.code:
        if opcode in (LOAD_FAST, LOAD_DEREF, LOAD_GLOBAL):
            opcode = LOAD_NAME
        elif opcode in (STORE_FAST, STORE_NAME, STORE_DEREF, STORE_GLOBAL):
            opcode = STORE_FAST
        newBytecode.append((opcode, arg))
    code.code = newBytecode
    code.newlocals = False
    code.freevars = ()
    return code.to_code()

#from types import CodeType
#class CallableCode(CodeType):
#    def __call__(self):
#        print 'hi'
nlv = nonlocal_var()
acb = AnonymousCodeBlock(nlv)
#acb.__class__ = CallableCode
#acb()
lulu = 'lulu2'
print type(acb)
print eval(acb)
del lulu
#type(lambda:0)(acb,{},'derp',())()

# <codecell>

from functools import partial, update_wrapper, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES
p = partial(eval, acb, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES)
update_wrapper(p, nlv)
p = partial(eval, acb)

class Block(partial):
    """ This doesn't work. self.func is already set when __init__ gets called """
    def __init__(self, func):
        print self
        print dir(self) #already has self.func = ret?? 
        newcode = make_block_code(func.func_code)
        super(Block,self).__init__(eval, newcode) #does nothing?
        update_wrapper(self, func)

class Block(partial):
    def __new__(cls, func, *args, **kwargs):
        newcode = make_block_code(func.func_code)
        self = super(Block, cls).__new__(cls, eval, newcode)
        self.code = newcode
        return update_wrapper(self, func)
        
nlv = nonlocal_var()
bnlv = Block(nlv)
print bnlv
print bnlv()

import dis
print '----'
def lu(f):
    lulu = 3
    f()
    print lulu
print lu(bnlv)
dis.disco(bnlv.code)
dis.dis(lu)

# <codecell>

from opcode import *

def find_or_append(lst, val):
    try:
        return lst.index(val)
    except ValueError:
        lst.append(val)
        return len(lst)-1

def make_block_code(co, co_name=None):
    from types import CodeType
    if not isinstance(co, CodeType):
        raise TypeError('make_block_code requires a code object (e.g., f.func_code)')
    
    code    = co.co_code
    flags   = 64 # CO_NOFREE on; CO_NEWLOCALS, CO_OPTIMIZED (and everything else) off
    
    newname  = co_name or co.co_name
    newcode  = []
    names    = [] # Normal, unoptimized locals
    varnames = [] # Used to overcome optimized LOAD/STORE_FAST in enclosing scope
    """ We don't know if the enclosing function is using LOAD_NAME or LOAD_FAST 
after the block has been called, so we store to both to be sure. If the enclosing function isn't
looking in FAST, then those will get cleaned up soon enough."""
    
    i = 0
    codelen = len(code)
    extended_arg = 0
    free = None
    is_store = False
    while i < codelen:
        c  = code[i]
        op = ord(c)
        
        if op in (LOAD_FAST, LOAD_DEREF, LOAD_GLOBAL):
            newcode.append(LOAD_NAME)
        elif op in (STORE_FAST, STORE_DEREF, STORE_GLOBAL):
            newcode.append(STORE_NAME)
            is_store = True
        else:
            newcode.append(op)
            
        i += 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + (ord(code[i+1])<<8) + extended_arg
            
            if op in hasname:
                name = co.co_names[oparg]
            elif op in haslocal:
                name = co.co_varnames[oparg]
            elif op in hasfree:
                if free is None:
                    free = co.co_cellvars + co.co_freevars
                name = free[oparg]
            else:
                name = None
                newcode.append(ord(code[i]))
                newcode.append(ord(code[i+1])<<8)
                
            if name is not None:
                n = find_or_append(names, name)
                newcode.append(n & 0xFF)
                newcode.append((n >> 8) & 0xFF)
                if is_store:
                    newcode.append(LOAD_NAME)
                    newcode.append(n & 0xFF)
                    newcode.append((n >> 8) & 0xFF)
                    newcode.append(STORE_FAST)
                    n = find_or_append(varnames, name)
                    newcode.append(n & 0xFF)
                    newcode.append((n >> 8) & 0xFF)
                    is_store = False
            
            if op == EXTENDED_ARG:
                extended_arg = (oparg<<16)
                raise ValueError("Blocks don't support extended args, yet.") # TODO
            
            i += 2
                
    #return co.co_names, co.co_freevars, co.co_cellvars, co.co_varnames
    codestr = ''.join(map(chr,newcode))
    return type(co)(co.co_argcount, len(names), co.co_stacksize, flags,
                    codestr, co.co_consts, tuple(names), tuple(varnames), co.co_filename, newname,
                    co.co_firstlineno, co.co_lnotab, (), ())
    # TODO? flag to not modify builtins?
    
    
nlv = nonlocal_var()

from byteplay import Code
acb = AnonymousCodeBlock(nlv)
acb_code = Code.from_code(acb)
acb_cmp = acb_code.code

mbc = make_block_code(nlv.func_code)

#print repr(mbc.co_code)
#print repr(acb_code.to_code().co_code)
from bytely import dissco
dissco(mbc)
mbc_cmp = Code.from_code(mbc).code

print mbc.co_varnames
print mbc.co_names
print
print mbc.co_stacksize
print acb_code.to_code().co_stacksize
print mbc_cmp
print acb_cmp
eval(acb)
eval(mbc)

# <codecell>

nlv = nonlocal_var()
nf  = nlv.func_code
acb = AnonymousCodeBlock(nlv)

print Code.from_code(nf).to_code().co_names
print '---'
print Code.from_code(acb).to_code().co_names
print '---'
print Code.from_code(nf).code
print '---'
print Code.from_code(acb).code
print '---'
print repr(nf.co_code)
print '---'
print repr(acb.co_code)

# <codecell>

# Test 1
def f():
    x = 5

bf = Block(f)
    
x = 1
print 'pre-block  x:',x
bf()
print 'post-block x:',x
assert x == 5
print

# Test 2
def f2():
    print _a
bf2 = Block(f2)

def a():
    _a = 1
    def b():
        print _a
        bf2()
    return b
a()()
        

