#!bin/python
import pandas as pd
import matplotlib.pyplot as plt

sets = ['2']

pathToResults = '/Users/chrisbenson/Documents/Research/VUV/Data/RunDataResults/'
pathToConcatPlot = '/Users/chrisbenson/Documents/Research/VUV/Data/ResultPlotter/'+'Set'+str(sets[0])+'/'

# load the notes file
configFile = open(pathToConcatPlot+'Notes.txt','r').read().split('\n')

combineType = 0
runsToCombine = []
listOfLegends = []

for line in configFile:
	if 'type:' in line:
		combineType = line.split(':')[1]
		continue
	elif 'runs:' in line:
		listOfRuns = line.split(':')[1].split(',')
		for item in listOfRuns:
			runsToCombine.append(int(item))
		continue
	elif 'legend:' in line:
		tempList = line.split(':')[1].split(',')
		for item in tempList:
			listOfLegends.append(item)
		continue
		
# Now that we have extracted the run numbers we want to combine from the configuration file, extract the efficiency data!
wavelengthSet = []
effValSet = []
effUncSet = []
for runNum in runsToCombine:
	wavelengths = []
	effVals = []
	effUncert = []
	fileName = pathToResults+'Run'+str(runNum)+'/effData.csv'
	dataFileIn = open(fileName,'r').read().split('\n')
	for line in dataFileIn[1:]:	
		if line == '':
			continue
		tempLine = line.split(',')
		wavelengths.append(float(tempLine[0]))
		effVals.append(float(tempLine[1]))
		effUncert.append(float(tempLine[2]))
	wavelengthSet.append(wavelengths)
	effValSet.append(effVals)
	effUncSet.append(effUncert)
	
# Make the final plot now that we have all of the information!
figOut = plt.figure(facecolor='white')
axOut = figOut.add_subplot(111)
runningMaxWave = 0
for index,wave in enumerate(wavelengthSet):
	if max(wave) > runningMaxWave:
		runningMaxWave = max(wave)
	axOut.errorbar(wave,effValSet[index],yerr=effUncSet[index],xerr=None,label=listOfLegends[index])
axOut.set_xlabel('Wavelength [nm]')
axOut.set_ylabel('Forward Efficiency')
axOut.set_title('Forward Efficiency Comparisions between various TPB samples.')
axOut.set_xlim(left=30,right=runningMaxWave+30)
axOut.legend(loc='best')
		
plt.show()



