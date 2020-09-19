#!/usr/bin/env python
from sklearn import metrics
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.feature_extraction import DictVectorizer
#from sklearn.cluster import Ward
from math import ceil
from collections import OrderedDict
import numpy as np
import math
import os
import re
import sys
import argparse
import fnmatch
import shutil
import collections
import glob
import numpy
import matplotlib.pyplot as plt
#class cluster_node:
#   def __init__(self,vec,left=None,right=None,distance=0.0,id=None,count=1):
#        self.left=left
#        self.right=right
#        self.vec=vec
#        self.id=id
#        self.distance=distance
#        self.count=count #only used for weighted average 

#def process_options():    
#    parser = argparse.ArgumentParser(description='parse_counters.py')
#    parser.add_argument('-loadFVFile', action='store', dest='loadFVFile', help='input directory')
#    # parser.add_argument('-bicThreshold', action='store', dest='bicThreshold', help='input directory')    
#    parser.add_argument('-exp', action='store', dest='exp', help='benchmark to pick simulation points')
#    parser.add_argument('-hwconfig', action='store', dest='hwconfig', help='benchmark to pick simulation points')
#    parser.add_argument('-bench', action='store', dest='bench', help='input directory')    
#    return parser

def generate_feature_vector():
    feature_vector=[]
    ipc_list=[]
    instruction_counts=[]
    interval_profile=open('./warp_perf.txt','r')
    for line in interval_profile:
        ipc_list.append(float(line.split(',')[0]))
        instruction_counts.append(int(line.split(',')[1]))
    ipc_avg=np.mean(ipc_list)
    print('MIN_IPC')
    print(min(ipc_list))
    print('MAX_IPC')
    print(max(ipc_list))
    print(ipc_avg)
    instruction_counts_avg=np.mean(instruction_counts)
    print(instruction_counts_avg)
    for i in range(0,len(ipc_list)):
        a=[float(ipc_list[i])/float(ipc_avg),float(instruction_counts[i])/float(instruction_counts_avg)]
        feature_vector.append(a)
    return feature_vector

class Kmeans(object):
    def __init__(self):
        self.labels = []        
        pass

    def GetMinDist(self, X):
        repWarps = [0] * (self.labels.max() - self.labels.min() + 1)
        minDist = [0] * (self.labels.max() - self.labels.min() + 1)
        numUnits = [0] * (self.labels.max() - self.labels.min() + 1)
        
        for i in range(len(X)):
            repWarps[self.labels[i]] = 0
            minDist[self.labels[i]] = 100000
            numUnits[self.labels[i]] = 0
            
        for i in range(len(X)):
            numUnits[self.labels[i]] += 1
            #numUnits[self.labels[i]] += sizes[i]
                        
            if np.linalg.norm(X[i] - self.centroids[self.labels[i]]) < minDist[self.labels[i]]:
                repWarps[self.labels[i]] = i
                minDist[self.labels[i]] = np.linalg.norm(X[i] - self.centroids[self.labels[i]])
 #       print(repWarps)
 #       print(X[repWarps[0]],X[repWarps[1]])
   #     Calculate_dist(self,X,i)
        weights = [float(x) / sum(numUnits) for x in numUnits]
        print(weights)
        return repWarps, weights

    def MergeClusters(self, X):
        pass
    
  #  def Calculate_dist(self, X, center)
  #      accum=0
  #      for i in range(0,len(X)):
  #          accum+=np.linalg.norm(X[i]-X[center])
  #      print(float(accum)/float(len(X)))

    
    def RunMins(self, X, clusterNum):
        ipc_list = [e[0] for e in X]
        print('MIN')
        print(min(ipc_list))
        return [ipc_list.index(min(ipc_list))], [1.00], 0
          
    def RunMaxs(self, X, clusterNum):
        ipc_list = [e[0] for e in X]
        print('MAX')
        print(max(ipc_list))
        return [ipc_list.index(max(ipc_list))], [1.00], 0
    
    def RunKmeans(self, X, clusterNum):        
        X = np.reshape(X, (len(X), 2))
        # X = np.reshape(X, (len(X), 1))

        if len(X) <= 1:
            return 0                                

        k_means = KMeans(init='k-means++', n_clusters=clusterNum)        
        k_means.fit(X)
        self.labels = k_means.labels_            
        self.centroids = k_means.cluster_centers_
        

        print "len", len(self.centroids), clusterNum
        if len(self.centroids) == 2:
            dist = numpy.linalg.norm(self.centroids[0] - self.centroids[1])            
        else:
            dist = 0

        print "dist", dist
        print(len(X))
       # plt.plot(X[:,0],X[:,1],'o')
       # plt.scatter(self.centroids[:,0],self.centroids[:,1],c='black')
       # plt.show() 
        
        # find the closest unit to center in the largest cluster
        repUnits, weights = self.GetMinDist(X)

        # find largest cluster
        # clusterId = numUnits.index(max(numUnits))                 
                                
        #######################
        # This is for weighted
        #######################        
        return repUnits, weights    

                        

        
#########################################################################################
# main function
#########################################################################################
def main():
    X=generate_feature_vector()
    clusterNum=2
      
    # parse arguments
    
    runInstance = Kmeans()        
    runInstance.RunKmeans(X,2)
    #runInstance.RunMins(X,2)
    #runInstance.RunMaxs(X,2)
if __name__ == '__main__':
    main()                    



