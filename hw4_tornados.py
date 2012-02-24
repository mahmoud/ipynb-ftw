# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

# HW4

# import
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter as cc
import numpy as np
import csv

# Tornado 2010, 2009, 2008 data
with open('../2010_torn.csv', 'r') as torntxt_2010:
    lines_2010 = torntxt_2010.readlines()
with open('../2009_torn.csv', 'r') as torntxt_2009:
    lines_2009 = torntxt_2009.readlines()
with open('../2008_torn.csv', 'r') as torntxt_2008:
    lines_2008 = torntxt_2008.readlines()

# combine data from files
lines = lines_2010 + lines_2009 + lines_2008

# Prepare lists of latitudes and longitudes
tuples = [line.split(',') for line in lines]

#make seperate lists
from collections import namedtuple
Nader = namedtuple('Nader', 'lons, lats, fujita, color, size')

# add color to fujita scale
#DEFAULT_COLOR = "#008020"
fujita_scale_color_map = { "0": "#7777DD", #(0.0,0.0,0.75),
                 "1": "#5577AA",#(.250,.000,.500),
                 "2": "#AA7755",#(.500,.000,.250),
                 "3": "#AA7777",#(.500,.000,.000),
                 "4": "#DD7777",#(.750,.000,.000),
                 "5": "#DD5577",#(.750,.250,.000),
                    }

torns = []
for t in tuples:
    fujita = t[10].strip()
    torns.append(Nader( lons   = float(t[16]),
                        lats  = float(t[15]), 
                        fujita  = fujita,
                        color   = fujita_scale_color_map.get(fujita, "#FFFFFF"),
                        size   = float(t[21])*float(t[22])
                    ))

# <codecell>

# MAP!!! Specify the map boundaries and projection type
map_func = Basemap(llcrnrlon= -120, llcrnrlat=25, urcrnrlon=-50, urcrnrlat=50,
              projection='tmerc', lon_0 = -95, lat_0 = 35,
              resolution = 'l')
    
# MAP!!! Draw some features of the map
map_func.drawcoastlines(color = 'gray')
map_func.drawcountries(color = 'gray')
map_func.drawstates(color = 'gray')
map_func.fillcontinents(color = 'beige')
map_func.drawmapboundary()

lons = [ t.lons for t in torns ]
lats = [ t.lats for t in torns ]
colors = [t.color for t in torns]
sizes = [float(t.size) * 10 for t in torns]
x,y = map_func(lons, lats)
#colors = ['blue']*(len(x)/2) + ['pink']*(len(x)/2)
print x[:10], y[:10], colors[:10], sizes[:10]
from matplotlib import cm
map_func.scatter(x, y, s=28, marker='o', c=colors, cmap=cm.spring, zorder=2, alpha=0.1)

plt.show()

# <codecell>

dir(cm)

