# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
import math
from itertools import izip, islice

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

# Receives a list and a positive integer, returning the 'n' most common elements of the
# list, in a tuple (element,frequency). By default returns THE most common element. 

def most_common(lst,n=1):

	if n==1:
		return collections.Counter(lst).most_common(n)[0][0]	
	else:
		return collections.Counter(lst).most_common(n)	

# Returns '1' if transaction ocurred on Weekend, '0' if ocurred on Weekday

def predictDow(previous_transaction):
	if previous_transaction[0] in ['6','0']: # Weekend
		if previous_transaction[0] == '0' and int(previous_transaction[3]) > 16:
			return 0
		else:
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
			weekday.append(t[0])

	return (weekday,weekend)

# Predicts the DOW for each of the transactions in the testData. This method uses the previous
# transaction's DOW to predict the DOW of the next transaction. It is NOT using the future to
# predict, as is real life for any transaction all the previous ones are available.

def predictDows(trainingData, testData):
	predicted = []
	for i in range(len(testData)):
		if i==0:
			t = trainingData[len(trainingData)-1]
			predicted.append(predictDow(t))		
		else:			
			predicted.append(predictDow(testData[i-1]))

	return predicted

# Receives a list with the training data (visited MCC / COM_ID) and a list of test data 
# (visited MCC / COM_ID) on the next period, and returns a score between 0 and 1 for the 
# prediction of the FIRST transaction

def evaluateAllFirstN(trainingData, testData, n):

	if n > len(testData):
		return -1.0 # Ignore this card for this specific test
	else:

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

		predictions = [] 

		for i in range(len(testData)):
			p = predictedDows[i]

			if p == 1: # Weekend
				predictions.append(top_weekend)
			else: # Weekday
				predictions.append(top_weekday)
			i += 1

		real_tuples = []

		for t in ntuples(testData,n):
			real_tuples.append([x[1] for x in t])

		predicted_tuples = [list(t) for t in ntuples(predictions,n)]

		acc = 0

		for i in range(len(real_tuples)):
			if real_tuples[i] == predicted_tuples[i]:
				acc += 1

		return acc / len(real_tuples)

def evaluateAnyFirstN(trainingData, testData, n):

	if n > len(testData):
		return -1.0 # Ignore this card for this specific test
	else:

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
		acc = 0

		real_tuples = []

		for t in ntuples(testData,n):
			real_tuples.append([x[1] for x in t])

		for i in range(len(real_tuples)):

			t = real_tuples[i] # Get the corresponding tuple of transactions
			week_time = predictedDows[i]

			if week_time == 1: # Weekend
				for v in t:
					if v == top_weekend:
						correct = 1
						break
				
			else: # Weekday
				for v in t:
					if v == top_weekday:
						correct = 1
						break

			if correct == 1:
				acc += 1
				correct = 0		

		return acc / len(real_tuples)

# Receives a transaction history and returns the most probable MCC / COM_ID of the next transaction

def predict(history):

	return most_common(history)

### =================================================================================



