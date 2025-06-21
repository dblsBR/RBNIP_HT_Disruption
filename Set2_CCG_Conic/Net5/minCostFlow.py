# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:02:32 2025

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

def minCostFlow (G, s, t, budget):
    
    
    print('\nSolving min cost interdiction problem to get initial gamma ... \n')
    
    time0 = time.time();
    
    m = gp.Model("MinCost");
    
    gamma = m.addVars(G.edges, vtype=GRB.BINARY);
    alpha = m.addVars(G.nodes, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY);
    theta = m.addVars(G.edges, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=0);
    
    x = m.addVars(G.edges, vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY);
    
    m.addConstr(gp.quicksum(G.edges[i,j]['int_cost']*gamma[i,j] for i,j in G.edges) <= budget);
                
    for i,j in G.edges:
        m.addConstr(alpha[i] - alpha[j] + theta[i,j] <= G.edges[i,j]['op_cost']);
        
    m.setObjective(gp.quicksum(G.nodes[i]['demand']*alpha[i] for i in G.nodes) 
                   + gp.quicksum(G.edges[i,j]['capacity']*(1 - gamma[i,j])*theta[i,j] for i,j in G.edges),
                   GRB.MAXIMIZE);
    
    m.setParam("OutputFlag", 0);
    m.optimize();
    
    # print('model status: %g' %m.status);
    
    time1 = time.time();
    runTime = round(time1-time0, 2);
    print('\nRun time min cost flow interdiction problem: %g sec\n' %runTime);
    
    Gamma = {};
    for i,j in G.edges:
        Gamma[i,j] = gamma[i,j].x;

        
    return Gamma;
    
    
