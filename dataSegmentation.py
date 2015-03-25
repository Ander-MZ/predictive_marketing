# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import sys, getopt
import time
import itertools
import operator
import collections

### =================================================================================

# Store input and output file names
ifile=''
rfile=''
column='com_id'
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:r:c:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-r':
        rfile=a
    elif o == '-c':
        column=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================

print "\tReading file"

# Input file must be sorted by grouping key!

def f():

	# types = {'pan':'str',
	# 	  'amount':'float',
	# 	  'mcc':'str',
	# 	  'month':'int',
	# 	  'day':'int',
	# 	  'hour':'int',
	# 	  'min':'int',
	# 	  'dow':'int',
	# 	  'com_id':'str'}

	types = {'pan':'str',
		  'amount':'float',
		  'com_id':'str'}


	# Read CSV file and extract columns 'pan' & 'mcc'

	data = np.asarray(pd.read_csv(ifile,dtype=types)[['pan','amount','com_id']])

	print "\tExtracting transactions"

	max_amount = 0
	min_amount = 1

	max_transactions = 0
	min_transaction = 1

	mtx = collections.defaultdict(list)

	#output_file = open(ofile,'w')
	#write = output_file.write

	# Group rows by 'pan' and then write a file with a row for each pan & its 
	# associated values listed in chronological order (ascending)


	for key, grp in itertools.groupby(data, key=operator.itemgetter(0)):
		tmp = map(operator.itemgetter(1,2),grp)
		m_amount = np.mean([float(t[0]) for t in tmp])
		t_size = len(tmp)

		# The boundaries of the space are refined

		if m_amount < min_amount:
			min_amount = m_amount
		elif m_amount > max_amount:
			max_amount = m_amount

		if t_size > max_transactions:
			max_transactions = t_size 

		# Dictionary that stores a list with (mean amount, number of transactions, precision of predictions) for each 'pan'

		mtx[key]=[m_amount,t_size,0]
		
		#write( "%s%s%s%s" % ( key, "," , len(map(operator.itemgetter(1),grp)) , '\n' ) )

	#output_file.close

	results = np.asarray(pd.read_csv(rfile,header=None)) # (pan,precision)

	for pan, precision in results:
		if len(mtx[pan]) > 0:
			mtx[pan][2]=precision
			print mtx[pan]


f()


