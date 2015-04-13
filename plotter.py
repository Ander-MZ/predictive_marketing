# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math

### =================================================================================

def plot_matrix(m,xpartition,ypartition,title,filename,norm=False):

    # Normalize values between 0 and 1
    if norm:
        cm = m.astype(float)
        for i in range(cm.shape[0]):
            total = cm[i].sum()
            for j in range(cm.shape[1]):
                cm[i,j]=cm[i,j]/total
        m=cm

    if ypartition[0]==0:
    	ypartition[0]=1

    xtags = map(str,xpartition)
    ytags = map(str,ypartition)

    # Set up a colormap:
    #palette = matplotlib.cm.RdYlGn
    palette = matplotlib.cm.jet
    palette.set_under('gray', 1.0)

    plt.matshow(m,vmin=0,vmax=1,cmap=palette)
    plt.title(title+'\n')
    plt.colorbar()
    
    plt.ylabel('Min history')
    plt.xlabel('Max history')
    plt.xticks(range(len(xtags)),xtags)
    plt.yticks(range(len(ytags)),ytags)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
  
    plt.savefig(filename)
    #plt.show()

# Receives a data collection in the form of a Numpy Array

def plot_histogram(data,title,filename,verbose=False):

	data = data[data>=0] # Remove -1 from the 'not found in training' cases

	n = len(data)

	if verbose:
		print "Predictions with precision = 0%% : %.2f %%" %  (100 * len(data[data==0.0]) / n) 
		print "Predictions with precision > 0%% : %.2f %%" %  (100 * len(data[data>0.00]) / n) 
		print "Predictions with precision > 25%% : %.2f %%" % (100 * len(data[data>0.25]) / n) 
		print "Predictions with precision > 50%% : %.2f %%" % (100 * len(data[data>0.50]) / n) 
		print "Predictions with precision > 75%% : %.2f %%" % (100 * len(data[data>0.75]) / n) 

	nx, xbins, ptchs = plt.hist(data, bins=20)
	plt.clf() # Get rid of this histogram since not the one we want.

	nx_frac = nx/len(data) # Each bin divided by total number of objects.
	width = xbins[1] - xbins[0] # Width of each bin.
	x = np.ravel(zip(xbins[:-1], xbins[:-1]+width))
	y = np.ravel(zip(nx_frac,nx_frac))

	plt.plot(x,y)
	plt.fill_between(x, 0, y)
	plt.title(title)
	plt.xlabel("Value")
	plt.ylabel("Frequency")
	plt.savefig(filename)
	#plt.show()