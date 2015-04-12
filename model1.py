# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
from itertools import izip, islice, product
import scipy.sparse as sps

### =================================================================================

# Receives a list and returns a list of overlapping n-tuples:
# in = [1,2,3,4,5] and n = 2 then out = [(1,2),(2,3),(3,4),(4,5)]
# in = [1,2,3,4,5] and n = 3 then out = [(1,2,3),(2,3,4),(3,4,5)]

def ntuples(lst, n):
    return zip(*[lst[i:]+lst[:i] for i in range(n)])[:(-n+1)]

# Receives a sparse matrix and a row index, and returns the col index of the max value in that row

def index_of_max(mtx,row):
	return np.argmax(mtx[row,:].todense())

# Receives a sparse matrix and returns the index of the column with highest frequency

def top_freq_col(mtx):
	return np.argmax(mtx.sum(axis=0)) # axis=0 -> sum over columns

# Receives a dictionary and a value, and returns the key associated to the given value

def key_of_value(d,value):
	key = ''
	for k, v in d.iteritems():
		if v == value:
			key = k
			break
	return key

# Creates a sparse transition matrix for a given 'pan' and its chain of events, modeling an m-order Markov Process. 

def create_sparse_matrix(chain,order):

	row_code = collections.defaultdict(list)
	col_code = collections.defaultdict(list)
	states = set(chain)
	
	# Calculate the ratio transitions/states

	r = (len(chain)-1)/len(states)

	# Generate a numerical index for each combination of states

	index = 0

	for p in product(sorted(states),repeat=max(order,1)):
		row_code["".join(p)]=index	
		index += 1

	# Generate a numerical index for each state

	index = 0

	for element in sorted(states):
		col_code[element]=index
		index += 1

	# Create arrays to populate the sparse matrix

	row,col,f = [],[],[]

	append_row = row.append
	append_col = col.append
	append_f = f.append

	# Duplicate entries are summed together

	for t in ntuples(chain,order+1):
		append_row(row_code["".join(t[:order])])
		append_col(col_code[t[order:][0]])
		append_f(1) 

	# Create a sparse matrix in 'coo' format with # rows = (states^order) and # cols = states 

	mtx = sps.coo_matrix((f, (row, col)), shape=(len(states)**order, len(states)))

	# Transform matrix into Compressed Sparse Row format to allow arithmetic manipulation and slicing

	mtx = mtx.tocsr()

	# Normalize matrix to represent probabilities

	#row_sums = np.array(mtx.sum(axis=1))[:,0]
	#row_indices, col_indices = mtx.nonzero()
	#mtx.data = mtx.data / row_sums[row_indices]


	#print "Density: " , mtx.nnz/len(states)**(order+1)
	#np.savetxt(("../results/matrices/" + str(pan) + ".csv"), matrix, delimiter=",",fmt='%.4f')

	return (mtx,row_code,col_code)


# Receives a list with the training data (visited MCC / COM_ID) and a list of test data 
# (visited MCC / COM_ID) on the next period, and returns a score between 0 and 1 for the prediction

def evaluate(trainingData, testData, order=1):

	(mtx,row_code,col_code) = create_sparse_matrix(trainingData,order)

	n = len(testData)-order # Number of n-tuples in chain of test data

	correct = 0

	if n > 0:

		# We add the last 'order' elements from training data to allow a prediction for
		# the first element on the test data

		for t in ntuples(trainingData[len(trainingData)-order:]+testData,order+1):

			row = row_code["".join(t[:order])] # State n
			observed_col = col_code[t[order:][0]] # State n+1

			if not row == [] and not observed_col == []: # If both states are on the matrix

				if observed_col == index_of_max(mtx,row): # State n+1 with highest probability
					correct += 1

			elif row ==[] and not observed_col == []: # Sequence of business not in matrix

				if observed_col == top_freq_col(mtx): # Most frequent state for given 'pan'
					correct += 1

	return correct / len(testData)

# Receives a transaction history and returns the most probable MCC / COM_ID of the next transaction

def predict(history):

	print ""

### =================================================================================
