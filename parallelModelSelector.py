# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
from itertools import izip, islice, product
import scipy.sparse as sps
from xml.etree import cElementTree
import math
import matplotlib
import matplotlib.pyplot as plt
import warnings
from multiprocessing import Pool, Value
import time

# Models

import model0
import model1
import model2
import model3

# Utils

import plotter

### =================================================================================

# Global Variables
total = 0
counter = None

# Command line arguments
history_file=""
results_file=""
alpha=0.75
modelName = ""
m0_max_history = 1000
m1_max_history = 1
m2_max_history = 1
 
# Read command line args (training file, results file, proportion of history)
try:
	myopts, args = getopt.getopt(sys.argv[1:],"i:o:a:n:0:1:2:",["input=","output=","alpha=","name=","model0=","model1=","model2="])
except getopt.GetoptError:
	print "Arguments are incomplete"
	sys.exit(2)
###############################
# opt == option
# arg == argument passed to the o
###############################
for opt, arg in myopts:
    if opt in ("-i","--input"):
        history_file=arg
    elif opt in ("-o","--output"):
        results_file=arg
    elif opt in ("-a","--alpha"):
        alpha=float(arg)
    elif opt in ("-n","--name"):
        modelName=arg
    elif opt in ("-0","--model0"):
        m0_max_history=int(arg)   
    elif opt in ("-1","--model1"):
        m1_max_history=int(arg)   
    elif opt in ("-2","--model2"):
        m2_max_history=int(arg)   
    else:
        print("Usage: %s -i input -o output -a alpha -0 model0 -1 model1 -2 model2" % sys.argv[0])

### =================================================================================

def assign_partition(value,partition):
	i = 0

	# There are n+1 partitions, but only n indices
	while(i < len(partition)-1 and value > partition[i]):
		i += 1

	if value > partition[i]:       
		i += 1

	return i-1

# Updates the matrix containing the results of all evaluations

def update_evaluation_matrix(mtx,counts,results,xpartition,ypartition):

	for p , n in results:

		i = assign_partition(n,ypartition) # Min
		j = assign_partition(n,xpartition) # Max
		v = mtx[i,j]

		# Average of values on the bucket
		if v >= 0:
			if p >= 0:
				nv = v+p
			else:
				nv = v
		else:
			nv = p

		counts[i,j] += 1
		mtx[i,j] = nv
		
	with warnings.catch_warnings():
		warnings.filterwarnings("ignore", message="divide by zero encountered in TRUE_divide")
		mtx = np.where(counts==0, -1, mtx/counts)

	return mtx

# Based on the characteristics of the transaction history of the card, the best
# model is used to create the prediction

def select_and_evaluate_model(history,n_t):

	if len(history) < 2: # Not enought data for training or testing
		
		return 0.0

	elif n_t <= m0_max_history: # Model 0

		return model0.evaluate(history[:n_t],history[n_t:])

	elif n_t <= m1_max_history: # Model 1 (Minimum history length = 9 with alpha = 0.75)	

		return model1.evaluate(history[:n_t],history[n_t:],1)

	elif n_t <= m2_max_history: # Model 2 (Minimum history length = 9 with alpha = 0.75)	

		return model2.evaluate(history[:n_t],history[n_t:],2)

	else: # More than
		
		return -1.0

	print ""

# Prepares global counter for use within processes

def init(args):
    global counter
    counter = args

# Receives an XML node with all the cards and returns a list containing 
# the history of transactions of each card

def extract_history(cards):

	results = []

	for card in cards:

		pan = card.attrib.get('PAN')
		history = []

		for t in card.find('History'):
			history.append(t.attrib.get('COM_ID'))

		results.append(history)

	return results

# This is used for *** PARALLEL *** distribution of tasks
# Receives a card node (XML) and executes the 'Select and Evaluate' method. 

def exec_task(history):

	global counter
	counter.value += 1

	n_t = int(math.floor(alpha*len(history)))

	return ( select_and_evaluate_model(history,n_t) , n_t)

# Receives the XML file containing all the transaction history data, and parses it to populate
# the dictionary required by the models

def parse_XML(doc):

	cards = doc.getroot()

	# Create general transition matrix (Model 3)
	# (general_mtx,row_code,col_code) = model3.create_transition_matrix(extract_history(cards), 1)

	# Updating global variable for progress measuring purposes
	global total
	total = len(cards)

	global counter
	counter = Value('i', 0)

	# Executes card history evaluation in parallel
	pool = Pool(processes=8, initializer = init, initargs = (counter, ))
	rs = pool.map_async(exec_task, extract_history(cards), chunksize = 1)

	while(True):
		if (rs.ready()): 
		    break
		remaining = rs._number_left
		sys.stdout.write("\tCurrent progress: %.2f %% of cards analyzed\r" % (100*(total-remaining)/total) )
		sys.stdout.flush()

		time.sleep(0.1)

	rs.wait()
	
	results = rs.get()

	# Configurations for evaluation matrix
	m_min_history = 0
	m_max_history = 500
	delta = 25
	levels = int(math.floor((m_max_history-m_min_history)/delta))
	mtx = np.zeros((levels,levels), dtype=np.float) - 1
	counts = np.zeros((levels,levels), dtype=np.float)
	min_range = range(m_min_history,delta*levels+m_min_history,delta)
	max_range = range(m_min_history+delta,delta*levels+m_min_history+delta,delta)

	###

	mtx = update_evaluation_matrix(mtx,counts,results,min_range,min_range)

	sys.stdout.write("\tCurrent progress: %.2f %% of cards analyzed\r\n" % (100.00) )
	sys.stdout.flush()

	precision = [float(i[0]) for i in results]

	print "Average precision: " , sum(precision)/len(precision) , " ( min-history = " , min(1,m_min_history) , ", max-history = " , m_max_history, " )"

	plotter.plot_matrix(mtx,max_range,min_range,"Model " + modelName + " precision","../results/model_"+modelName+"_matrix.png")
	plotter.plot_histogram(np.asarray(precision),"Model " + modelName + " precision","../results/model_"+modelName+"_histogram.png")

	print "Evaluation completed!"


def save_results(results):

	mean = np.mean(results)
	median = np.median(results)

	print "Mean: " , mean , ", Median: " , median

	output_file = open(results_file,'w')
	write = output_file.write

	for precision in results:
		write("%s%s" % (precision,"\n"))

	output_file.close


### =================================================================================

t0 = millis = int(round(time.time() * 1000))

print ">Reading file"

tree = cElementTree.parse(history_file)

print ">Parsing file"

parse_XML(tree)

t1 = millis = int(round(time.time() * 1000))

print "Time elapsed (ms): " , t1-t0
