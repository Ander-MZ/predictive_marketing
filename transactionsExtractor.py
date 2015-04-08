# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import sys, getopt
import time
import collections
import itertools
import operator
from xml.etree.cElementTree import Element, SubElement, Comment, tostring, ElementTree, ElementPath
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
	  'hour':'int',
	  'dow':'int',
	  'com_id':'str'}

columns = ['AMOUNT',
		  'MCC',
		  'HOUR',
		  'DOW',
		  'COM_ID']


print ">Reading file"

data = np.asarray(pd.read_csv(ifile,dtype=types))

print ">Extracting transactions"

# Group rows by 'pan' and then adds entry to XML tree

progress = 0
top = Element('Data')
cards = []
append = cards.append

for pan, grp in itertools.groupby(data, key=operator.itemgetter(0)):

	history = map(operator.itemgetter(range(1,len(types))),grp)
	progress += 1

	if progress%1000==0:
		sys.stdout.write("\tCurrent progress: %d cards grouped\r" % (progress) )
		sys.stdout.flush()

	card = Element('Card',PAN=pan)
	transactions_list = SubElement(card, "History")

	# For each transaction of the card, create a node and add a tag for each attribute

	for t in history:
		node = SubElement(transactions_list, "T")
		for i in range(len(t)):
			node.set(columns[i],str(t[i]))

	append(card)

sys.stdout.write("\tCurrent progress: %d cards grouped\r\n" % (len(cards)) )
sys.stdout.flush()

top.extend(cards)

#print prettify(xml_result)

print ">Saving file"

tree = ElementTree(top)

tree.write(ofile)

############################################################

















