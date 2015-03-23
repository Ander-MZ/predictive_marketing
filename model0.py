# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
import math
from itertools import izip, islice

### =================================================================================

# Store input and output file names
train_file=''
eval_file=''
chain_length = 1
column = ''
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"t:e:n:c:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-t':
        train_file=a
    elif o == '-e':
        eval_file=a
    elif o == '-n':
        chain_length=int(a)
    elif o == '-c':
        column=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================

# Receives a list and a positive integer, returning the 'n' most common elements of the
# list, in a tuple (element,frequency). By default returns THE most common element. 

def most_common(lst,n=1):

	if n==1:
		return collections.Counter(lst).most_common(n)[0][0]	
	else:
		return collections.Counter(lst).most_common(n)

# Creates a transitions matrix for a given 'pan' and its chain of events. The output is saved 
# as a CSV file with filename = pan.csv

def create_matrix(pan,chain):

	states = set(chain)
	code = collections.defaultdict(list)
	index = 0

	# Calculate the ratio transitions/states

	r = (len(chain)-1)/len(states)

	# Generate a numerical index for each state

	for element in states:
		code[element]=index
		index += 1

	matrix = np.zeros([len(states),len(states)],dtype=float)

	# Populate matrix from chain

	for current, next in izip(chain,islice(chain,1,None)):
		i = code[current]
		j = code[next]
		matrix[i][j] += 1

	# Transform frequencies into probabilities

	for row in matrix:
		row_sum = sum(row)
		if row_sum > 0:
			row[:] = [n/row_sum for n in row]

	#np.savetxt(("../results/matrices/" + str(pan) + ".csv"), matrix, delimiter=",",fmt='%.4f')

	return (matrix,code,r)

# Read the training file and store first column ('pan') as key, with
# the most common element as value

def read_train_file():

	pan_test = collections.defaultdict(list)

	with open(train_file) as f:
		for row in f:
			t = row.strip().split(",") 
			pan_test[t[0]]=most_common(t[1:])

	return pan_test

# Read the evaluation file and compare the first n transactions with the most common element.

def evaluate_model(pan_test):

	pan_results = collections.defaultdict(list)

	with open(eval_file) as f:
		for row in f:
			t = row.strip().split(",")
			values = t[1:] 
			n = min(chain_length,len(values))
			top = pan_test[t[0]]
			if not top == []: # 'pan' not seen on training set
				correct = 0
				for v in values[:n]:
					if v == top:
						correct += 1
				pan_results[t[0]]= correct / n

	return pan_results


### =================================================================================

d_test = read_train_file()

d_res = evaluate_model(d_test)

mean = 0.0
total = 0

output_file = open("../results/p" + str(chain_length) + "_" + column + ".csv",'w')
write = output_file.write

for k, v in d_res.items():
	write("%s%s" % (v,"\n"))
	mean += v
	total +=1

output_file.close

print mean/total


