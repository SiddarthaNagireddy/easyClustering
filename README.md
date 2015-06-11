## easyClustering
Clustering made easy

As the name suggests this package helps people cluster data easily. As of now it is on a early development stage wherein only limited features have been implemented, this will change with time. 

#### Dependencies:

1. Sklearn
2. FuzzyWuzzy
3. nltk

### Features 

1. Data : Suitable for text data only 
2. Pairwise metrics : 
  * Levenstiens (Use levenstiens in case of shorter strings)
  * cosine (cosine when clustering huge text documents)
3. Blocking : POS tag blocker ( More to come )
  * When dealing with high dimensional data please use this feature. Blocks data based on similar in the text.
  * This will reduce the computation on cluster algorithm with little cost to accuracy. 
  * Keep in mind that there is a high posiblity of documents appearing in multiple buckets.

### Usage: 

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

### Example

Sample TestFile :

active network limited
active network
action for boston community development abcd in
action for boston community development abcd
action for boston community development
action for boston community development inc
bay chevrolet
bay chevrolet corp
bay valley foods llc
bay valley foods
security national automotive acceptance
security national automotive acceptance corporation
security national automotive acceptance snaac

Output :

Clustered:  'active network limited\n', 'active network\n'
Clustered: action for boston community development abcd in\n', 'action for boston community development abcd\n', 'action for boston community development\n', 'action for boston community development inc\n'
Clustered:  'bay chevrolet\n', 'bay chevrolet corp\n'
Clustered:  'bay valley foods llc\n', 'bay valley foods\n'
Clustered:  'security national automotive acceptance\n', 'security national automotive acceptance corporation\n', 'security national automotive acceptance snaac\n'
Clustered:  'bae systems\n', 'bae systems inc\n'

### Stats

Tested on 100 K records.. 
Time Taken : 5min 26Sec
