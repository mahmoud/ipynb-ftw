# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

#
# CS 171 2012 HW2 skeleton code for making a 2D scatter plot with matplotlib
#

import numpy
import matplotlib.pyplot
import json

# read refined results from TXT file
lines = []

with open( "raw_data.csv", "r" ) as txtFile:
    lines = txtFile.readlines()

# break lines into tokens
tuples = [ line.strip().split( "," ) for line in lines ]

# remove column headings
titles = tuples.pop(0)

# make separate lists for each column of TXT file
from collections import namedtuple
Laptop = namedtuple('Laptop', 'price, rating, reviews, model, brand, color')

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
                    

props = dict( alpha = 0.5, edgecolors = 'none')

plot = matplotlib.pyplot.scatter(
        [ l.price for l in laptops ],
        [ l.reviews for l in laptops ],
        c=[ l.color for l in laptops ],
        s=[ l.rating for l in laptops ],
        ** props)

matplotlib.pyplot.title( "Newegg Laptops: Correlation Between Rating, Reviewers, and Price by Brand" )
matplotlib.pyplot.ylabel( titles[ 2 ] )
matplotlib.pyplot.xlabel( titles[ 0 ] )
matplotlib.pyplot.grid( True, color = "yellow", which = 'both' )

matplotlib.pyplot.show()

