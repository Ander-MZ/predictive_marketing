# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
import math
from itertools import izip, islice

### =================================================================================

# Return 0 for weekday and 1 for weekend

def predictDow(previous_transaction):
	if previous_transaction[0] in ['6','0']: # Weekend
		if previous_transaction[0] == '0' and int(previous_transaction[3]) > 16:
			return 0
		else:
			return 1
	else:
		return 0

def classifyDOW(trainingData, testData):

	# 0 -> weekday, 1 -> weekend
	real = []
	predicted = []

	for t in testData:
		if t[0] in ['6','0']:
			real.append(1)
		else:
			real.append(0)

	for i in range(len(testData)):
		if i==0:
			t = trainingData[len(trainingData)-1]
			predicted.append(predictDow(t))		
		else:			
			predicted.append(predictDow(testData[i-1]))

	acc = 0.0
	for i in range(len(real)):
		if real[i] == predicted[i]:
			acc += 1

	return acc/len(real)

def predictDOW():
	return 0.0