# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys, getopt
import time
import itertools
import operator as op
import collections

### =================================================================================

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

# Receives a list and a positive integer, returning the 'n' most common elements of the
# list, in a tuple (element,frequency). by default returns THE most common element. 
def most_common(lst,n=1):
    return collections.Counter(lst).most_common(n)

### =================================================================================

# Dictionary for storing a 'pan' and its associated 'mcc' 

dict_pan_mcc = collections.defaultdict(list)

# Read the file and store first column ('pan') as key, with a list of 'mcc' as value

with open(ifile) as f:
	for row in f:
		values = row.strip().split(",") 
		dict_pan_mcc[values[0]]=values[1:]


dict_pan_mcc_top = collections.defaultdict(list)

# Generate a dictionary containing a 'pan' and its most common 'mcc'

for pan, mccs in dict_pan_mcc.items():
	dict_pan_mcc_top[pan]=Utils.most_common(mccs,1)[0][0]





