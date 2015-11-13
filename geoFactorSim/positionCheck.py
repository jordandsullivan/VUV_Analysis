import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ROOT
import math

macroList = os.listdir('./sourceMacros/')
numNodes = math.sqrt(len(macroList))

x = []
y = []
z = []

intensityY = []
intensityZ = []

for index in range(1,len(macroList)+1):
	tempFileName = './sourceMacros/pos'+str(index)+'.mac'
	tempFile = open(tempFileName,'r').read().split('\n')
	for line in tempFile:
		tempLine = line.split(' ')
		if tempLine[0] == '/generator/pos/set':
			x.append(float(tempLine[1]))
			y.append(float(tempLine[2]))
			z.append(float(tempLine[3]))
		elif tempLine[0] == '/run/beamOn':
			if index in range(55,66):
				intensityY.append(float(tempLine[1]))
			if index%numNodes == 0:
				intensityZ.append(float(tempLine[1]))
			print tempFileName+': numPhotons = '+str(tempLine[1])
		else:
			continue
	
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(x,y,z)
fig.show()

figIy = plt.figure()
axIy = figIy.add_subplot(111)
axIy.plot(y[55:66],intensityY)
figIy.show()


#figIz = plt.figure()
#axIz = figIz.add_subplot(111)




