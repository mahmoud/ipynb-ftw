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

a = 'global1'
b = 'global2'
c = 'global3'
def nonlocal_var():
    b = 'deref1'
    c = 'deref2'
    def ret():
        c = 'local1'
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

import byteplay
from byteplay import Code
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
        elif opcode in (STORE_FAST, STORE_DEREF, STORE_GLOBAL):
            opcode = STORE_NAME
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
print type(acb)
print eval(acb)
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
        newcode = AnonymousCodeBlock(func)
        super(Block,self).__init__(eval, newcode) #does nothing?
        update_wrapper(self, func)

class Block(partial):
    def __new__(cls, func, *args, **kwargs):
        newcode = AnonymousCodeBlock(func)
        self = super(Block, cls).__new__(cls, eval, newcode)
        return update_wrapper(self, func)
    def __init__(self, func):
        print (func, self.func, self)
        
nlv = nonlocal_var()
bnlv = Block(nlv)
print bnlv
print bnlv()

# <codecell>

from opcode import *
def make_block_code(co, name=None):
    from types import CodeType
    if not isinstance(co, CodeType):
        raise TypeError('make_block_code requires a code object (e.g., f.func_code)')
    
    code    = co.co_code
    newname = name or co.co_name
    newcode = map(ord, co.co_code)
    names   = list(co.co_names)
    
    i = 0
    codelen = len(newcode)
    extended_arg = 0
    free = None
    while i < codelen:
        c  = code[i]
        op = ord(c)
        op_name = opname[op]
        
        i += 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + (ord(code[i+1])<<8) + extended_arg
            extended_arg = 0
            i += 2
            if op == EXTENDED_ARG:
                extended_arg = (oparg<<16)
            
            if op in hasconst:
                arg = co.co_consts[oparg]
            elif op in hasname:
                arg = co.co_names[oparg]
            elif op in hasjrel:
                arg = i + oparg
            elif op in haslocal:
                arg = co.co_varnames[oparg]
            elif op in hascompare:
                arg = cmp_op[oparg]
            elif op in hasfree:
                if free is None:
                    free = co.co_cellvars + co.co_freevars
                arg = free[oparg]
                
    return co.co_names, co.co_freevars, co.co_cellvars, co.co_varnames
    # TODO? flag to not modify builtins?
    
nlv = nonlocal_var()
print make_block_code(nlv.func_code)

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

