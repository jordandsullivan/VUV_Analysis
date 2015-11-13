#!/bin/python
import rat
import ROOT
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

pathToData = '/Users/chrisbenson/Documents/Research/VUV/RATSims/simData/'
fileName = 'test.root'

fileIterator = rat.dsreader(pathToData+fileName)

dataVect = []
housingPoints = []

keepGoing = True
while keepGoing:
	try:
		tempEntry = fileIterator.next()
	except:
		keepGoing = False
		continue
	
	tempMC = tempEntry.GetMC()
	for trackIndex in range(tempMC.GetMCTrackCount()):
		tempTrack = tempMC.GetMCTrack(trackIndex)
		tempData = []
		trigStore = False
		monoHousStore = False
		for j in range(tempTrack.GetMCTrackStepCount()):
			tempStep = tempTrack.GetMCTrackStep(j)
			tempCoords = tempStep.GetEndpoint()
			tempData.append([tempCoords.x(),tempCoords.y(),tempCoords.z()])
			print tempStep.GetVolume()
			if 'shutter_tunnel' in tempStep.GetVolume():
				trigStore = True
			if 'shutter_tunnel' in tempStep.GetVolume():
				monoHousStore = True
		if trigStore == True:
			dataVect.append(tempData)
		
		if monoHousStore == True and len(housingPoints)<1000:
			housingPoints.append(tempData)
			
		
print 'plotting now!'
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
for row in dataVect:
	x = []
	y = []
	z = []
	for cordSet in row:
		x.append(cordSet[0])
		y.append(cordSet[1])
		z.append(cordSet[2])
	ax.plot(xs=x,ys=y,zs=z)
	
for row in housingPoints:
	x = []
	y = []
	z = []
	for cordSet in row:
		x.append(cordSet[0])
		y.append(cordSet[1])
		z.append(cordSet[2])
	ax.scatter(xs=x[1:],ys=y[1:],zs=z[1:])

			
plt.show()


