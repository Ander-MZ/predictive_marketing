# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
import math
from itertools import izip, islice

### =================================================================================

# Receives a list and a positive integer, returning the 'n' most common elements of the
# list, in a tuple (element,frequency). By default returns THE most common element. 

def most_common(lst,n=1):

	if n==1:
		return collections.Counter(lst).most_common(n)[0][0]	
	else:
		return collections.Counter(lst).most_common(n)	

# Receives a list with the training data (visited MCC / COM_ID) and a list of test data 
# (visited MCC / COM_ID) on the next period, and returns a score between 0 and 1 for the prediction

def evaluate(trainingData, testData):

	top = most_common(trainingData)
	correct = 0

	for v in testData:
		if v == top:
			correct += 1

	return correct / len(testData)

# Receives a list with the training data (visited MCC / COM_ID) and a list of test data 
# (visited MCC / COM_ID) on the next period, and returns a score between 0 and 1 for the 
# prediction of the FIRST transaction

def evaluateAllFirstN(trainingData, testData, n):

	top = most_common(trainingData)
	correct = 1

	if n <= len(testData):

		for i in range(n):
			v = testData[i]
			if v != top:
				correct *= 0

	return correct

def evaluateAnyFirstN(trainingData, testData, n):

	top = most_common(trainingData)
	correct = 0

	if n <= len(testData):

		for i in range(n):
			v = testData[i]
			if v == top:
				correct = 1

	return correct

# Receives a transaction history and returns the most probable MCC / COM_ID of the next transaction

def predict(history):

	return most_common(history)

### =================================================================================



