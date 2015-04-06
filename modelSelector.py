# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
from itertools import izip, islice, product
import scipy.sparse as sps

### =================================================================================

# Store input and output file names
train_file=''
eval_file=''
results_file=''
memory=1
debug="f"
 
# Read command line args (training file, evaluation file, results file, order of the chain, debug mode)
myopts, args = getopt.getopt(sys.argv[1:],"t:e:r:o:d:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-t':
        train_file=a
    elif o == '-e':
        eval_file=a
    elif o == '-r':
        results_file=a
    elif o == '-o':
        memory=int(a)
    elif o == '-d':
        debug=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================


# Receives a list and returns a list of overlapping n-tuples:
# in = [1,2,3,4,5] and n = 2 then out = [(1,2),(2,3),(3,4),(4,5)]
# in = [1,2,3,4,5] and n = 3 then out = [(1,2,3),(2,3,4),(3,4,5)]

def ntuples(lst, n):
    return zip(*[lst[i:]+lst[:i] for i in range(n)])[:(-n+1)]

# Receives a sparse matrix and a row index, and returns the col index of the max value in that row.
# If the row is full of zeros, then the index of the most frequent column is returned.

def index_of_max(mtx,row_index):
	row = mtx[row_index,:]
	if row.sum() == 0:
		i = top_freq_col(mtx)
	else:
		i = np.argmax(row.todense())
	return i

# Receives a sparse matrix and returns the index of the column with highest frequency

def top_freq_col(mtx):
	sums = mtx.sum(axis=0) # Sum the columns
	return np.argmax(sums)

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

	# for k, v in row_code.items():
	# 	print "key: ", k, " value: ", v

	# print ""

	# for k, v in col_code.items():
	# 	print "key: ", k, " value: ", v

	# print ""


	# Create arrays to populate the sparse matrix

	row,col,f = [],[],[]

	append_row = row.append
	append_col = col.append
	append_f = f.append

	if order == 0: # Matrix only matters for state with top frequency

		for state in chain:
			append_row(0) # Unique row
			append_col(col_code[state])
			append_f(1)

	else:

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

	if debug=="t":
		print "Density: " , mtx.nnz/len(states)**(order+1)
		#if len(states) <= 7:	
			#print "\n" , mtx.todense() , "\n\n***\n"

	#np.savetxt(("../results/matrices/" + str(pan) + ".csv"), matrix, delimiter=",",fmt='%.4f')

	return (mtx,row_code,col_code)


# Read the file and store first column ('pan') as key, with a chain of events as value

def read_train_file():

	# Dictionary for storing a 'pan' and its associated transaction history

	dict_pan_history = collections.defaultdict(list)	

	with open(train_file) as f:
		for row in f:
			t = row.strip().split(",") 
			dict_pan_history[t[0]]=t[1:]

	return dict_pan_history

# Read the evaluation file and compare the first n transactions against the Markov Chain expectations

def evaluate_model(dict_pan_matrix,order):

	dict_pan_results = collections.defaultdict(list)

	print ""

	with open(eval_file) as f:
		for row in f:
			values = row.strip().split(",")
			pan = values[0]
			chain = values[1:] 

			model = dict_pan_matrix[pan]

			if len(model) > 0: # The evaluation 'pan' was seen on the training phase

				(mtx,row_code,col_code) = model

				if order == 0: # Order 0 is interpreted as comparison against the most frequent value

					top = top_freq_col(mtx) # Most frequent state for given 'pan'
					correct = 0

					if debug == 't':
						print "Most frequent value: " , key_of_value(col_code,top)

					for state in chain:
						
						if col_code[state] == top:
							correct += 1

					dict_pan_results[pan] = correct / len(chain)

					if debug == 't':
						print "Precision for pan: ", pan , " = " , correct / len(chain) , "\n"

				else: # Order of Marvov Chain is >= 1

					n = len(chain)-order # Number of n-tuples in chain

					if n > 0:

						correct = 0

						for t in ntuples(chain,order+1):

							row = row_code["".join(t[:order])] # State n
							observed_col = col_code[t[order:][0]] # State n+1

							if not row == [] and not observed_col == []: # If both states are on the matrix
								predicted_col = index_of_max(mtx,row) # State n+1 with highest probability

								if observed_col == predicted_col:
									correct += 1

						dict_pan_results[pan] = correct / n

						if debug == 't':
							print "Precision for pan: ", pan , " = " , correct / n , "\n"

					else: # Not enough transactions

						dict_pan_results[pan]= -1	

			else: # New 'pan', not seen on training phase (card without transactions on training period)

				# We should try to predict its next transaction with other means

				if debug == 't':
					print "pan: " , pan , " not seen on training"
				#
				# WORK TO DO
				#
				#

	return dict_pan_results


def save_results(dict_pan_results):

	mean = np.mean(dict_pan_results.values())
	median = np.median(dict_pan_results.values())

	print "Mean: " , mean , ", Median: " , median

	output_file = open(results_file,'w')
	write = output_file.write

	for pan, precision in dict_pan_results.items():
		write("%s%s" % (precision,"\n"))

	output_file.close

# Based on the characteristics of the transaction history of the card, the best
# model is used to create the prediction:

# Only 1 transaction
# Many transactions, all or almost all in the same place
# Many transactions, in different places

def select_model(history):

	h_size = len(history)

	if h_size == 1: # 
		print ""
	elif h_size <= 20: # 
		print ""
	else: # More than
		print ""

	print ""


### =================================================================================

# Creates a dictionary containing the transaction history of each card
dict_pan_history = read_train_file()

for 

if not eval_file == '':
	dict_pan_results = evaluate_model(dict_pan_matrix,memory)

save_results(dict_pan_results)
