# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import pandas as pd
import sys, getopt
from itertools import izip, islice, product
import scipy.sparse as sps
import math
import matplotlib
import matplotlib.pyplot as plt
import warnings
import time
import itertools
import operator

# Models

import model0
import model1
import model2
import model3

# Utils

import plotter

### =================================================================================

# Global variables
precision = 0.0
results = []

# Store input and output file names
history_file=''
results_file=''
alpha=0.75
modelName = ""
m0_max_history = 1000
m1_max_history = 1
m2_max_history = 1
firstN = 1
evaltype = "ALL"
 
# Read command line args (training file, results file, proportion of history)
try:
	myopts, args = getopt.getopt(sys.argv[1:],"i:o:a:t:n:m:0:1:2:",["input=","output=","alpha=","evaltype=","firstN=","name=","model0=","model1=","model2="])
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
    elif opt in ("-t","--evaltype"):
        evaltype=arg       
    elif opt in ("-n","--firstN"):
        firstN=int(arg)        
    elif opt in ("-m","--modelName"):
        modelName=arg
    elif opt in ("-0","--model0"):
        m0_max_history=int(arg)   
    elif opt in ("-1","--model1"):
        m1_max_history=int(arg)   
    elif opt in ("-2","--model2"):
        m2_max_history=int(arg)   
    else:
        print("Usage: %s -i input -o output -a alpha -0 model0 -1 model1 -2 model2" % sys.argv[0])

print "Model: " , modelName

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

	global firstN

	if len(history) < 2: # Not enought data for training or testing
		
		return 0.0

	elif n_t <= m0_max_history: # Model 0

		if evaltype == "ALL":
			return model0.evaluateAllFirstN(history[:n_t],history[n_t:],firstN)
		else:
			return model0.evaluateAnyFirstN(history[:n_t],history[n_t:],firstN)

	elif n_t <= m1_max_history: # Model 1 (Minimum history length = 9 with alpha = 0.75)	

		if evaltype == "ALL":
			return model1.evaluateAllFirstN(history[:n_t],history[n_t:],firstN,1)
		else:
			return model1.evaluateAnyFirstN(history[:n_t],history[n_t:],firstN,1)

	elif n_t <= m2_max_history: # Model 2 (Minimum history length = 9 with alpha = 0.75)	

		if evaltype == "ALL":
			return model2.evaluateAllFirstN(history[:n_t],history[n_t:],firstN,2)
		else:
			return model2.evaluateAnyFirstN(history[:n_t],history[n_t:],firstN,2)

	else: # More than
		
		return -1.0

def fast_iter(history):

	global precision
	global results

	n_t = int(math.floor(alpha*len(history)))
	p = select_and_evaluate_model(history,n_t)
	precision += p
	results.append((p,n_t))

def create_output():

	global results

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
	precision = [float(i[0]) for i in results]

	print "Average precision: " , sum(precision)/len(precision) , " ( min-history = " , min(1,m_min_history) , ", max-history = " , m_max_history, " )"

	with warnings.catch_warnings():
		warnings.filterwarnings("ignore", message="divide by zero encountered in TRUE_divide")
		mtx = np.where(counts==0, -1, mtx/counts)

	#plotter.plot_matrix(mtx,max_range,min_range,"Precision of model " + modelName,"../results/model_" + modelName + "_matrix.png")
	plotter.plot_histogram(np.asarray(precision),"Precision of model " + modelName,"../results/model_" + modelName + "_histogram.png")
	plotter.plot_row_matrix(mtx,max_range,"Precision of model " + modelName,"../results/model_" + modelName + "_row_matrix.png")

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

types = {'pan':'str',
	  'amount':'float',
	  'mcc':'str',
	  'year':'int',
	  'month':'int',
	  'day':'int',
	  'hour':'int',
	  'min':'int',
	  'dow':'int',
	  'com_id':'str'}

### PAN = 0, AMOUNT = 1,MCC = 2, YEAR = 3, MONTH = 4,DAY = 5, HOUR = 6, MIN = 7, DOW = 8, COM_ID = 9

cols = [0,8,9]

t0 = millis = int(round(time.time() * 1000))

print ">Reading CSV file"

data = np.asarray(pd.read_csv(history_file,dtype=types,usecols=cols))

print ">Processing CSV file"

progress = 0

for pan, grp in itertools.groupby(data, key=operator.itemgetter(0)):

	allHistory = map(operator.itemgetter(range(1,len(cols))),grp)
	card_history = []
	progress += 1

	if progress%1000==0:
		sys.stdout.write("\tCurrent progress: %d cards processed\r" % (progress) )
		sys.stdout.flush()

	# CardHistory = {AMOUNT,MCC,YEAR,MONTH,DAY,HOUR,MIN,DOW,COM_ID}

	# AllHistory = {{AMOUNT, MCC, ...},{AMOUNT, MCC, ...},...,{AMOUNT, MCC, ...}}

	for t in allHistory:
		card_history.append( (str(t[0]),str(t[1])) ) # Index depends of 'cols' array

	fast_iter(card_history)

	del grp

sys.stdout.write("\tCurrent progress: %d cards processed\r\n" % (progress) )
sys.stdout.flush()

print ">Creating output"

create_output()

t1 = millis = int(round(time.time() * 1000))

print "Time elapsed (ms): " , t1-t0

