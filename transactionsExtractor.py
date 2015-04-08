# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import sys, getopt
import time
import collections
import itertools
import operator
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree, ElementPath
from xml.dom import minidom

### This class takes a list of transactions sorted by date, and then parses it
### into a XML file with the following structure:

# <Data>
#	<Card PAN="pan">
#		<Transactions>		
#			<T AMOUNT="amount" MCC="mcc" COM_ID="com_id" MONTH="month" DAY="day" HOUR="hour" MIN="min" DOW="dow" />
#			...
#			...
#			<T AMOUNT="amount" MCC="mcc" COM_ID="com_id" MONTH="month" DAY="day" HOUR="hour" MIN="min" DOW="dow" />
#		</Transactions>
#	</Card>
# </Data>

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

def dictionary_to_XML(d):

	top = Element('Data')
	cards = []
	append = cards.append

	progress = 0

	for pan, history in d.items():

		progress += 1

		if progress%1000==0:
			sys.stdout.write("\tCurrent progress: %.2f %% of cards parsed\r" % (100*progress/len(d)) )
			sys.stdout.flush()

		card = Element('Card',PAN=pan)
		transactions_list = SubElement(card, "Transactions")

		# For each transaction of the card, create a node and add a tag for each attribute

		for t in history:
			node = SubElement(transactions_list, "T")
			for i in range(len(t)):
				node.set(columns[i],str(t[i]))

		append(card)

	sys.stdout.write("\tCurrent progress: %.2f %% of cards parsed\r\n" % (100.00) )
	sys.stdout.flush()

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

columns = ['AMOUNT',
		  'MCC',
		  'MONTH',
		  'DAY',
		  'HOUR',
		  'MIN',
		  'DOW',
		  'COM_ID']


print ">Reading file"

data = np.asarray(pd.read_csv(ifile,dtype=types))

print ">Extracting transactions"

# Group rows by 'pan' and then adds entry to dictionary for each pan & its 
# associated values listed in chronological order (ascending)

d = collections.defaultdict(list)

progress = 0

for key, grp in itertools.groupby(data, key=operator.itemgetter(0)):

	progress += 1

	if progress%1000==0:
		sys.stdout.write("\tCurrent progress: %.2f %% of cards grouped\r" % (100*progress/len(data)) )
		sys.stdout.flush()

	d[key] = map(operator.itemgetter(range(1,len(types))),grp)

sys.stdout.write("\tCurrent progress: %.2f %% of cards grouped\r\n" % (100.00) )
sys.stdout.flush()

print ">Creating XML file"

xml_result = dictionary_to_XML(d)

#print prettify(xml_result)

print ">Saving file"

tree = ElementTree(xml_result)

tree.write(ofile)

############################################################

















