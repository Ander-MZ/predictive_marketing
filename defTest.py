# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
from itertools import izip, islice, product
import scipy.sparse as sps

from random import randint


def index_of_max(mtx,row_index):

	row = mtx[row_index,:].todense()

	print "row: " , row

	print "sum: " , np.sum(row)

	print "len: " , np.shape(row)[1]

	print "row[0]: " , row[0,0]

	if np.sum(row) == 0:
		return -1
	elif np.sum(row) / np.shape(row)[1] == row[0,0]:
		return -2
	else:
		return np.argmax(row)


row = [0,0,1,1,2,2]

col = [0,1,0,1,0,1]

f = [0,5,0,0,3,3]

# Duplicate entries are summed together

# Create a sparse matrix in 'coo' format with # rows = (states^order) and # cols = states 

mtx = sps.coo_matrix((f, (row, col)), shape=(3, 2))

mtx = mtx.tocsr()

print mtx.todense()
print index_of_max(mtx,0)
print index_of_max(mtx,1)
print index_of_max(mtx,2)