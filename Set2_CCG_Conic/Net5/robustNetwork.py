'''
Code: robustNetwork
Author: Daniel B Lopes da Silva
Date: 5/26/2025

Purpose: to adapt the human trafficking networks to be used with the 
robust min-cost flow network interdiction problem.

This code:
(1) reads a csv file containing a human trafficking network;
(2) replaces the returning (t,s) arc from the maximum flow problem by
a (s,t) arc to ensure feasibility of the min-cost flow problem; and
(3) sets the demand/supply values for the nodes.

'''

import networkx as nx;
import gurobipy as gp;
from gurobipy import GRB;
import sys;
import time;
from datetime import datetime;
import csv;
import pandas as pd;
import math;
import random;
import numpy;
from numpy import *  


def robustNetwork (network):
    
    with open(network, newline='') as f:
        reader = csv.reader(f);
        row1 = next(reader);
        
        s = int(row1[0]);     
        t = int(row1[1]); 
        
        G = nx.DiGraph();
        data = pd.read_csv(network, skiprows=1, header=None);
        n_edge = len(data.index+1);
        
        for i in range(n_edge):
            G.add_edge(data.iat[i,0], data.iat[i,1],
                       capacity = data.iat[i,2],
                       int_cost = data.iat[i,3],
                       special = data.iat[i,4],
                       trafficker = data.iat[i,5], 
                       bottom=data.iat[i,6],
                       victim=data.iat[i,7]);
    
    
    G.remove_edge(t,s);
    G.add_edge(s,t,
               capacity = 10000,
               int_cost = 10000,
               special = 0,
               trafficker = 0, 
               bottom = 0,
               victim = 0);
                
    
    totalCap = 0;
    for i,j in G.edges:
        if j == t and i != s:
            totalCap += G.edges[i,j]['capacity'];
    
    # demand = random.randint(0.6*totalCap, 0.8*totalCap);
    
    demand = math.floor(0.7*totalCap);
    
    TotalDemand = 0;
    Demand = {};
    
    for i in G.nodes:
        if i != s and i != t:
            Demand[i] = 0;
        
    Demand[s] = demand;
    Demand[t] = -demand; # math.floor(0.6*demand);
    
    nx.set_node_attributes(G, Demand, 'demand');
    
    # for i in G.nodes:
    #     print('Demand node %g: %g' %(i, G.nodes[i]['demand']))
    
    # for i,j in G.edges:
    #     print('Operational Cost (%d, %d) %g' %(i,j, G.edges[i,j]['op_cost']))

    return G, s, t;
    