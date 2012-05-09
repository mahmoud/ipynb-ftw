# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import json

with open('weirdnesteddicts.json') as di:
    stuff = json.load(di)

print keys(stuff)

