# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import sys
import types
from collections import namedtuple

from dis import findlabels, findlinestarts
from opcode import *

class Instruction(object):
    def __init__(self, op=None, oparg=None, arg=None, lineno=None):
        if op:
            self.op  = op
        else:
            self._op = None
        self.oparg   = oparg
        self.arg     = arg
        self.lineno  = lineno

    @property
    def op(self):
        return self._op
    @op.setter
    def op(self, value):
        if value in opmap.values():
            self._op = value
        elif value in opmap:
            self._op = opmap[value]
        else:
            raise ValueError(value+' is an invalid op code or name.')
    
    @property
    def op_name(self):
        return opname[self._op]
    @op_name.setter
    def op_name(self, value):
        self.op = value # call through to other setter
    
    def __str__(self):
        ret = self.op_name
        if self.op > HAVE_ARGUMENT:
            ret += ': '+self.arg
        if self.lineno:
            ret += ' (line '+self.lineno+')'
        return ret
    
    def __repr__(self):
        return str((self.op_name, self.arg, self.lineno))
print Instruction(12).__repr__()
print Instruction(12)

# <codecell>

# a programmatic dis.disco
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
    oparg = None
    arg = None
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
                
        ret.append(Instruction(op, oparg, arg, cur_line))
        oparg = None
        arg = None
    return ret
    
def test_func(a):
    if a:
        b = a + 1
    else:
        b = 0
    return b

import dis
dis.dis(test_func)

dissco(test_func.func_code)

