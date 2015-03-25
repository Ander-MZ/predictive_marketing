# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt

### =================================================================================

# Store input and output file names
ifile=''
ofile=''
column=1
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:c:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    elif o == '-c':
        column=int(a)
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================

tmp = ifile.split("/")

base_dir = "/".join(tmp[:len(tmp)-1]) + "/"

fig_name = tmp[len(tmp)-1].split(".")[0] + ".png"

#data = np.asarray(pd.read_csv(ifile,header=None))

data = np.asarray(pd.read_csv(ifile,header=None).ix[:,column:column+1]) # We select the column with the value

data = data[data>=0] # Remove -1 from the 'not found in training' cases

nx, xbins, ptchs = plt.hist(data, bins=20)
plt.clf() # Get rid of this histogram since not the one we want.

nx_frac = nx/len(data) # Each bin divided by total number of objects.
width = xbins[1] - xbins[0] # Width of each bin.
x = np.ravel(zip(xbins[:-1], xbins[:-1]+width))
y = np.ravel(zip(nx_frac,nx_frac))

plt.plot(x,y)
plt.fill_between(x, 0, y)
plt.title("Precision Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
#plt.show()
plt.savefig(base_dir + fig_name)