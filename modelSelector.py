# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
from itertools import izip, islice, product
import scipy.sparse as sps
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree, ElementPath
from xml.dom import minidom
import math
import matplotlib
import matplotlib.pyplot as plt
import warnings

# Models

import model0
import model1


### =================================================================================

# Store input and output file names
train_file=''
eval_file=''
results_file=''
alpha=0.75
memory=1
debug="f"
 
# Read command line args (training file, evaluation file, results file, order of the chain, debug mode)
myopts, args = getopt.getopt(sys.argv[1:],"t:e:r:o:a:")
 
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

def plot_matrix(m,xpartition,ypartition,title,norm=False):

    # Normalize values between 0 and 1
    if norm:
        cm = m.astype(float)
        for i in range(cm.shape[0]):
            total = cm[i].sum()
            for j in range(cm.shape[1]):
                cm[i,j]=cm[i,j]/total
        m=cm

    if ypartition[0]==0:
    	ypartition[0]=1

    xtags = map(str,xpartition)
    ytags = map(str,ypartition)

    # Set up a colormap:
    #palette = matplotlib.cm.RdYlGn
    palette = matplotlib.cm.jet
    palette.set_under('gray', 1.0)

    plt.matshow(m,vmin=0,vmax=1,cmap=palette)
    plt.title(title+'\n')
    plt.colorbar()
    

    plt.ylabel('Min history')
    plt.xlabel('Max history')
    plt.xticks(range(len(xtags)),xtags)
    plt.yticks(range(len(ytags)),ytags)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    
    #plt.savefig(base_dir + fig_name
    plt.savefig("../results/model0_x.png")
    #plt.show()

def update_evaluation_matrix(mtx,counts,n,p,xpartition,ypartition):
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


# Based on the characteristics of the transaction history of the card, the best
# model is used to create the prediction

def select_model(history):

	h_size = len(history)

	m0_max_history = 25 

	m1_max_history = 1000

	if h_size == 1: # 
		print ""

	elif h_size <= m0_max_history: # Model 0

		precision += model0.evaluate(history[:n_t],history[n_t:])

	elif h_size <= m1_max_history: # Model 0	

		precision += model1.evaluate(history[:n_t],history[n_t:],1)

	else: # More than
		print ""

	print ""

# Receives the XML file containing all the transaction history data, and parses it to populate
# the dictionary required by the models

def parse_XML(doc):

	d = collections.defaultdict(list)
	cards = doc.getElementsByTagName('Card')

	progress = 0
	precision = 0.0

	m0_min_history = 1
	m0_max_history = 20 # Average precision:  0.203688330522 for [1,20]

	m1_min_history = 50
	m1_max_history = 450

	#####

	delta = 25

	levels = int(math.floor((m1_max_history-m1_min_history)/delta))

	mtx = np.zeros((levels,levels), dtype=np.float) - 1
	counts = np.zeros((levels,levels), dtype=np.float)

	min_range = range(m1_min_history,delta*levels+m1_min_history,delta)
	max_range = range(m1_min_history+delta,delta*levels+m1_min_history+delta,delta)

	#####

	for card in cards:

		progress += 1

		if progress%500==0:
			sys.stdout.write("\tCurrent progress: %.2f %% of cards analyzed\r" % (100*progress/len(cards)) )
			sys.stdout.flush()

		pan = card.getAttribute('PAN')
		transactions = card.getElementsByTagName('T')
		history = []
		n = len(transactions)
		n_t = int(math.floor(alpha*n))
		n_e = n - n_t

		#print "Number of transactions: %d (%d -> training, %d -> evaluation)" % (n,n_t,n_e)

		for t in transactions:
			for attrName, attrValue in t.attributes.items():
				if attrName == "COM_ID":
					history.append(str(attrValue))		

		# Model 0

		if m0_min_history <= n_t <= m0_max_history and len(history) >= 2:
			precision += model0.evaluate(history[:n_t],history[n_t:])

		# Model 1

		# if m1_min_history <= n_t <= m1_max_history and len(history) >= 2:
		# 	precision += model1.evaluate(history[:n_t],history[n_t:],1)

		############################################################

		if len(history)>2:
			p = model0.evaluate(history[:n_t],history[n_t:])
			update_evaluation_matrix(mtx,counts,n_t,p,min_range,min_range)

		############################################################

		d[pan] = history

	sys.stdout.write("\tCurrent progress: %.2f %% of cards analyzed\r\n" % (100.00) )
	sys.stdout.flush()

	print "Average precision: " , precision / progress , " ( min-history = " , m1_min_history , ", max-history = " , m1_max_history, " )"

	with warnings.catch_warnings():
		warnings.filterwarnings("ignore", message="divide by zero encountered in TRUE_divide")
		mtx = np.where(counts==0, -1, mtx/counts)
	plot_matrix(mtx,max_range,min_range,"Model 0 results")



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

xml_history = minidom.parse(train_file)

print ">Parsing file"

parse_XML(xml_history)

# dict_pan_history = read_train_file()

# for 

# if not eval_file == '':
# 	dict_pan_results = evaluate_model(dict_pan_matrix,memory)

# save_results(dict_pan_results)
