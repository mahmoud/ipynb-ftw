# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

def shift_reg(next=None):
    while True:
        next, last = (yield last), next

# <codecell>

a = shift_reg()
a.next()
print a.send(3), a.send(2), a.send(1)()

# <codecell>


