'''
Created on Jun 10, 2015

@author: sid.reddy
'''

import nltk
import string
from operator import itemgetter
from nltk.corpus import stopwords
import os

class dataCleansing():
    
    def __init__(self,filePath):
        self.table = string.maketrans("","")
        self.freqDist = nltk.FreqDist()
        self.stop = stopwords.words('english')
        self.filePath = filePath
    
    ''' Return file name '''
        
    def getFileName(self):
        return self.filePath.split('/')[-1]
    
    ''' Cleans up data and outputs it to temp
        folder for further processing '''
   
    def cleanse(self,boolFDist=False,freqThreshold=0,removePunct = True,removeDigits = False):
        
        ''' Check if temp folder exists; if not create it '''
        if not os.path.exists('tmp/'):
            os.makedirs('tmp/')
        
        fw = open('tmp/cleaned-%s'%self.getFileName(),'w')   
        
        count = 0
        with open(self.filePath,'r') as fd:
            for companyName in fd:
                count += 1
                if count % 1000 == 0:
                    print('Processed %d records'%count)
                normalisedName = companyName.lower().strip()
                
                ''' Ignore Spaces '''
                if len(normalisedName) == 0:
                    continue
                
                if removePunct:
                    normalisedName = normalisedName.translate(self.table,string.punctuation)
                
                if removeDigits:
                    normalisedName = normalisedName.translate(self.table,string.digits)
                
                fw.write(normalisedName+'\n')
                
                if boolFDist:
                    words = nltk.word_tokenize(normalisedName)
                    words = [word for word in words if word not in self.stop]
                    for word in words:
                        self.freqDist[word] += 1
                    wd = open('tmp/freqDist-%s'%self.getFileName(),'w')
                    for k,v in sorted(self.freqDist.items(),key=itemgetter(1),reverse=True):
                        if v > freqThreshold:
                            wd.write("%s\t%d\n"%(k,v))
                    wd.close()
        fd.close()
        fw.close()