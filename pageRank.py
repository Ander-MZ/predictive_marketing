# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import numpy as np
import sys, getopt
import networkx as nx
import matplotlib.pyplot as plt

G=nx.DiGraph()

elist=[('a','b',5.0),('b','c',3.0),('a','c',1.0),('c','d',7.3),('b','a',3.0),('d','b',1.0),('d','c',9.0)]

G.add_weighted_edges_from(elist)

pos = nx.circular_layout(G)

edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])

nx.write_dot(G,'graph.dot')

# nx.draw(G,pos=pos,with_labels=True)

# nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)

# plt.show()