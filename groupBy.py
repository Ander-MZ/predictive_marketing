# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import sys, getopt
import time
import itertools
import operator

### =================================================================================

# Store input and output file names
ifile=''
ofile=''
column='com_id'
 
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
        column=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================

print "\tReading file"

# Input file must be sorted by grouping key!

def f():

	types = {'pan':'str',
		  'amount':'float',
		  'mcc':'str',
		  'month':'int',
		  'day':'int',
		  'hour':'int',
		  'min':'int',
		  'dow':'int',
		  'com_id':'str'}


	# Read CSV file and extract columns 'pan' & 'mcc'

	data = np.asarray(pd.read_csv(ifile,dtype=types)[['pan',column]])

	#data = np.asarray(pd.read_csv(ifile)[['pan',column]])

	print "\tExtracting transactions"

	output_file = open(ofile,'w')
	write = output_file.write

	# Group rows by 'pan' and then write a file with a row for each pan & its 
	# associated values listed in chronological order (ascending)

	for key, grp in itertools.groupby(data, key=operator.itemgetter(0)):
		write( "%s%s%s%s" % ( key, "," , ','.join(map(str,map(operator.itemgetter(1),grp))) , '\n' ) )

	# pan,value1,value2,...,valueN

	output_file.close
	print "\tExtraction completed"

f()


