import rat
import ROOT
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import RootPlotLibs as RPL
import sys
import json

pathToData = '/data/snoplus/home/cbenson/VUV/VUV_Analysis/geoFactorSim/'

fileName = sys.argv[1]

fileIterator = rat.dsreader(pathToData+'data/'+fileName+'.root')

numTracksHist = ROOT.TH1D('numTracks','numTracks',50,0,50)
outgoingDotProdHist = ROOT.TH1D('outDotProd','outDotProd',200,-1,1)
incidentDotProd = ROOT.TH1D('incidentDotProd','incidentDotProd',200,-1,1)
reemissionAngleHist = ROOT.TH1D('angle','angle',200,0,math.pi)

# Some tracking vectors 
secondVertexPoints = []

### geoEffNums
geoEffUV = 0
geoEffVisible = 0

AbsorbedTrackSet = []
UVTrackSet = []

runQuiet = True
pythonPlots = True
debugg = True
keepGoing = True
entryNumber = -1
volumeStr = []
while keepGoing:
    try: 
        tempEntry = fileIterator.next()
        entryNumber += 1
        if entryNumber%10000 == 0 and not runQuiet:
            print 'Entry: '+str(entryNumber)
            if UVHitCount > 0:
                'temp GeoFactor: '+str(float(hitDetector)/float(UVHitCount))

        if debugg and entryNumber > 100000:
            keepGoing = False
            continue
    except:
        keepGoing = False
        continue
   
   ### Now grab onto the track numbers and generate a histogram of number of tracks created.
    tempMC = tempEntry.GetMC()
    numTracksHist.Fill(tempMC.GetMCTrackCount())

    # Get dot product distribution for sets 
    if tempMC.GetMCTrackCount() == 2:
        # take dot product of endpoint moment vector of 1 and 2 to get relative angle of reemission.
        firstTrack = tempMC.GetMCTrack(0)
        numSteps = firstTrack.GetMCTrackStepCount()
        firstVect = {'x':firstTrack.GetMCTrackStep(numSteps-1).GetEndpoint().x() - firstTrack.GetMCTrackStep(numSteps-2).GetEndpoint().x(),\
                'y':firstTrack.GetMCTrackStep(numSteps-1).GetEndpoint().y() - firstTrack.GetMCTrackStep(numSteps-2).GetEndpoint().y(),\
                'z':firstTrack.GetMCTrackStep(numSteps-1).GetEndpoint().z() - firstTrack.GetMCTrackStep(numSteps-2).GetEndpoint().z()}
        firstNorm = math.sqrt(firstVect['x']**2 + firstVect['y']**2 + firstVect['z']**2)
        firstVect['x'] = firstVect['x']/firstNorm
        firstVect['y'] = firstVect['y']/firstNorm
        firstVect['z'] = firstVect['z']/firstNorm
        firstDot = firstVect['x']*1.0 + firstVect['y']*0 + firstVect['z']*0
        incidentDotProd.Fill(firstDot)

        secondTrack = tempMC.GetMCTrack(1)
        secondVect = {'x':secondTrack.GetMCTrackStep(1).GetEndpoint().x() - secondTrack.GetMCTrackStep(0).GetEndpoint().x(),\
                'y':secondTrack.GetMCTrackStep(1).GetEndpoint().y() - secondTrack.GetMCTrackStep(0).GetEndpoint().y(),\
                'z':secondTrack.GetMCTrackStep(1).GetEndpoint().z() - secondTrack.GetMCTrackStep(0).GetEndpoint().z()}
        secondNorm = math.sqrt(secondVect['x']**2 + secondVect['y']**2 + secondVect['z']**2)
        secondVect['x'] = secondVect['x']/secondNorm
        secondVect['y'] = secondVect['y']/secondNorm
        secondVect['z'] = secondVect['z']/secondNorm
        secondDot = secondVect['x']*1.0 + secondVect['y']*0 + secondVect['z']*0
        outgoingDotProdHist.Fill(secondDot)

    ### Now perofmr the counting and optional track storage
    numTracks = tempMC.GetMCTrackCount()
    if numTracks > 1: # This will only count tracks which have at least one reemitted photon
        for iTrack in range(tempMC.GetMCTrackCount()):
            tempTrack = tempMC.GetMCTrack(iTrack)
            if iTrack == 0 and tempTrack.GetMCTrackStep(tempTrack.GetMCTrackStepCount()-1).GetEndpoint().x() > 160.0: # Make sure the last step terminates on sample surface
                geoEffUV += 1
                if pythonPlots and len(UVTrackSet) < 100:
                    stepSet = {'x':[],'y':[],'z':[]}
                    for iStep in range(tempTrack.GetMCTrackStepCount()):
                        tempStep = tempTrack.GetMCTrackStep(iStep)
                        stepSet['x'].append(tempStep.GetEndpoint().x())
                        stepSet['y'].append(tempStep.GetEndpoint().y())
                        stepSet['z'].append(tempStep.GetEndpoint().z())
                    UVTrackSet.append(stepSet)
                continue
    
            if iTrack > 0:
                lastStep = tempTrack.GetMCTrackStep(tempTrack.GetMCTrackStepCount()-1)
                if lastStep.GetVolume() == 'detector_vol_vac':
                    geoEffVisible += 1
                    if pythonPlots and len(AbsorbedTrackSet) < 100:
                        stepSet = {'x':[],'y':[],'z':[]}
                        for iStep in range(tempTrack.GetMCTrackStepCount()):
                            tempStep = tempTrack.GetMCTrackStep(iStep)
                            stepSet['x'].append(tempStep.GetEndpoint().x())
                            stepSet['y'].append(tempStep.GetEndpoint().y())
                            stepSet['z'].append(tempStep.GetEndpoint().z())
                        AbsorbedTrackSet.append(stepSet)
                    break

#AbsorbedTrackSet = []
#UVTrackSet = []

if not runQuiet:
    print 'Geo Factor: '+str(float(geoEffVisible)/float(geoEffUV))

if pythonPlots:
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.set_aspect('equal')
    for line in UVTrackSet:
        tempX = []
        tempY = []
        tempZ = []
        for index in range(len(line['x'])):
            tempX.append(line['x'][index])
            tempY.append(line['y'][index])
            tempZ.append(line['z'][index])
        ax.plot(tempX,tempY,tempZ,color='b')

    # Plot the visible tracks now
    for line in AbsorbedTrackSet:
        tempX = []
        tempY = []
        tempZ = []
        for index in range(len(line['x'])):
            tempX.append(line['x'][index])
            tempY.append(line['y'][index])
            tempZ.append(line['z'][index])
        ax.plot(tempX,tempY,tempZ,color='g')
        ax.scatter(tempX[-1],tempY[-1],tempZ[-1],color='r')
        ax.scatter(tempX[0],tempY[0],tempZ[0],color='b')

    ax.set_xlim3d(left=160)
    ax.set_aspect('equal')
    fig.show()

if not debugg:
    # Save the root histograms first
    rootOutFile = ROOT.TFile(pathToData+'plots/'+fileName+'.root','recreate')
    rootOutFile.WriteTObject(outgoingDotProdHist)
    rootOutFile.WriteTObject(incidentDotProd)
    rootOutFile.WriteTObject(numTracksHist)
    rootOutFile.Close()

    outgoingDotProdHist.Delete()
    incidentDotProd.Delete()
    numTracksHist.Delete()

    # save the results
    tempOutFile = open(pathToData+'plots/'+fileName+'.txt','w+')
    outDict = {'VisibleCount':geoEffVisible,'UVCount':geoEffUV,'geoEff':float(geoEffVisible)/float(geoEffUV)}
    json.dump(outDict,tempOutFile)
    tempOutFile.close()


