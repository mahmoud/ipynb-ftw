# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

#
# CS 171 2012 HW2 skeleton code for making a 2D scatter plot with matplotlib
#

import numpy
import matplotlib.pyplot

# read refined results from TXT file
lines = []

with open( "../refined_newegg.tsv", "r" ) as txtFile:
    lines = txtFile.readlines()

# break lines into tokens
tuples = [ line.strip().split( "\t" ) for line in lines ]

# remove column headings
tuples.pop(0)

# sanity check - only work with a small example
# tuples = tuples[ 0::1 ]

# make separate lists for each column of TXT file
from collections import namedtuple
Laptop = namedtuple('Laptop', 'price, rating, reviews, model, brand, color')

#adds colors to scatter plot (by appending list with color value)
DEFAULT_COLOR = "#008020"
color_brand_map = { "ASUS": "#FF33CC",
                    "Sony VAIO": "#FF3366",
                    "DELL": "#FF6633",
                    "Toshiba": "#FFCC33",
                    "Acer America": "#CC33FF",
                    "Lenovo": "#002EB8",
                    "Gateway": "#003DF5",
                    "MSI": "#B88A00",
                    "Hewlett-Packard": "#66FF33",
                    "SAMSUNG": "#33FFCC",
                    "Fujitsu": "#800020"
                    }

laptops = []
for t in tuples:
    brand = t[4].strip()
    laptops.append(Laptop( price   = float(t[0]),
                           rating  = float(t[1]), 
                           reviews = float(t[2]),
                           model   = t[3].strip(),
                           brand   = brand,
                           color   = color_brand_map.get(brand, DEFAULT_COLOR))
                    )
                    

print [ l.price for l in laptops ]
print [ l.reviews for l in laptops ]
print [ l.color for l in laptops ]

# <codecell>

plot = matplotlib.pyplot.scatter(
        [ l.price for l in laptops ],
        [ l.reviews for l in laptops ],
        c=[ l.color for l in laptops ] )

matplotlib.pyplot.title( "Newegg Laptops: Correlation Between Rating, Reviewers, and Price by Brand" )
matplotlib.pyplot.ylabel( titles[ 2 ] )
matplotlib.pyplot.xlabel( titles[ 0 ] )
matplotlib.pyplot.semilogy()
matplotlib.pyplot.grid( True, which = 'both' )

matplotlib.pyplot.show()

