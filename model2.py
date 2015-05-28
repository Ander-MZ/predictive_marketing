# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
from itertools import izip, islice, product
import scipy.sparse as sps
from random import randint

### =================================================================================

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
# If all values of row are 0, then returns -1. If there is a tie, returns a random col index

def index_of_max(mtx,row_index):

	row = mtx[row_index,:].todense()

	if np.sum(row) == 0: # All cols are 0
		# return -1
		return randint(0,np.shape(row)[1]-1) # Random col index
	elif np.sum(row) / np.shape(row)[1] == row[0,0]: # All cols are same value
		# return -2
		return randint(0,np.shape(row)[1]-1) # Random col index
	else:
		return np.argmax(row)

# Receives a sparse matrix and returns the index of the column with highest frequency

def top_freq_col(mtx):
	return np.argmax(mtx.sum(axis=0)) # axis=0 -> sum over columns

# Returns a random column index

def randomCol(mtx):
	col_num = np.shape(mtx[0,:].todense())[1]-1
	return randint(0,col_num) # Random col index

# Receives a dictionary and a value, and returns the key associated to the given value

def key_of_value(d,value):
	key = ''
	for k, v in d.iteritems():
		if v == value:
			key = k
			break
	return key

# Creates a sparse transition matrix for a given 'pan' and its chain of events, modeling a N-gram model 

def create_sparse_matrix(chain,order):

	row_code = collections.defaultdict(list)
	col_code = collections.defaultdict(list)
	states = set(chain)
	
	rows = set()

	# Extract all the different N-Grams from the chain

	for t in ntuples(chain,order):
		rows.add(frozenset(t))

	# Generate a numerical index for each N-Gram

	index = 0

	for ngram in rows:
		row_code[ngram]=index	
		index += 1

	# Generate a numerical index for each unique state

	index = 0

	for element in states:
		col_code[element]=index
		index += 1

	# Create arrays to populate the sparse matrix

	row,col,f = [],[],[]

	append_row = row.append
	append_col = col.append
	append_f = f.append

	# Duplicate entries are summed together

	for t in ntuples(chain,order+1):
		append_row(row_code[frozenset(t[:order])])
		append_col(col_code[t[order:][0]])
		append_f(1) 

	# Create a sparse matrix in 'coo' format with # rows = # N-Grams and # cols = states 

	mtx = sps.coo_matrix((f, (row, col)), shape=(len(row_code), len(col_code)))

	# Transform matrix into Compressed Sparse Row format to allow arithmetic manipulation and slicing

	return (mtx.tocsr(),row_code,col_code)

def evaluateAllFirstN(trainingData, testData, n, order=2):

	# Remove DOW and MONTH from data (not used here)
	trainingData = [x[1] for x in trainingData]
	testData = [x[1] for x in testData]

	(mtx,row_code,col_code) = create_sparse_matrix(trainingData,order)

	correct = 1
	i = 0

	# We add the last 'order' elements from training data to allow a prediction for
	# the first element on the test data

	tuples = ntuples(trainingData[len(trainingData)-order:]+testData,order+1)

	while i < n and i < len(tuples):

		t = tuples[i]

		row = row_code[frozenset(t[:order])] # State n
		observed_col = col_code[t[order:][0]] # State n+1

		if not row == [] and not observed_col == []: # If both states are on the matrix

			if observed_col != index_of_max(mtx,row): # State n+1 with highest probability
				correct = 0

		elif row ==[] and not observed_col == []: # Sequence of business not in matrix

			if observed_col != randomCol(mtx): # Random column
				correct = 0

		else:

			correct = 0

		i += 1

	return correct

def evaluateAnyFirstN(trainingData, testData, n, order=2):

	# Remove DOW and MONTH from data (not used here)
	trainingData = [x[1] for x in trainingData]
	testData = [x[1] for x in testData]

	(mtx,row_code,col_code) = create_sparse_matrix(trainingData,order)

	correct = 0
	i = 0

	# We add the last 'order' elements from training data to allow a prediction for
	# the first element on the test data

	tuples = ntuples(trainingData[len(trainingData)-order:]+testData,order+1)

	while i < n and i < len(tuples):

		t = tuples[i]

		row = row_code[frozenset(t[:order])] # State n
		observed_col = col_code[t[order:][0]] # State n+1

		if not row == [] and not observed_col == []: # If both states are on the matrix

			if observed_col == index_of_max(mtx,row): # State n+1 with highest probability
				correct = 1

		elif row ==[] and not observed_col == []: # Sequence of business not in matrix

			if observed_col == randomCol(mtx): # Random column
				correct = 1

		i += 1

	return correct

# Receives a transaction history and returns the most probable MCC / COM_ID of the next transaction

def predict(history):

	print ""

### =================================================================================