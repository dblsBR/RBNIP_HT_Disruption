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

from robustNetwork import*
from sub0 import *
from sub1 import *


cMax = -10;
cMin = -30;

Nets = [1];
Budget = [8,10,12];
Rate = [1];


timeLimit = 7200;




for n in Nets:
    
    network = "Net5.csv";
    
    Summary = "Summary_Results_" +network;
    file = open(Summary, "w");
    file.write('Budget,UB,Gap,Time\n');
    file.close(); 
    
    G, s, t = robustNetwork(network);
    
    for rate in Rate:
        G1 = G.copy();
        
        for i in G1.successors(s):
                G1.edges[s,i]['capacity'] = math.floor(rate*G.edges[s,i]['capacity']);
        
    
        for budget in Budget:
            print('\nBudget %g\n' %budget);          

            Traffickers = [];
            Bottoms = [];
            Victims = [];
            
            for i,j in G1.edges:
                if G1.edges[i,j]['trafficker'] == 1:
                    Traffickers.append(j);
                elif G1.edges[i,j]['bottom'] == 1:
                    Bottoms.append(j);
                elif G1.edges[i,j]['victim'] == 1:
                    Victims.append(j);
            
            n_Traf = len(Traffickers);
            
            Gamma = {};
            
            Arr=[];
            fileName = "GammaVectors_Net" + str(len(Traffickers)) + "_B"+str(budget)+".txt" 
            with open(fileName, "r") as file2:
                ctr = 0;
                for line in file2:
                    Gamma[ctr] = {};
                    line = line[:-1]
                    line = line.replace(" ", "");
                    line = line.replace("-", "");
                    for j in line:
                        Arr.append(int(j));
                    
                    for i,j in G1.edges:
                        Gamma[ctr][i,j] = Arr.pop(0);
                    ctr += 1;
            
            gap = [];

            C = {};
            UB = [];
            
            c0 = {};
            c1 = {};
            
            ub0 = 0;
            ub1 = 0;
            
            gap0 = 0;
            gap1 = 0;
            
            
            print('\nInterdiction:')
            for k in Gamma.keys():
                
                for i,j in G.edges:
                    if Gamma[k][i,j] > 0.0001:
                        print('(%d,%d)' %(i,j))
                print('\n')
                
                now = datetime.now();
                start = time.time();
                
                c0, ub0, gap0 = sub0 (G, s, t, budget, Gamma[k], cMin, cMax, k, timeLimit);
                c1, ub1, gap1 = sub1 (G, s, t, budget, Gamma[k], cMin, cMax, k, timeLimit);
                
                end = time.time();
                runTime = round(end-start, 2);
                
                print('\nRuntime: %g sec\n' %runTime);
                
                C[k] = {};
                
                print('\nUB0 = %d, UB1 = %d\n' %(ub0,ub1))
                
                if ub0 > ub1:
                    C[k] = c0;
                    UB.append(ub0);
                    gap.append(gap0);
                else:
                    C[k] = c1;
                    UB.append(ub1);
                    gap.append(gap1);
                    
                fileResults = 'Results_Net' + str(len(Traffickers)) + '_B' +str(budget)+'_S'+str(k)+'.txt';
                
                with open(fileResults, "w") as file:
                    file.write('Instance executed at: %s \n' %now.strftime("%c"));
                    
                    file.write('\nRuntime: %g\n' %runTime);
                    
                    Gap = 100*round(gap[k],4);
                    
                    file.write('\nMIP Gap: %g%s\n' %(Gap,  str(chr(37))));
                    
                    file.write('\nInterdiction Vectors\n')
                    for i,j in G1.edges:
                        if Gamma[k][i,j] > 0.0001:
                            file.write('(%d,%d)\n' %(i,j));
                    file.write('\n\n')
                    
                    file.write('Cost Vectors\n')
                    for i,j in G1.edges:
                        file.write('%g ' %C[k][i,j]);
                    file.write('\n\n')
                    
                    ub = round(UB[k],2)
                    file.write('Upper Bound (sub objective): %g \n' %ub);
                
                write = [budget,ub,Gap,runTime];
                with open(Summary, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile);
                    csvwriter.writerow(write);
                    csvfile.close();

        