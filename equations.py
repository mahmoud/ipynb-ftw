# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

from pylab import *
import numpy as np

# <codecell>

# testing matplotlib (it works!)
x = randn(10000)
y = hist(x,100)

# <codecell>

def fights_per_level(level):
    factor = 0.514
    height = 2.21
    width  = 2.94
    return (height * (width*level)**factor) - 3

sample_data = zip(*((1,1),(5,5),(10,9),(20,16),(30,20),(50,25)))
xdata = np.array([1,5,10,20,30,50]) #70
ydata = np.array([1,5, 9,16,20,25]) #26

plot(*sample_data)
plot(range(1,50),[fights_per_level(x) for x in range(1,50)])

# <codecell>

from scipy import interpolate
f = interpolate.interp1d(*sample_data, kind='linear')
xnew = range(1,50)
ynew = [y for y in f(xnew)]
plot(xdata, ydata)
plot(xnew, ynew)

# <codecell>

def fights_per_level(levels, factor=0.5, height=2.2, width=3):
    return np.array([height * (width*level)**factor - 3 for level in levels])

from scipy.optimize import curve_fit
popt, pcov = curve_fit(fights_per_level, xdata, ydata, np.array([0.5,2.2,3]))
print popt, pcov

plot(xdata, ydata)
plot(np.array(xrange(1,50)), np.array(fights_per_level(xrange(1,50))))
plot(np.array(xrange(1,50)), np.array(fights_per_level(xrange(1,50),popt[0],popt[1],popt[2])))

# <codecell>

def xp_for_even_fight(level):
    factor = 0.514
    height = 2.21
    width  = 2.94
    return (100 * level)/((height * (width*level)**factor) - 3)
print xp_for_even_fight(1), xp_for_even_fight(2)
plot(range(1,50),[xp_for_even_fight(x) for x in range(1,50)])

# <codecell>

def get_bounty(level1, level2):
    from random import randint
    ret = max((5 + level2 - level1)/5.0, 1) * xp_for_even_fight(level2)
    ret += randint(0,9)
    return ret
print get_bounty(5, 10), get_bounty(9,10)
plot(range(1,20), [get_bounty(x,10) for x in range(1,20)])

