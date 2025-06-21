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

def minCostFlow1 (G, s, t, budget):
    
    
    print('\nSolving min cost interdiction problem to get initial gamma ... \n')
    
    time0 = time.time();
    
    m = gp.Model("MinCost");
    
    gamma = m.addVars(G.edges, vtype=GRB.BINARY);
    
    
    x = m.addVars(G.edges, vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY);
    
    m.addConstr(gp.quicksum(G.edges[i,j]['int_cost']*gamma[i,j] for i,j in G.edges) <= budget);
    
    m.addConstrs(gp.quicksum(x[i,j] for j in G.successors(i)) 
                     - gp.quicksum(x[j,i] for j in G.predecessors(i)) 
                     == G.nodes[i]['demand'] for i in G.nodes);
    
    coef_gamma = {};
    for i,j in G.edges:
        m.addConstr(x[i,j] <= G.edges[i,j]['capacity']*(1-gamma[i,j]));
        coef_gamma[i,j] = random.randint(-2,2);
        
    m.setObjective(gp.quicksum(coef_gamma[i,j]*G.edges[i,j]['capacity']*gamma[i,j] for i,j in G.edges),
                   GRB.MAXIMIZE);
    
    
    
    
    file = 'LogFile_MinCostProblem_B'+str(budget)+'.txt'
    
    m.setParam("OutputFlag", 0);    
    # m.setParam("NonConvex", 2);
    
    m.setParam("OutputFlag", 1);
    m.setParam("LogFile", file);
    m.setParam("LogToConsole", 0);
    m.optimize();
    
    # print('model status: %g' %m.status);
    
    time1 = time.time();
    runTime = round(time1-time0, 2);
    print('\nRun time min cost flow interdiction problem: %g sec\n' %runTime);
    
    Gamma = {};
    for i,j in G.edges:
        Gamma[i,j] = gamma[i,j].x;

        
    return Gamma;