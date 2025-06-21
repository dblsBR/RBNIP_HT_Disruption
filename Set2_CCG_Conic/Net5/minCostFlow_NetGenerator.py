# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 11:26:04 2025

@author: Daniel
"""

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

from minCostFlow import*


def minCostFlow_Network (network, costVector):
    
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
                
    op = {}
    
    for i, j in G.edges:
        if G.edges[i,j]['special'] == 1:
            op[i,j] = random.randint(1,10); #-1;
        else:
            op[i,j] = random.randint(1,10);
    
    nx.set_edge_attributes(G, op, "op_cost");
    
    G.edges[s,t]["op_cost"] = 1000; #0;
    
    TotalDemand = 0;
    Demand = {};
    
    for i in G.nodes:
        if G.has_edge(i, t) and i != s:
            Demand[i] = 0;
            TotalDemand += G.edges[i,t]["capacity"];
        else:
            Demand[i] = 0;
    
    # Demand[s] = 0;
    # Demand[t] = 0;    
    
    Demand[s] = TotalDemand;
    Demand[t] = -TotalDemand;
    
    nx.set_node_attributes(G, Demand, "demand");
    
    # for i in G.nodes:
    #     print('Demand node %g: %g' %(i, G.nodes[i]['demand']))
    
    # for i,j in G.edges:
    #     print('Operational Cost (%d, %d) %g' %(i,j, G.edges[i,j]['op_cost']))

    return G, s, t;
    