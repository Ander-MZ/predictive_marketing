# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import sys, getopt
import time
import collections
import itertools
import operator

import plotter


# Store input and output file names
ifile=''
ofile=''
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================



### =================================================================================

types = {'pan':'str',
	  'amount':'float',
	  'mcc':'str',
	  'hour':'int',
	  'dow':'int',
	  'com_id':'str'}

print ">Reading file"

data = np.asarray(pd.read_csv(ifile,dtype=types))

print ">Extracting transactions"

# Group rows by 'pan' and then adds entry to XML tree

progress = 0
results = []

for pan, grp in itertools.groupby(data, key=operator.itemgetter(0)):

	history = map(operator.itemgetter(range(1,len(types))),grp)
	results.append(len(history))
	progress += 1

	if progress%1000==0:
		sys.stdout.write("\tCurrent progress: %d cards grouped\r" % (progress) )
		sys.stdout.flush()


sys.stdout.write("\tCurrent progress: %d cards grouped\r\n" % (len(results)) )
sys.stdout.flush()

plotter.plot_histogram(np.asarray(results),"History length","../results/history_length_histogram.png")

print "Number of cards: " , len(results)

############################################################

















