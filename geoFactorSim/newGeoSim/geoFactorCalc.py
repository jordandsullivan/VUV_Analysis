import json
import sys

cmdArgs = sys.argv

dataSet = 'config_'+cmdArgs[1]
pathToData = './data/'+dataSet+'/geoCalcs/'

numFiles = 25

fileVect = range(1,numFiles+1)

masterDataVect = {'UVCount':0,'VisibleCount':0}

for fileNum in fileVect:
    try:
        tempFile = open(pathToData+'pos'+str(fileNum)+'.json','r').read()
    except:
        continue
    tempData = json.loads(tempFile)

    masterDataVect['UVCount'] += tempData['UVCount']
    masterDataVect['VisibleCount'] += tempData['VisibleCount']


print masterDataVect
print 'GeoFactor = '+str(float(masterDataVect['VisibleCount'])/float(masterDataVect['UVCount']))
