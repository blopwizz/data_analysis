# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 19:36:57 2017

@author: Stephane
"""
from matplotlib.delaunay.testfuncs import saddle
from matplotlib.backend_bases import DrawEvent

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 12:09:06 2017

@author: Stephane
"""

import csv
import matplotlib.pyplot as plt
import scipy.stats as stat
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
#############################################################################

awe = [] #awe
amu = [] #amusement 
fea = [] #fear
sad = [] #sadness
exc = [] #excitement
con = [] #contentment
dis = [] #disgust

for k in range(1,11):
    if (k < 10):
        user = '00' + str(k)
    else:
        user = '0' + str(k)
    
    ##############################################################################
    tab = [] #table
    T1 = [] #time from ui
    T2 = [] #time from eeg
    S1 = [] #time in seconds since beginning of the DAY from the UI
    S2 = [] #idem with eeg
    A = [] #arousal from UI
    P = [] #pleasure from UI
    STE = [] #short term excitement from EEG
    LTE = [] #long term excitement from EEG
    EB = [] #engagement/boredom from EEG
    EB_ = [] #average engagement/boredom on the last 3 seconds before ui event
    
    
   
    
    #reading data from UI
    with open('data/'+user+'_ui.csv', 'rt') as ui:
        reader = csv.reader(ui)
        next(reader) #jump the header
        for row in reader:
            T1.append(row[0])
            A.append(float(row[2]))
            P.append(float(row[3]))
            
            if("awe" in row[1]):
                awe.append((float(row[2]), float(row[3])))
            if("amu" in row[1]):
                amu.append((float(row[2]), float(row[3])))
            if("fea" in row[1]):
                fea.append((float(row[2]), float(row[3])))
            if("sad" in row[1]):
                sad.append((float(row[2]), float(row[3])))
            if("exc" in row[1]):
                exc.append((float(row[2]), float(row[3])))
            if("con" in row[1]):
                con.append((float(row[2]), float(row[3])))
            if("dis" in row[1]):
                dis.append((float(row[2]), float(row[3])))
        
        
        
            #print awe
        #dic={}
        #for x in sets:
        #    if x[0] not in dic:
        #     arousal=float(x[1])
        #     valence=float(x[2])
        #     #print(nos)
        #     dic[x[0]]=[price,valence]
        #    else:
        #     arousal=float(x[1])
        #     nos=float(x[2])
        #     dic[x[0]][1]+=valence
        #     dic[x[0]][0]+=arousal
        
        #print(dic) 
        
          
    #reading data from eeg
    with open('data/'+user+'_eeg.csv', 'rt') as eeg:
        reader = csv.reader(eeg)
        next(reader) #jump the header
        for row in reader:
            if(row[0] != 'Time from start'):
                T2.append(row[0])
                STE.append(float(row[16])) 
                LTE.append(float(row[17]))
                EB.append(float(row[18]))
    
    #print T2
    #print STE
    #print LTE
    #print EB
    
    #converting time clock to seconds from the beginning of the DAY
    for t in T1:
         DateAndTime = t.split(' ')
         Clock = DateAndTime[1].split(":")
         sec = int(Clock[0]) * 3600 + int(Clock[1]) * 60 + int(Clock[2])
         S1.append(sec)
         
    #print S1
         
    for t in T2:
         DateAndTime = t.split(' ')
         Clock = DateAndTime[1].split(":")
         h = int(Clock[0])
         m = int(Clock[1])
         s = int(Clock[2])
         #converting 12 fromat to 24 format (all the test were after 10 am)
         if (h < 10):
             h += 12
         sec = h * 3600 + m * 60 + s
         S2.append(sec)
         
    #print S2
         
    #crop eeg data on S1 (UI time)
    #the ten first images are just for training
    #so the real data begin at S1[9] - 3s
    #c = 0
    #while S2[c] <  S1[9] - 3:
    #    c += 1
    #
    #S2 = S2[c:] #from the c th element
    #A = A[c:]
    #P = P[c:]
    
    numPhotoTraining = 9
    #average on the last three seconds before UI event
    
    while True:
        try:
    
            for k in range(numPhotoTraining, len(S1)):
            
                d = 1
            
                tCurrent = S1[k]  #current event time (user submit)
                tPast = S1[k-1]  #last past event time
                tInit = tPast + 1 #init data after the black screen
            
                #definition of time frame for average computation
                if (tCurrent - tPast < d+1):  #quick answer from user (1s black + 3s reflexion)
                    tEnd = tCurrent
                else: 
                    tEnd = tInit + d
            
                #  converting S1 index into S2 index
                i = 0
                while(S2[i]<tInit):
                        i += 1
                        ia = i
                while(S2[i]<tEnd):
                    i+= 1
                    ib = i
                
                EB_.append(sum(EB[ia:ib])/len(EB[ia:ib]))
            
            
            #print EB_
            #print A[9:]
            #print(np.corrcoef(EB_, A[9:]))
            plt.clf()
            plt.plot(S1[9:], A[9:])
            plt.plot(S1[9:], EB_)
            r = stat.spearmanr(A[9:], EB_)[0]
            plt.xlabel('user '+user+ ', Spearman r=' + str(r))
            plt.savefig(user + '_analysis')
            #print r

            #plt.plot(A[9:], EB_, 'ro')
            #plt.axis([0, 1, 0, 1])
#            
#            D = [] #rating duration 
#            for i in range(9, len(S1)):
#                D.append(S1[i]-S1[i-1])
#            print(sum(D)/len(D))
#            
       
            break
        except IndexError: 
            print("IndexError (Data not usable for user " +user + ", ui and eeg not synchronised)")
            print("UI data begins at " + str(T1[0]) + " and ends at " + str(T1[-1]))
            print("EEG data begins at " + str(T2[0]) + " and ends at " + str(T2[-1]))
            break

aweAVG = [sum(y) / len(y) for y in zip(*awe)]
amuAVG = [sum(y) / len(y) for y in zip(*amu)] 
feaAVG = [sum(y) / len(y) for y in zip(*fea)]
sadAVG = [sum(y) / len(y) for y in zip(*sad)]
excAVG = [sum(y) / len(y) for y in zip(*exc)]
conAVG = [sum(y) / len(y) for y in zip(*con)]
disAVG = [sum(y) / len(y) for y in zip(*dis)]
#print aweAVG
#print amuAVG
#print feaAVG
#print sadAVG
#print excAVG
#print conAVG
#print disAVG
    
    
        
        
    
