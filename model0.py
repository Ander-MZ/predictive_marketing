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

# Receives a list of transactions with the form (DOW,COM_ID) and returns 2 lists, one with
# transactions made between Monday - Friday and the other with transactions of Saturday - Sunday

def filterByDOW(lst):
	weekday = []
	weekend = []
	for t in lst:
		if t[0] in ['6','0']: # Weekend
			weekend.append(t[1])
		else:
			weekday.append(t[1])

	return (weekday,weekend)

# Receives a list with the training data (visited MCC / COM_ID) and a list of test data 
# (visited MCC / COM_ID) on the next period, and returns a score between 0 and 1 for the 
# prediction of the FIRST transaction

def evaluateAllFirstN(trainingData, testData, n):

	(weekday,weekend) = filterByDOW(trainingData)

	top_weekday = -1
	top_weekend = -1

	if len(weekday) > 0:
		top_weekday = most_common(weekday)

	if len(weekend) > 0:	
		top_weekend = most_common(weekend)

	if top_weekday == -1 and top_weekend != -1: # Transactions only seen on weekends
		top_weekday = top_weekend
	elif top_weekday != -1 and top_weekend == -1: # Transactions only seen on weekdays
		top_weekend = top_weekday

	correct = 1
	i = 0

	while i < n and i < len(testData):
		v = testData[i]

		if v[0] in ['6','0']: # Weekend
			if v[1] != top_weekend:
				correct = 0
		else: # Weekday
			if v[1] != top_weekday:
				correct = 0
		i += 1

	return correct

def evaluateAnyFirstN(trainingData, testData, n):

	(weekday,weekend) = filterByDOW(trainingData)

	top_weekday = -1
	top_weekend = -1

	if len(weekday) > 0:
		top_weekday = most_common(weekday)

	if len(weekend) > 0:	
		top_weekend = most_common(weekend)

	if top_weekday == -1 and top_weekend != -1: # Transactions only seen on weekends
		top_weekday = top_weekend
	elif top_weekday != -1 and top_weekend == -1: # Transactions only seen on weekdays
		top_weekend = top_weekday

	correct = 0
	i = 0

	while i < n and i < len(testData):
		v = testData[i]
		if v[0] in ['6','0']: # Weekend
			if v[1] == top_weekend:
				correct = 1
		else: # Weekday
			if v[1] == top_weekday:
				correct = 1
		i += 1

	return correct

# Receives a transaction history and returns the most probable MCC / COM_ID of the next transaction

def predict(history):

	return most_common(history)

### =================================================================================



