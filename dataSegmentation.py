# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import sys, getopt
import time
import itertools
import operator
import collections
import matplotlib.pyplot as plt
import math
import random

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

# Output filename

tmp = rfile.split("/")

base_dir = "/".join(tmp[:len(tmp)-1]) + "/"

fig_name = tmp[len(tmp)-1].split(".")[0] + "_matrix.png"

### =================================================================================

# Creates n equaly sized sub-intervals from the given interval

def create_partition(minValue,maxValue,log,n=10):
	if log:
		return np.logspace( int(math.ceil(minValue)-1) , int(math.ceil(maxValue)) , n+1 , dtype=int)
	else:
		return np.linspace( int(math.ceil(minValue)-1) , int(math.ceil(maxValue)) , n+1 , dtype=int)

# Receives a value and a partition and returns the index of the associated partition (starting at 0)

def assign_partition(value,partition):
	i = 0

	# There are n+1 partitions, but only n indices
	while(i < len(partition)-1 and value > partition[i]):
		i += 1

	return i-1
	

def plot_matrix(m,xpartition,ypartition,norm=False):

    # Normalize values between 0 and 1
    if norm:
        cm = m.astype(float)
        for i in range(cm.shape[0]):
            total = cm[i].sum()
            for j in range(cm.shape[1]):
                cm[i,j]=cm[i,j]/total
        m=cm

    # Removed first element of partition. Each square has elements LESS THAN thick

    xtags = map(str,xpartition[1:])
    ytags = map(str,ypartition[1:])

    plt.matshow(m)
    plt.title('Precision of prediction\n')
    if norm:
        plt.clim(0,1)
    plt.colorbar()
    plt.ylabel('Mean amount')
    plt.xlabel('Number of transactions')
    plt.xticks(range(len(xtags)),xtags)
    plt.yticks(range(len(ytags)),ytags)

    plt.savefig(base_dir + fig_name)

    #plt.show()

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

	data = np.asarray(pd.read_csv(ifile,dtype=types)[['pan','amount','com_id']])

	print "\tExtracting transactions"

	max_amount = 0.0
	min_amount = 1000000.0

	max_transactions = 0
	min_transactions = 1000000

	d = collections.defaultdict(list)

	#output_file = open(ofile,'w')
	#write = output_file.write


	amounts = []
	append_a = amounts.append

	transactions = []
	append_t = transactions.append

	# For each 'pan' extract all its transactions

	for pan, grp in itertools.groupby(data, key=operator.itemgetter(0)):
		tmp = map(operator.itemgetter(1,2),grp)
		m_amount = np.mean([float(t[0]) for t in tmp])
		append_a(m_amount)
		t_size = len(tmp)
		append_t(t_size)

		# The boundaries of the space are refined

		if m_amount < min_amount:
			min_amount = m_amount
		elif m_amount > max_amount:
			max_amount = m_amount

		if t_size < min_transactions:
			min_transactions = t_size
		elif t_size > max_transactions:
			max_transactions = t_size 

		# Dictionary that stores a list with (mean amount, number of transactions, precision of predictions) for each 'pan'

		d[pan]=[m_amount,t_size,random.uniform(0,1)]
		
		#write( "%s%s%s%s" % ( pan, "," , len(map(operator.itemgetter(1),grp)) , '\n' ) )

	#output_file.close

	results = np.asarray(pd.read_csv(rfile,header=None)) # (pan,precision)


	print "Limits: Amount [" , min_amount , "," , max_amount , "] , Transactions [" , min_transactions , "," , max_transactions , "]"

	# Removal of extreme values from the results

	median_amount = np.median(np.asarray(amounts))
	median_transaction = np.median(np.asarray(transactions))

	max_amount = median_amount
	max_transactions = median_transaction

	dev_a = 30
	dev_t = 15

	for pan, precision in results:
		if len(d[pan]) > 0:
			d[pan][2]=precision
			if d[pan][0] > dev_a*median_amount:
				d[pan][0] = dev_a*median_amount-1
			if d[pan][1] > dev_t*median_transaction:
				d[pan][1] = dev_t*median_transaction-1			


	print "Amounts: Median = " , median_amount

	print "Transactions: Median = " , median_transaction

	n = 20
	log = False # logarithmic scale for partitioning

	amount_partition = create_partition(min_amount,dev_a*max_amount,log,n)
	transaction_partition = create_partition(min_transactions,dev_t*max_transactions,log,n)

	# Initialize matrix with -1 to differentiate from 0 precision

	mtx = np.zeros((n,n), dtype=np.float)-1

	# values = [mean amount, number of transactions, precision of predictions]
	for pan, values in d.items():
		if len(values) > 0:
			i = assign_partition(values[0],amount_partition)
			j = assign_partition(values[1],transaction_partition)
			mtx[i,j]=values[2]

	# Matrix, xlabels, ylabels 
	plot_matrix(mtx,transaction_partition,amount_partition)

f()


