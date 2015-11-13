import matplotlib.pyplot as plt

			
def parseFile(fullFileName):
	tempFile = open(fullFileName).read().split('\n')[1].split(',')[2:4]
	meanVal = float(tempFile[0])
	stdev = float(tempFile[1])
	return meanVal, stdev

pathToData = '/Users/chrisbenson/Documents/Research/VUV/Data/RunData/'

wavelengths = range(110,260,10)

totalSetVect = []

for runNum in [10,11]:#### 10 was calibrated PD, 11 was non-calibrated PD
	tempDataSetMeans = []
	tempDataStd = []
	for wave in wavelengths:
		darkCur = 0.0
		for sampleName in ['D','L']:
			tempFileName = pathToData+'Run'+str(runNum)+'/'+str(wave)+'nm/'+str(wave)+'_nm_Sample_'+sampleName+'.txt'
			dataOut = parseFile(tempFileName)
			if sampleName == 'D':
				darkCur = dataOut[0]
			elif sampleName == 'L':
				tempDataSetMeans.append(dataOut[0]-darkCur)
				tempDataStd.append(dataOut[1])
				
	totalSetVect.append(tempDataSetMeans)

print '\n\n'

ratioVect = []
for index in range(len(totalSetVect[0])):
	ratioVect.append(totalSetVect[1][index]/totalSetVect[0][index])
	print ratioVect[-1]

for val in wavelengths:
	print val

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(wavelengths,ratioVect)