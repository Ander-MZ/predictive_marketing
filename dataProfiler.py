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
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================



### =================================================================================

types = {'pan':'str',
	  'amount':'float',
	  'mcc':'str',
	  'year':'int',
	  'month':'int',
	  'day':'int',
	  'hour':'int',
	  'min':'int',
	  'dow':'int',
	  'com_id':'str'}

print ">Reading file"

data = np.asarray(pd.read_csv(ifile,dtype=types))

print ">Extracting transactions"

# Group rows by 'pan' and then adds entry to XML tree

progress = 0
frequencies = []
amounts = []

for pan, grp in itertools.groupby(data, key=operator.itemgetter(0)):

	history = map(operator.itemgetter(range(1,len(types))),grp)
	amount_acc = 0.0

	for t in history:
		amount_acc += float(t[0])
	
	frequencies.append(len(history))
	amounts.append(amount_acc / len(history))

	progress += 1

	if progress%1000==0:
		sys.stdout.write("\tCurrent progress: %d cards grouped\r" % (progress) )
		sys.stdout.flush()


frequencies = np.asarray(frequencies)
amounts = np.asarray(amounts)

frequencies = frequencies[frequencies<=500]
amounts = amounts[amounts<=25000]

sys.stdout.write("\tCurrent progress: %d cards grouped\r\n" % (len(frequencies)) )
sys.stdout.flush()

plotter.plot_histogram(np.asarray(frequencies),"History length","../results/history_length_histogram.png",50)

plotter.plot_histogram(np.asarray(amounts),"Mean purchase amount","../results/mean_amounts_histogram.png",50)

print "Mean purchase amount: " , np.mean(np.asarray(amounts))

print "Median purchase amount: " , np.median(np.asarray(amounts))

print "Number of cards: " , len(frequencies)

############################################################

















