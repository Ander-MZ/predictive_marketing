# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import collections
import sys, getopt
import math

### =================================================================================

# Store input and output file names
ifile=''
ofile=''
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================

def read_file():

	pan_test = collections.defaultdict(list)

	distinct = []
	top = 0

	with open(ifile) as f:
		for row in f:
			t = row.strip().split(",")
			d =  len(set(t[1:]))
			distinct.append(d)
			if d > top:
				top=d

	print top
	return distinct

def write_file(data):

	output_file = open(ofile,'w')
	write = output_file.write

	for row in data:
		write("%s%s" % (row,"\n"))

	output_file.close()

data = read_file()

write_file(data)


