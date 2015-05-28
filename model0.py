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

# Returns '1' if transaction ocurred on Weekend, '0' if ocurred on Weekday

def getDowCode(transaction):
	if transaction[0] in ['6','0']: # Weekend
		return 1
	else:
		return 0

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

# Predicts the DOW for each of the transactions in the testData. This method uses the previous
# transaction's DOW to predict the DOW of the next transaction. It is NOT using the future to
# predict, as is real life for any transaction all the previous ones are available.

def predictDows(trainingData, testData):
	predicted = []
	for i in range(len(testData)):
		if i==0:
			t = trainingData[len(trainingData)-1]
			predicted.append(getDowCode(t))		
		else:			
			predicted.append(getDowCode(testData[i-1]))

	return predicted

# Receives a list with the training data (visited MCC / COM_ID) and a list of test data 
# (visited MCC / COM_ID) on the next period, and returns a score between 0 and 1 for the 
# prediction of the FIRST transaction

def evaluateAllFirstN(trainingData, testData, n):

	(weekday,weekend) = filterByDOW(trainingData)
	predictedDows = predictDows(trainingData, testData)

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
		p = predictedDows[i]
		if p == 1: # Weekend
			if v[1] != top_weekend:
				correct = 0
		else: # Weekday
			if v[1] != top_weekday:
				correct = 0
		i += 1

	return correct

def evaluateAnyFirstN(trainingData, testData, n):

	(weekday,weekend) = filterByDOW(trainingData)
	predictedDows = predictDows(trainingData, testData)

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
		p = predictedDows[i]
		if p == 1: # Weekend
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



