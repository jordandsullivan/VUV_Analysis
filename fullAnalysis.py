#!bin/python
import sys
import os
import toolsFullAnalysis as tools
import ROOT
import SpectraTools as ST
import pandas as pd
import matplotlib.pyplot as plt

inputss = sys.argv
dataSets = inputss[1:]

# Pretend this is the input from the user on the commandline
pathToData = '/Users/chrisbenson/Documents/Research/VUV/Data/RunData/'
pathToResults = '/Users/chrisbenson/Documents/Research/VUV/Data/RunDataResults/'

listOfSpectra = []
listOfCurrent = []

for dataNum in dataSets:
	print '\n\n'
	print 'Processing Data in Run Set '+str(dataNum)
	
	tempDir = pathToData+'/Run'+dataNum+'/'
	savePath = pathToResults+'/Run'+dataNum+'/'
	if not os.path.exists(savePath):
		os.makedirs(savePath)
	
	dirContents = os.listdir(tempDir)

	newDirContents = []
	for item in dirContents:
		if ('Notes' in item) and ('.txt' in item):
			continue
		newDirContents.append(item)
			
	# This is the test for spectrum data
	if 'Dark_00.txt' in newDirContents:
		print 'Run '+str(dataNum)+' is being analyzed like a spectrum run!\n' 
		spect1 = tools.spectrum(tempDir,savePath)
		spect1.writeHistos()
		listOfSpectra.append(spect1)
		print '\n'
		continue
	
	# This is the test for current data
	if ('nm' in newDirContents[0]) or ('nm' in newDirContents[1]):
		print 'Run '+str(dataNum)+' is being analyzed like a current run!\n' 
		curr1 = tools.efficency(tempDir,savePath)
		curr1.rawDataToTextFile()
		curr1.rawAndDarkCurrentedCurrentPlots()
		curr1.allCurrentPlotsTogether()
		listOfCurrent.append(curr1)
		
		print '\n'
		continue
		
		
