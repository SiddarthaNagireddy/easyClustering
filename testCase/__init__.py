
''' CLUSTERING 

    DISTANCE METRIC = LEVENSTEIN'S
    ALGORITHM = DBSCAN '''

from dataCleansing import cleanseData
from blocking import blockPOS
from clustering import dbscan

filePath = '~testFile.txt' 

''' Clean the data '''

obj1 = cleanseData.dataCleansing(filePath)
obj1.cleanse(boolFDist=True,freqThreshold=100,removePunct=True,removeDigits=True)

''' Block the data into similar chunks '''

obj2 = blockPOS.blocking(filePath)

''' build a custom stop list '''

obj2.buildStopList(boolFDist=True)

''' Start the POS Tagger '''

obj2.posTag()

''' Start the Blocker '''

obj2.block()

''' Apply dbscan on blocks '''
obj3 = dbscan.dbScanAlgo(filePath,epsilon=0.17,distanceMetric='levenstein')
obj3.start(blocking=True)
