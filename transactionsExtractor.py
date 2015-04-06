# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import sys, getopt
import time
import collections
import itertools
import operator
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.etree import ElementTree
from xml.dom import minidom

### =================================================================================

# Store input and output file names
ifile=''
ofile=''
column='com_id'
 
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:c:")
 
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    elif o == '-c':
        column=a
    else:
        print("Usage: %s -i input -o output" % sys.argv[0])

### =================================================================================

def dictionary_to_XML(d):

	top = Element('Data')
	cards = []
	append = cards.append

	for pan, history in d.items():

		card = Element('Card',PAN=pan)
		transactions_list = SubElement(card, "Transactions")

		# For each transaction of the card, create a node and add a tag for each atribute

		for t in history:
			node = SubElement(transactions_list, "T")
			for i in range(len(t)):
				node.set(columns[i],str(t[i]))

		append(card)

	top.extend(cards)
	return top

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

### =================================================================================

types = {'pan':'str',
	  'amount':'float',
	  'mcc':'str',
	  'month':'int',
	  'day':'int',
	  'hour':'int',
	  'min':'int',
	  'dow':'int',
	  'com_id':'str'}

columns = ['amount',
		  'mcc',
		  'month',
		  'day',
		  'hour',
		  'min',
		  'dow',
		  'com_id']


print "\tReading file"

data = np.asarray(pd.read_csv(ifile,dtype=types))

print "\tExtracting transactions"

# Group rows by 'pan' and then adds entry to dictionary for each pan & its 
# associated values listed in chronological order (ascending)

d = collections.defaultdict(list)

for key, grp in itertools.groupby(data, key=operator.itemgetter(0)):
	d[key] = map(operator.itemgetter(range(1,len(types))),grp)

print "\nCreating XML file"

xml_result = dictionary_to_XML(d)

print prettify(xml_result)

print "\nSaving file"

tree = ElementTree.ElementTree(xml_result)

tree.write('../data/output.xml')

# output_file.close



############################################################

















