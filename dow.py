# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
import math
from itertools import izip, islice, product
import scipy.sparse as sps
import warnings
from random import randint

### =================================================================================

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

# Creates a sparse transition matrix for a given 'pan' and its chain of events, modeling an m-order Markov Process. 

def create_sparse_matrix(chain,order):

	row_code = collections.defaultdict(list)
	col_code = collections.defaultdict(list)
	states = set(chain)
	rows = set()

	# Generate a numerical index for each combination of states seen on chain

	for t in ntuples(chain,order):
		rows.add(t)

	index = 0

	for t in rows:
		row_code[t]=index
		index += 1

	# for p in product(sorted(states),repeat=max(order,1)):
	# 	row_code["".join(p)]=index	
	# 	index += 1

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

	# Duplicate entries are summed together

	for t in ntuples(chain,order+1):
		append_row(row_code[t[:order]])
		append_col(col_code[t[order:][0]])
		append_f(1) 

	# Create a sparse matrix in 'coo' format with # rows = (states^order) and # cols = states 
	warnings.filterwarnings("ignore")
	mtx = sps.coo_matrix((f, (row, col)), shape=(len(rows), len(states)))
	# Transform matrix into Compressed Sparse Row format to allow arithmetic manipulation and slicing

	mtx = mtx.tocsr()

	# Normalize matrix to represent probabilities

	#row_sums = np.array(mtx.sum(axis=1))[:,0]
	#row_indices, col_indices = mtx.nonzero()
	#mtx.data = mtx.data / row_sums[row_indices]

	#print "Density: " , mtx.nnz/len(rows)
	#np.savetxt(("../results/matrices/" + str(pan) + ".csv"), matrix, delimiter=",",fmt='%.4f')

	return (mtx,row_code,col_code)

def getDowCode(day):
	if day in ['6','0']:
		return 1
	else:
		return 0

# Return 0 for weekday and 1 for weekend

def predictDow(previous_transaction):
	if previous_transaction[0] in ['6','0']: # Weekend
		if previous_transaction[0] == '0' and int(previous_transaction[3]) > 16:
			return 0
		else:
			return 1
	else:
		return 0

def predictDowMarkov(trainingData, testData, order):

	if len(testData)-order+1 > 0:

		trainingData = [getDowCode(x[0]) for x in trainingData]
		testData = [getDowCode(x[0]) for x in testData]

		# trainingData = [x[0] for x in trainingData]
		# testData = [x[0] for x in testData]

		(mtx,row_code,col_code) = create_sparse_matrix(trainingData,order)

		# print "\nTraining Data: " , trainingData 
		# print "Test Data: " , testData 

		# if col_code[0] == []: # No transactions on weekdays
		# 	print "No Weekdays"
		# if col_code[1] == []:
		# 	print "No Weekends"

		# print col_code
		# print row_code

		# print mtx.todense() , " = " , np.shape(mtx.todense())[0] 

		tuples = ntuples(trainingData[len(trainingData)-order:]+testData,order+1)
		acc = 0

		for t in tuples:

			row = row_code[t[:order]] # State n
			observed_col = col_code[t[order:][0]] # State n+1

			if not row == [] and not observed_col == []: # If both states are on the matrix
				#print "R: " , index_of_max(mtx,row) ,  " P: " , t[order:][0]
				if observed_col == index_of_max(mtx,row):
					acc += 1

			else: # Sequence of business not in matrix
				if observed_col == randomCol(mtx): # Random column
					acc += 1

		return acc / len(tuples)

	else:

		return -1.0

def classifyDOW(trainingData, testData):

	# 0 -> weekday, 1 -> weekend
	real = []
	predicted = []

	for t in testData:
		if t[0] in ['6','0']:
			real.append(1)
		else:
			real.append(0)

	for i in range(len(testData)):
		if i==0:
			t = trainingData[len(trainingData)-1]
			predicted.append(predictDow(t))		
		else:			
			predicted.append(predictDow(testData[i-1]))

	acc = 0.0
	for i in range(len(real)):
		if real[i] == predicted[i]:
			acc += 1

	return acc/len(real)

def predictDOW():
	return 0.0