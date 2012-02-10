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

# remove line breaks
lines = [ line.strip() for line in lines ]

# break lines into tokens
tuples = [ line.split( "\t" ) for line in lines ]

# remove column headings
tuples.pop()

# sanity check - only work with a small example
# tuples = tuples[ 0::1 ]

# make separate lists for each column of TXT file
from collections import namedtuple
Laptop = namedtuple('Laptop', 'price, rating, reviews, model, brand, color')

laptops = []
for t in tuples:
    laptops.append(Laptop( price   = float(t[0]),
                           rating  = float(t[1]), 
                           reviews = float(t[2]),
                           model   = t[3].strip(),
                           brand   = t[4].strip())
                    )
                    
    
Price   = [ float( t[0] ) for t in tuples ]
Rating  = [ float( t[1] ) for t in tuples ]
Reviews = [ float( t[2] ) for t in tuples ]
Model   = [ str( t[3] ) for t in tuples ]
Brand   = [ str( t[4] ) for t in tuples ]

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

colour = [ str( t[ 5 ] ) for t in tuples ]

plot = matplotlib.pyplot.scatter(
        Price,
        Reviews,
        c = colour )

matplotlib.pyplot.title( "Newegg Laptops: Correlation Between Rating, Reviewers, and Price by Brand" )
matplotlib.pyplot.ylabel( titles[ 2 ] )
matplotlib.pyplot.xlabel( titles[ 0 ] )
matplotlib.pyplot.semilogy()
matplotlib.pyplot.grid( True, which = 'both' )

matplotlib.pyplot.show()

