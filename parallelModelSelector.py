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
import multiprocessing as mp

# Models

import model0
import model1
import model2

# Utils

import plotter

### =================================================================================



# Global Variables

modelName = "2"
progress = 0
total = 0

# Store input and output file names
history_file=''
results_file=''
alpha=0.75
debug="f"
 
# Read command line args (training file, results file, proportion of history)
myopts, args = getopt.getopt(sys.argv[1:],"i:o:a:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        history_file=a
    elif o == '-o':
        results_file=a
    elif o == '-a':
        alpha=float(a)
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================

# tmp = rfile.split("/")

# base_dir = "/".join(tmp[:len(tmp)-1]) + "/"

# fig_name = tmp[len(tmp)-1].split(".")[0] + "_matrix_" + str(levels) + ".png"

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

	m0_max_history = 25
	m1_max_history = 1
	m2_max_history = 1000

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

	global progress
	global total

	progress += 1

	if progress%1000==0:
		sys.stdout.write("\tCurrent progress: %.2f %% of cards analyzed\r" % (100*progress/total) )
		sys.stdout.flush()

	n_t = int(math.floor(alpha*len(history)))

	return ( select_and_evaluate_model(history,n_t) , n_t)

# Receives the XML file containing all the transaction history data, and parses it to populate
# the dictionary required by the models

def parse_XML(doc):

	precision = 0.0

	m_min_history = 0
	m_max_history = 500

	#####

	delta = 25
	levels = int(math.floor((m_max_history-m_min_history)/delta))

	mtx = np.zeros((levels,levels), dtype=np.float) - 1
	counts = np.zeros((levels,levels), dtype=np.float)

	min_range = range(m_min_history,delta*levels+m_min_history,delta)
	max_range = range(m_min_history+delta,delta*levels+m_min_history+delta,delta)

	#####

	cards = doc.getroot()


	# Updating global variable for progress measuring purposes
	global total
	total = len(cards)

	# Executes card history evaluation in parallel
	pool = mp.Pool(processes=8)
	results = pool.map(exec_task, extract_history(cards))
	
	pool.close()
	pool.join()

	mtx = update_evaluation_matrix(mtx,counts,results,min_range,min_range)

	sys.stdout.write("\tCurrent progress: %.2f %% of cards analyzed\r\n" % (100.00) )
	sys.stdout.flush()

	precision = [float(i[0]) for i in results]

	print "Average precision: " , sum(precision)/len(precision) , " ( min-history = " , min(1,m_min_history) , ", max-history = " , m_max_history, " )"

	plotter.plot_matrix(mtx,max_range,min_range,"Model " + modelName + " precision","../results/model_"+modelName+"_matrix.png")

	plotter.plot_histogram(np.asarray(precision),"Model " + modelName + " precision","../results/model_"+modelName+"_histogram.png")

	print "Evaluation completed!"


def save_results(dict_pan_results):

	mean = np.mean(dict_pan_results.values())
	median = np.median(dict_pan_results.values())

	print "Mean: " , mean , ", Median: " , median

	output_file = open(results_file,'w')
	write = output_file.write

	for pan, precision in dict_pan_results.items():
		write("%s%s" % (precision,"\n"))

	output_file.close


### =================================================================================

# Creates a dictionary containing the transaction history of each card

print ">Reading file"

tree = cElementTree.parse(history_file)

print ">Parsing file"

parse_XML(tree)