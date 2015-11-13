import matplotlib.pyplot as plt

pathToOrignal = './IRD_Cals/IRD_photodiode_calibration_Orignal.csv'


### Extract Data
wavelengths = []
absResponse = []
relUncert = []
absUncert = []

tempFile = open(pathToOrignal,'r').read().split('\n')
for index,line in enumerate(tempFile):
	if index == 0:
		continue
	tempLine = line.split(',')
	wavelengths.append(float(tempLine[0]))
	absResponse.append(float(tempLine[1]))
	relUncert.append(float(tempLine[2]))
	absUncert.append(relUncert[-1]*absResponse[-1]*0.01)
	
##### now selectively shift vals by a const factor in our regions of interest
adjustedResponse = []

minWave = 0
maxWave = 1000

scaleFactor = 1.15

for index,wave in enumerate(wavelengths):
	if wave >= minWave and wave <= maxWave:
		# adjust
		adjustedResponse.append(absResponse[index]*scaleFactor)
	else:
		adjustedResponse.append(absResponse[index])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.errorbar(wavelengths,adjustedResponse,yerr=absUncert,label='adjusted')
ax.errorbar(wavelengths,absResponse,yerr=absUncert,label='2008')


##### Now put this in a new file
outFileName = './IRD_File_Out.csv'
fileOut = open(outFileName,'w')
masterString = 'Wavelength [nm],Absolute Responsivity [A/W],Relative Expanded Uncertainty (k=2) [%]\n'
for index,val in enumerate(wavelengths):
	masterString += str(val)+','+str(adjustedResponse[index])+','+str(relUncert[index])+'\n'

fileOut.write(masterString)
fileOut.close()





