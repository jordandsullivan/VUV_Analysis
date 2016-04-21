import rat
import ROOT
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dataPath = '~/VUV_Analysis/geoFactorSim/newGeoSim/data/config_31/pos13.root'

fileIterator = rat.dsreader(dataPath)

createPlot = True

rayVect = [[],[],[],[]]
volumeNames = []
detectedTracks = []

for i in range(50000):
    tempEntry = fileIterator.next()
    tempMC = tempEntry.GetMC()
    print i
    for iTrack in range(tempMC.GetMCTrackCount()):
        if iTrack > 3:
            break
        tempTrack = tempMC.GetMCTrack(iTrack)
        tempRayPoints = []
        aDetectedTrack = False
        for iStep in range(tempTrack.GetMCTrackStepCount()):
            tempStep = tempTrack.GetMCTrackStep(iStep)
            if tempStep.GetVolume() not in volumeNames:
                volumeNames.append(tempStep.GetVolume())
            tempDict = {'x':tempStep.GetEndpoint().x(),'y':tempStep.GetEndpoint().y(),'z':tempStep.GetEndpoint().z()}
            if iStep == tempTrack.GetMCTrackStepCount()-1 and tempStep.GetVolume() == 'detector_vol_vac':
                aDetectedTrack = True
            tempRayPoints.append(tempDict)
        if aDetectedTrack:
            detectedTracks.append(tempRayPoints)

       # rayVect[iTrack].append(tempRayPoints)

if createPlot:
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')

    plotNumLimit = 1000
    for setIndex,raySet in enumerate(rayVect):
        for numIndex,line in enumerate(raySet):
            tempX = []
            tempY = []
            tempZ = []
            for row in line:
                tempX.append(row['x'])
                tempY.append(row['y'])
                tempZ.append(row['z'])
            color = 'b'
            if setIndex == 1:
                color = 'r'
            elif setIndex == 2:
                color = 'g'
            ax.plot(tempX,tempY,tempZ,color=color)
            if numIndex > plotNumLimit:
                break

    #fig.show()

figDetect = plt.figure()
axDetect = figDetect.add_subplot(111,projection='3d')

rayCount = 0
for aRay in detectedTracks:
    rayCount += 1
    if rayCount > 3000:
        break
    tempX = []
    tempY = []
    tempZ = []
    for row in aRay:
        tempX.append(row['x'])
        tempY.append(row['y'])
        tempZ.append(row['z'])
    axDetect.plot(tempX,tempY,tempZ,color='b')
figDetect.show()







