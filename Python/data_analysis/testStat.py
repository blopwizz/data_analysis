# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 21:07:41 2017

@author: Stephane
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stat
import random as r
import math


A =[]
B =[]
T = np.arange(0, 1000, 20)

for t in T:
    A.append(3*math.cos(t))
    B.append(math.cos(10*t))
    
R = stat.spearmanr(A, B)[0]
    
plt.clf()
plt.plot(T, A)
plt.plot(T, B)
plt.xlabel('cos with different phase, spearman r='+ str(R))
plt.savefig('cos with different phase')
   
print(r)
