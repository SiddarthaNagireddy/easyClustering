'''
Created on May 13, 2015

@author: sid.reddy
'''
import numpy as np
import os
from fuzzywuzzy import fuzz
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer

class dbScanAlgo():
    
    def __init__(self,filePath,epsilon=0.17,distanceMetric='levenstein'):
        self.filePath = filePath
        self.epsilon = epsilon
        if not os.path.exists('tmp/'):
            os.makedirs('tmp/')
        self.result = open('tmp/result-%s'%self.getFileName(),'w')
        self.dMetric = distanceMetric
    
    ''' Return file name '''
    
    def getFileName(self):
        return self.filePath.split('/')[-1]
    
    ''' Levenstein's Distance '''
   
    def compute_dist(self,str1,str2):
        return 1.0 - (0.01 * fuzz.ratio(str1, str2))
    
    ''' Fit the algorithm '''
    
    def dbscan_algo(self,cluster,X=None):
        
        if self.dMetric=='levenstein':
            clust = DBSCAN(eps=self.epsilon,min_samples=1,metric="precomputed")
            clust.fit(X)
        else:
            vectorizer = TfidfVectorizer().fit_transform(cluster)
            dataX = TfidfTransformer(norm='l1',smooth_idf=True,use_idf=True,sublinear_tf=False).fit_transform(vectorizer)
            clust = DBSCAN(eps=self.epsilon,metric="cosine",min_samples=3,algorithm='brute')
            clust.fit(dataX)
        
        companyNames = cluster
        
        preds = clust.labels_
        clabels = np.unique(preds)
        for i in range(clabels.shape[0]):
            if clabels[i] < 0:
                continue
            cmem_ids = np.where(preds==clabels[i])[0]
            cmembers = []
            for cmem_id in cmem_ids:
                cmembers.append(companyNames[cmem_id])
            clusteritems = ",".join(cmembers)
            print clusteritems
            if len(cmem_ids) > 1:
                self.result.write("Clustered: %s"%clusteritems)
                self.result.write('\n')
    
    ''' Construct a matrix '''
    
    def distance_matrix(self,cluster):
        X = np.zeros((len(cluster),len(cluster)))
        for i in range(len(cluster)):
            if i > 0 and i % 10 == 0:
                print "Processed %d/%d rows of data"% (i,X.shape[0])
            for j in range(len(cluster)):
                if X[i,j] == 0.0:
                    X[i,j] = self.compute_dist(cluster[i],cluster[j])
                    X[j,i] = X[i,j]
        ''' Apply cluster algorithm '''
        self.dbscan_algo(cluster, X)
    
    ''' Initiator '''
    
    def start(self,blocking=False):
        if blocking:
            fileName = 'tmp/block-%s'%self.getFileName()
        else:
            fileName = self.getFileName()
        
        with open(fileName,'r') as fd:
            for line in fd:
                line = line.strip('[').strip(']').strip("'").strip('\n')
                cluster = line.split(',')
                # print cluster
                if self.dMetric == 'levenstein':
                    try:
                        self.distance_matrix(cluster)
                    except:
                        print('Unicode Decode Error! skipping block')
                else: 
                    dbScanAlgo(cluster)

        fd.close()
        self.result.close()