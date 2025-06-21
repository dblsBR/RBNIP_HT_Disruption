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


def minCostFlow_Network (G1, s, t, costVector):
    
    G = G1.copy();
    
    G.add_edge(s,t,
               capacity = 10000,
               int_cost = 10000,
               special = 0,
               trafficker = 0, 
               bottom = 0,
               victim = 0);
                
    op = {}
    
    for i, j in G.edges:
        op[i,j] = costVector[i,j]; 
    
    nx.set_edge_attributes(G, op, "op_cost");
    
    # G.edges[s,t]["op_cost"] = 1000; #0;
    
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

    return G;
    