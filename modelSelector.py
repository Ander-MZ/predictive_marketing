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
from random import randint

# Models

import model0_A
import model0
import model1
import model2

# Utils

import plotter

### =================================================================================

# Global variables
results = []

# Store input and output file names
history_file=''
results_file=''
alpha=0.75
modelName = "0"
m0_max_history = 1000
m1_max_history = 1
m2_max_history = 1
firstN = 1
evaltype = "ALL"
 
# Read command line args (training file, results file, proportion of history)
try:
	myopts, args = getopt.getopt(sys.argv[1:],"i:a:t:n:m:",["input=","alpha=","firstN=","model="])
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
    elif opt in ("-a","--alpha"):
        alpha=float(arg)   
    elif opt in ("-n","--firstN"):
        firstN=int(arg)        
    elif opt in ("-m","--model"):
        modelName=arg
    else:
        print("Usage: %s -i input -a alpha -n firstN -m model" % sys.argv[0])

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

def select_and_evaluate_model(history,n):

	if len(history) < 2: # Not enought data for training or testing
		
		return 0.0

	elif modelName == "0": # Model 0

		if evaltype == "ALL":
			return model0.evaluateAllFirstN(history[:n],history[n:],firstN)
		else:
			return model0.evaluateAnyFirstN(history[:n],history[n:],firstN)

	elif modelName == "1": # Model 1

		if evaltype == "ALL":
			return model1.evaluateAllFirstN(history[:n],history[n:],firstN,1)
		else:
			return model1.evaluateAnyFirstN(history[:n],history[n:],firstN,1)

	elif modelName == "2": # Model 2

		if evaltype == "ALL":
			return model2.evaluateAllFirstN(history[:n],history[n:],firstN,2)
		else:
			return model2.evaluateAnyFirstN(history[:n],history[n:],firstN,2)

	else: # 
		
		return -1.0

def fast_iter(history):

	global results

	n = 0
	# Separate history in 2 sections: training (04-08) and test (09)
	# for t in history:
	# 	if int(t[2]) < 9: # Month less than 9 (September)
	# 		n +=1

	# Separate history based on a fraction (default: 75%)
	n = int(math.floor(alpha*len(history)))

	# Only consider cards with transactions on September
	if 0 < n < len(history):
		# p = select_and_evaluate_model(history,n)
		p = model0_A.createInferences(history[:n],history[n:],firstN)
		results.append((p,n))

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

	print "Average precision: " , sum(precision)/len(precision)

	#plotter.plot_matrix(mtx,max_range,min_range,"Precision of model " + modelName,"../results/model_" + modelName + "_matrix.png")
	#plotter.plot_histogram(np.asarray(precision),"Precision of model " + modelName,"../results/model_" + modelName + "_histogram.png")
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
	  'com_id':'str',
	  't_id':'str'}

### PAN = 0, AMOUNT = 1,MCC = 2, YEAR = 3, MONTH = 4,DAY = 5, HOUR = 6, MIN = 7, DOW = 8, COM_ID = 9, T_ID = 10

cols = [0,4,6,8,9,10] # {PAN,MONTH,DOW,COM_ID,T_ID}

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

	# t = {MONTH,HOUR,DOW,COM_ID,T_ID}
	for t in allHistory:
		#card_history.append( (str(t[0]),str(t[1]),str(t[2]),str(t[3]),str(t[4])) ) # Index depends of 'cols' array
		card_history.append( (str(t[0]),str(t[1]),str(t[2]),str(t[3]),str(randint(1,9223372036854775807))) ) # Index depends of 'cols' array
															   
	fast_iter(card_history)

	del grp

sys.stdout.write("\tCurrent progress: %d cards processed\r\n" % (progress) )
sys.stdout.flush()

print ">Creating output"

create_output()

t1 = millis = int(round(time.time() * 1000))

print "Time elapsed (ms): " , t1-t0

