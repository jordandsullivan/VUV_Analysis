#!/bin/python
import rat
import ROOT
import matplotlib.pyplot as plt
#import pandas
from mpl_toolkits.mplot3d import Axes3D

"""
Some things to add:
- Histogram of X vs Z on hits on detector. Give an idea of what the hit distribution is like.
- Wavelength distribution of reemitted photons at TPB and at detector.
- A vector to track how the geometric factor is changeing over counting (with increasing tracks) to check for stability.
 - A plot of tracks. 

"""


class trackSorter:
	def __init__(self,fileName,saveTrack=False,targetType=1):
		## Create a file iterator
		self.fileName = fileName
		fileIter = rat.dsreader(fileName)
		
		# start a loop over all of tree entries breakout of loop if at end.
		keepLooping = True
		entryIndex = -1
		showStartCoords = True
		#self.testFigure = plt.figure()
		#self.ax = self.testFigure.add_subplot(111,projection='3d')
		
		self.caseCount = [0]*9
		self.WLS_Start = []
		self.WLS_End = []
		
		self.checkpointEventCount = []
		self.geometricFactorCheckPoint = []
		self.caseCountCheckpoint = []
		
		self.targetTracks = []
		
		while keepLooping:
			try:
				tempEntry = fileIter.next()
				entryIndex += 1
				#if entryIndex%1000 == 0:
					#print entryIndex
			except:
				keepLooping = False
				continue
		
			tempMC = tempEntry.GetMC()
			
			# Get number of MC tracks and loop over them
			for iTrack in range(tempMC.GetMCTrackCount()):
				tempTrack = tempMC.GetMCTrack(iTrack)
				if showStartCoords == True:
					# This will store the coords or the very first simulated photon step 0, for source tracking.
					tempEndpoint = tempTrack.GetMCTrackStep(0).GetEndpoint()
					if tempEndpoint.x() < 0.0 and tempEndpoint.y() > 0.0:
						self.startCoords = [tempEndpoint.x(),tempEndpoint.y(),tempEndpoint.z()]
						tempEndpoint = False
				
				### Sort that track
				trackResult = self.endPointSorter(tempTrack)
				
				self.caseCount[trackResult] += 1
				
				if trackResult in [4,5,6,7,8]:
					wavelengthResults = self.getTrackStartEndWavelengths(tempTrack)
					self.WLS_Start.append(wavelengthResults[0])
					self.WLS_End.append(wavelengthResults[1])
				
				if trackResult == 8:
					#wavelengthResults = self.getTrackStartEndWavelengths(tempTrack)
					#self.WLSStart.append(wavelengthResults[0])
					coordsToPlot = convertTrackToXYZVect(tempTrack)
					#self.ax.plot(coordsToPlot[0],coordsToPlot[1],coordsToPlot[2])
					#coordsToPlot = convertTrackToEndpoint(tempTrack,0)
					#self.ax.scatter(coordsToPlot[0],coordsToPlot[1],coordsToPlot[2],color='b')
					#coordsToPlot = convertTrackToEndpoint(tempTrack,1)
					#self.ax.scatter(coordsToPlot[0],coordsToPlot[1],coordsToPlot[2],color='r')
					
					
			if entryIndex % 10000 == 0:
				self.checkpointEventCount.append(entryIndex)
				tempCaseCount = self.caseCount[:]
				self.caseCountCheckpoint.append(tempCaseCount)
				
					
		self.printResuts()
					
				
	def endPointSorter(self,tempTrack):
		"Provide a track and function will look at endpoints and perfrom a first pass classification of what the track is. This will be used for storage and analysis decisions down the line."
		numSteps = tempTrack.GetMCTrackStepCount()
		volStart = tempTrack.GetMCTrackStep(0).GetVolume()
		volEnd = tempTrack.GetMCTrackStep(numSteps-1).GetVolume()
		
		## Classify which photon it is for storage and further analysis.
		if volStart == 'monochrom_housing' and volEnd == 'monochrom_housing':
			# This is a photon that didn't make it out of the housing. Not very relevant
			return 1
		elif volStart == 'monochrom_housing' and volEnd == 'shutter_tunnel':
			# This is a photon that made it through the first slit, but died somewhere in the shutter tunnel
			return 2
		elif volStart == 'monochrom_housing' and volEnd == 'tpb_vol_vac':
			# This photon started at the source and made it to the TPB surface.
			return 3
		elif (volStart == 'tpb_vol_vac' or volStart == 'shutter_tunnel') and volEnd == 'tpb_vol_vac':
			# This photon was created in the TPB but then immediately reabsorbed or reflect back to TPB surface and get absorbed.
			return 4
		elif (volStart == 'tpb_vol_vac' or volStart == 'shutter_tunnel') and volEnd == 'sample_vol':
			# This photon was created in the TPB but absorbed in the acrylic substrate
			return 5
		elif (volStart == 'tpb_vol_vac' or volStart == 'shutter_tunnel') and volEnd == 'monochrom_housing':
			# This photon was created in TPB, but then was remitted, went back through slits and absorbed somewhere in the monochromator housing.
			return 6
		elif (volStart == 'tpb_vol_vac' or volStart == 'shutter_tunnel') and volEnd == 'shutter_tunnel':
			# This photon was created in TPB, and absorbed somewhere in the shutter tunnel.
			return 7
		elif (volStart == 'tpb_vol_vac' or volStart == 'shutter_tunnel') and volEnd == 'detector_vol_vac':
			# This photon was remitted by TPB, and traveld to the detector to be absorbed.
			return 8
		else:
			# These are states we missed in planning
			print 'Start Vol: '+volStart+' End Vol: '+volEnd
			return 0
			
	def getTrackStartEndWavelengths(self,tempTrack):
			"""
			Returns the start and end wavelengths for this photon track
			"""
			numSteps = tempTrack.GetMCTrackStepCount()
			startKE = tempTrack.GetMCTrackStep(0).GetKE()
			endKE = tempTrack.GetMCTrackStep(numSteps-1).GetKE()
			
			lambdaStart = 1239.84193/(startKE*10**6)
			lambdaEnd = 1239.84193/(endKE*10**6)
			
			return lambdaStart, lambdaEnd
			
	def printResuts(self):
		print 'Results from:'+str(self.fileName)
		print 'source coords:'+str(self.startCoords)
		print 'track type vect:'+str(self.caseCount)
		print 'caseCountCheckpoint:'+str(self.caseCountCheckpoint)
		
			

def convertTrackToXYZVect(tempTrack):
	x = [] 
	y = []
	z = []
	for i in range(tempTrack.GetMCTrackStepCount()):
		tempTrackStep = tempTrack.GetMCTrackStep(i).GetEndpoint()
		x.append(tempTrackStep.x())
		y.append(tempTrackStep.y())
		z.append(tempTrackStep.z())
	return x,y,z	
	
def convertTrackToEndpoint(tempTrack,end=0):
	tempTrackStep = None
	if end == 0:
		# Want the first point
		tempTrackStep = tempTrack.GetMCTrackStep(0).GetEndpoint()
	else:
		# Want the last point
		numTrackSteps = tempTrack.GetMCTrackStepCount()
		tempTrackStep = tempTrack.GetMCTrackStep(numTrackSteps-1).GetEndpoint()
	return tempTrackStep.x(),tempTrackStep.y(),tempTrackStep.z()
	
	
	
		


