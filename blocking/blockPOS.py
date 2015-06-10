'''
Created on Jun 10, 2015

@author: sid.reddy
'''

'''
Created on May 13, 2015

@author: sid.reddy
'''
from nltk import pos_tag
from nltk.corpus import stopwords
from collections import defaultdict
import nltk

class blocking():
    
    def __init__(self,filePath):
        self.filePath = filePath
        self.diction = defaultdict()
    
    ''' Return file name '''
        
    def getFileName(self):
        return self.filePath.split('/')[-1]
    
    ''' Build a list of stop words from FreqDist '''
    
    def buildStopList(self,boolFDist=False):
        self.stop = stopwords.words('english')
        
        ''' Add custom words to the stopword list'''
        if boolFDist:
            with open('tmp/freqDist-%s'%self.getFileName(),'r') as fd:
                for line in fd:
                    self.stop.append(line.split('\t')[0])
            print('Done generating a custom stop list')
            fd.close()
        return self.stop
    
    ''' PosTag words and push to a dictionary '''    
    
    def posTag(self):
        count = 0
        with open('tmp/cleaned-%s'%self.getFileName(),'r') as fd:
            for line in fd:
                count += 1
                if count % 1000 == 0:
                    print('Processed %d records'%count) 
                try:
                    words = [word for word in nltk.word_tokenize(line) if word not in self.stop]
                    properNouns = [word for word,pos in pos_tag(words) if 'NN' in pos]
                except:
                    properNouns = []
                    print('ascii error')
                self.diction[line] = properNouns
        fd.close()
        
    def block(self):
        cluster = dict()
        print('Blocking has started')
        count = 0
        for x in self.diction:
            for y in self.diction[x]:
                if y in cluster:
                    cluster[y].append(x)
                else:
                    cluster[y] = [x]
                    print('Block - %d created'%count)
                    count += 1
        
        cl = open('tmp/block-%s'%self.getFileName(),'w')
        for clust in cluster:
            lists = str(cluster[clust])
            cl.write(lists+'\n')
        cl.close()
