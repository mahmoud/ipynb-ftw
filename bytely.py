# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

class Instruction(object):
    def __init__(self, op=None, arg=None, lineno=None):
        if op:
            self.op  = op
        else:
            self._op = None
        self.arg     = arg
        self.lineno  = lineno

    @property
    def op(self):
        return self._op
    @op.setter
    def op(self, value):
        if value in opname:
            self._op = value
        elif value in opmap:
            self._op = opmap[value]
        else:
            raise ValueError(value+' is an invalid op code or name.')
    
    @property
    def op_name(self):
        return opname[self._op]
            

        
        

# <codecell>

import sys
import types
from collections import namedtuple

from dis import findlabels, findlinestarts
from opcode import *

_have_code = (types.MethodType, types.FunctionType, types.CodeType, types.ClassType, type)

instruction = namedtuple('instruction', ('opcode','opname','arg','lineno'))


        
def diss(target=None):
    pass

def dissco(co):
    try:
        code = co.co_code
    except AttributeError:
        raise TypeError('disassembly only works on objects with code components.')
        
    ret = []
    labels = findlabels(code)
    linestarts = dict(findlinestarts(co))
    print labels, linestarts
    
    n = len(code)
    i = 0
    cur_line = 0
    extended_arg = 0
    free = None
    while i < n:
        c  = code[i]
        op = ord(c)
        if i in linestarts:
            cur_line = linestarts[i]
        op_name = opname[op]
        
        i += 1
        if op >= HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i+1])*256 + extended_arg
            extended_arg = 0
            i += 2
            if op == EXTENDED_ARG:
                extended_arg = oparg*65536L
            
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
                
        ret.append(instruction(op, op_name, arg, cur_line))
    return ret
    
def test_func(a):
    if a:
        b = a + 1
    else:
        b = 0
    return b

print dissco(test_func.func_code)

import dis
dis.dis(test_func)

# <codecell>

import opcode
type(opcode.HAVE_ARGUMENT)
opcode.HAVE_ARGUMENT

# <codecell>


