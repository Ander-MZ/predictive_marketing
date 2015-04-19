# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
from itertools import izip, islice, product
import scipy.sparse as sps
import math

### =================================================================================

# Receives a list and a positive integer, returning the 'n' most common elements of the
# list, in a tuple (element,frequency). By default returns THE most common element. 

def most_common(lst,n=1):

	if n==1:
		return collections.Counter(lst).most_common(n)[0][0]	
	else:
		return collections.Counter(lst).most_common(n)	

# Receives a list and returns a list of overlapping n-tuples:
# in = [1,2,3,4,5] and n = 2 then out = [(1,2),(2,3),(3,4),(4,5)]
# in = [1,2,3,4,5] and n = 3 then out = [(1,2,3),(2,3,4),(3,4,5)]

def ntuples(lst, n):
	if n == 1:
		tuples = []
		for elem in lst:
			tuples.append((elem,))
		return tuples
	else:
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

def create_transition_matrix(allHistory,order):

	row_code = collections.defaultdict(list)
	col_code = collections.defaultdict(list)
	states = set()
	chains = set()

	# Extract all individual states and then all chains

	for history in allHistory:
		states = set.union(states,set(history))
		chains = set.union(chains,set(ntuples(history,order)))
	
	print "States: " , len(states) , " , Chains: " , len(chains)
	
	# Generate a numerical index for each combination of states seen on chain

	index = 0

	for chain in chains:
		row_code[chain]=index
		index += 1

	# Generate a numerical index for each state

	index = 0

	for element in states:
		col_code[element]=index
		index += 1

	# Create arrays to populate the sparse matrix

	row,col,f = [],[],[]

	append_row = row.append
	append_col = col.append
	append_f = f.append

	# Traverse all histories to extract transitions

	for history in allHistory:
		for chain in ntuples(history,order+1):
			append_row(row_code[chain[:order]])
			append_col(col_code[chain[order:][0]])
			append_f(1) 

	# Create a sparse matrix in 'coo' format with # rows = (states^order) and # cols = states 

	mtx = sps.coo_matrix((f, (row, col)), shape=(len(chains), len(states)))

	# Transform matrix into Compressed Sparse Row format to allow arithmetic manipulation and slicing

	mtx = mtx.tocsr()

	# Normalize matrix to represent probabilities

	#row_sums = np.array(mtx.sum(axis=1))[:,0]
	#row_indices, col_indices = mtx.nonzero()
	#mtx.data = mtx.data / row_sums[row_indices]

	#print "Density: " , mtx.nnz/len(rows)
	#np.savetxt(("../results/matrices/" + str(pan) + ".csv"), matrix, delimiter=",",fmt='%.4f')

	return (mtx,row_code,col_code)


# Receives a list with the training data (visited MCC / COM_ID) and a list of test data 
# (visited MCC / COM_ID) on the next period, and returns a score between 0 and 1 for the prediction

# NOTE: Minimum test data: 2 elements

def evaluate(trainingData, testData, order=1):

	(mtx,row_code,col_code) = create_transition_matrix(trainingData,order)

	correct = 0
	total = 0
	index = 0
	k = 0

	for history in testData:

		total += len(history) # Accumulated number of evaluations

		evaluationHistory = trainingData[index][len(trainingData[index])-order:]+history

		# We add the last 'order' elements from training data to allow a prediction for
		# the first element on the test data

		for chain in ntuples(evaluationHistory,order+1):		

			row = row_code[chain[:order]] # State n
			observed_col = col_code[chain[order:][0]] # State n+1

			if not row == [] and not observed_col == []: # If both states are on the matrix

				if observed_col == index_of_max(mtx,row): # State n+1 with highest probability
					correct += 1

			elif row ==[] and not observed_col == []: # Sequence of business not in matrix

				k += 1

				if observed_col == col_code[most_common(evaluationHistory)]:
					correct += 1

		index += 1

	print "Unobserved states: " , k

	return correct / total

# Receives a transaction history and returns the most probable MCC / COM_ID of the next transaction

def predict(history):

	print ""

### =================================================================================