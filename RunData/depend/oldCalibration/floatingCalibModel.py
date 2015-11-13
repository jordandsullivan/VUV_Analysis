import matplotlib.pyplot as plt
import csv
import numpy as np


##### Trying to model a linearlly floating calibration.

# Extract calibraiton data sets from 2008 and 2014
pathToCalData = '/Users/chrisbenson/Documents/Research/VUV/Data/RunData/depend/oldCalibration/NIST_Cals/'
calFiles = ['NIST_photodiode_calibration_2008.csv','2014_NIST_photodiode_calibration.csv']
legendLabels = ['2008 Low NIST','2014 Low NIST']

wavelengths = []
responsivity = []
uncert = []
qunatum_eff = []
relUncert = []

for fileNum in range(len(calFiles)):
	tempWave = []
	tempResp = []
	tempUncert = []
	tempQE = []
	tempRelUncert = []
	with open(pathToCalData+calFiles[fileNum],'r') as csvfile:
		calreader = csv.reader(csvfile,delimiter=',')
		for index,row in enumerate(calreader):
			if index == 0:
				continue
			if fileNum == 2:
				tempWave.append(float(row[0]))
				tempResp.append(float(row[1]))
				tempUncert.append(float(row[1])*0.01*float(row[2]))
				tempQE.append(np.nan)
			else:
				tempWave.append(float(row[0]))
				tempResp.append(float(row[1]))
				tempUncert.append(float(row[1])*0.01*float(row[3]))
				tempQE.append(float(row[2]))
				tempRelUncert.append(float(row[3]))
	wavelengths.append(tempWave)
	responsivity.append(tempResp)
	uncert.append(tempUncert)
	qunatum_eff.append(tempQE)
	relUncert.append(tempRelUncert)
	
#####  Keep the data we want

waveSet = []
dataSet = []
dataUncert = []
relUncertSub = []

for setNum in range(len(wavelengths)):
	tempWave = []
	tempData = []
	tempUncert = []
	tempRelUncert = []
	for index,val in enumerate(wavelengths[setNum]):
		if val >= 80.0:
			tempWave.append(val)
			tempData.append(responsivity[setNum][index])
			tempUncert.append(uncert[setNum][index])
			tempRelUncert.append(relUncert[setNum][index])
	waveSet.append(tempWave)
	dataSet.append(tempData)
	dataUncert.append(tempUncert)
	relUncertSub.append(tempUncert)
	
		
#### Determine the annual rate of degradation at each wavelength by comparing calibration curves
deltaYears = 5.5 # Number of years between calibrations
# 2008 Calibration date: 8/2008
# 2012 Calibration date: 3/2012

absRate = [] ### Difference will be 2014 - 2008 vals
relativeRate = []
for index in range(len(waveSet[0])):
	absRate.append((dataSet[1][index]-dataSet[0][index])/deltaYears)
	relativeRate.append(absRate[-1]/dataSet[0][index]*100)
	
relRateFig = plt.figure()
relRateAx = relRateFig.add_subplot(111)
relRateAx.plot(waveSet[0],relativeRate)
relRateAx.set_xlabel('Wavelength[nm]')
relRateAx.set_ylabel('Annual Relative Change in Responsitivy (Linear Model) [%]')

###### Vectors over time
# Vic's date of data acquisition for publication: 10/14/2010
# dataDeltaT = float(2+2/12.0)
dataDeltaT = 5.5*1.0
# dataDeltaT=5.5
asymmetricCurve = True

multiplierVector = [1.0]*len(waveSet[0])
for index,wave in enumerate(waveSet[0]):
	if wave >= 210 and wave < 225:
		multiplierVector[index] = 2.0
	elif wave >= 225:
		multiplierVector[index] = 3.0
# 	elif wave >=140 and wave <= 160:
# 		multiplierVector[index] = 1.5
# 	elif wave >=135 and wave <140:
# 		multiplierVector[index] = 1.25

corrected_Cal = []
for index in range(len(waveSet[0])):
	corrected_Cal.append(dataSet[0][index] + absRate[index]*dataDeltaT*multiplierVector[index])
	
## Now plot all of the calibration curves on one plot
figCals = plt.figure(facecolor='white')
axCals = figCals.add_subplot(111)
axCals.errorbar(waveSet[0],dataSet[0],yerr=dataUncert[0],label='2008 Calib')
axCals.errorbar(waveSet[1],dataSet[1],yerr=dataUncert[1],label='2014 Calib')
axCals.errorbar(waveSet[0],corrected_Cal,yerr=dataUncert[0],label='Modified Calib')
axCals.set_xlabel('Wavelength [nm]')
axCals.set_ylabel('Absolute Responsivity [A/W]')
axCals.legend()

figCals.show()

#### Write out to a csv file
masterString = 'Wavelength [nm], Absolute Responsivity [A/W], Quantum Efficiency [electron/photon], Relative Uncertainty [%]\n'
for index,val in enumerate(waveSet[0]):
	masterString += str(float(val))+','+str(float(corrected_Cal[index]))+','+str(float(1.0))+','+str(float(relUncertSub[0][index]))+'\n'
	
calbration_file_name = './test1.csv'
csvFileOut = open(calbration_file_name,'w')
csvFileOut.write(masterString)
csvFileOut.close()

