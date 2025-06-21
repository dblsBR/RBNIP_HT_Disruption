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



def sub1 (G, s, t, budget, gamma, cMin, cMax, k, timeLimit):
    
    print('\n--- Solving Sub 1 ---\n')
   
    
    sub = gp.Model('sub1')
    
    obj = sub.addVar(vtype=GRB.INTEGER, lb = -GRB.INFINITY, ub = GRB.INFINITY, name = 'obj');
    
    c = sub.addVars(G.edges, vtype=GRB.INTEGER, lb = -GRB.INFINITY, ub = GRB.INFINITY, name = 'op_cost');
    
    y = sub.addVars(G.nodes, vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = GRB.INFINITY, name='y');
    w = sub.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = 0, name='w');
    p = sub.addVars(G.edges, vtype=GRB.CONTINUOUS, lb = -GRB.INFINITY, ub = 0, name='p');

    
    # Setting operational costs:   
    random.seed(1);
    
    for i,j in G.edges:
        if j == t:
            if i == s:
                sub.addConstr(c[i,j] == 0);
            else:
                center = random.randint(cMin, cMax);
                # print('(%d,%d) range = [%d,%d]' %(i,j,center-5,center+5));
                sub.addConstr(c[i,j] >= center-5);
                sub.addConstr(c[i,j] <= center+5);
        else:
            sub.addConstr(c[i,j] == 0);
    ###############################################################


    for i,j in G.edges:
        sub.addConstr(p[i,j] + G.edges[i,j]['capacity']*(1 - gamma[i,j]) >= 0);
        
        if G.edges[i,j]['special'] == 1:
            sub.addConstr(y[i] - y[j] + w[i,j] - c[i,j] <= 1);
            
        else:
            sub.addConstr(y[i] - y[j] + w[i,j] - c[i,j] <= 0);
            
    sub.addConstrs(gp.quicksum(p[i,j] for j in G.successors(i))
                  - gp.quicksum(p[j,i] for j in G.predecessors(i))
                  + G.nodes[i]['demand'] == 0 for i in G.nodes);
    
    
    # Integer Objective Value
    sub.addConstr(gp.quicksum(G.nodes[i]['demand']*y[i] for i in G.nodes) 
                                + gp.quicksum(G.edges[i,j]['capacity']*(1 - gamma[i,j])*w[i,j] for i,j in G.edges)
                                + gp.quicksum(c[i,j]*p[i,j] for i,j in G.edges) == obj);
    
    
    sub.setObjective(gp.quicksum(G.nodes[i]['demand']*y[i] for i in G.nodes) 
                                + gp.quicksum(G.edges[i,j]['capacity']*(1 - gamma[i,j])*w[i,j] for i,j in G.edges)
                                + gp.quicksum(c[i,j]*p[i,j] for i,j in G.edges), GRB.MAXIMIZE);
    
    
    
    file = 'LogFile_Sub1_B'+str(budget)+"_"+ str(k)+'.txt'
    
    sub.setParam("NonConvex", 2);
    
    sub.setParam("OutputFlag", 1);
    sub.setParam("LogFile", file);
    sub.setParam("LogToConsole", 0);
    sub.setParam("MIPFocus", 3);
    sub.setParam("Cuts", 3);
    sub.setParam("TimeLimit", timeLimit);
    
    sub.update();
    sub.optimize();
    
        
    UB = 10e8;
    C = {};
    for i,j in G.edges:
        C[i,j] = 0;
    
    if sub.status == 3:
        print('Infeasible!');
        gap = 10e8;

    
    elif sub.status == 4:
        print('Infeasible or Unbounded!');
        gap = 10e8;

        
    elif sub.status == 2:
        print('Solved to optimality!')
        
        for i,j in G.edges:
            C[i,j] = c[i,j].x;
            
        UB = sub.ObjVal;
        gap = 0;
    elif sub.status == 9:
        print('\nReached Time limt!\n')
        
        if sub.SolCount == 0:
            gap = 10e8;
            print('No feasible solution found!')
            return None;

        else:
            print('MIP Gap %g\n' %sub.MIPGap);  
        
            for i,j in G.edges:
                C[i,j] = c[i,j].x;
            
            UB = sub.ObjBound;
            gap = sub.MIPGap;
    else:
        print('Model status: %d' %sub.status);
      
    
    return C, UB, gap;