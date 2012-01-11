# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import sys
import types

from dis import findlabels, findlinestarts
from opcode import *

_have_code = (types.MethodType, types.FunctionType, types.CodeType, types.ClassType, type)

def diss(target=None):
    pass

def dissco(co):
    try:
        code = co.co_code
    except AttributeError:
        raise TypeError('disassembly only works on objects with code components.')
    labels = findlabels(code)
    linestarts = dict(findlinestarts(co))
    print labels, linestarts
    
    n = len(code)
    i = 0
    extended_arg = 0
    free = None
    while i < n:
        c  = code[i]
        op = ord(c)
    

def test_func(a):
    if a:
        b = a + 1
    else:
        b = 0
    return b

dissco(test_func.func_code)

