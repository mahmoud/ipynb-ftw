# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

from argparse import ArgumentParser


a = ArgumentParser()

alt = a.add_mutually_exclusive_group()
g1 = alt.add_argument_group()
g1.add_argument('-a')
g1.add_argument('-b')
g2 = alt.add_argument_group()
g2.add_argument('-c')
g2.add_argument('-d')

print a.parse_args(['a c'])

# <codecell>

from argparse import ArgumentParser


a = ArgumentParser(description='ok')

alt = a.add_mutually_exclusive_group()
alt.add_argument('-a')
g2 = alt.add_argument_group()
g2.add_argument('-c')
g2.add_argument('-d')

print a.print_help()

# <codecell>


