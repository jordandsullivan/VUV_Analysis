import rat
import ROOT
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

#dataPath = '~/VUV_Analysis/geoFactorSim/newGeoSim/data/config_31/pos13.root'

dataPath = '~/VUV_Analysis/Chrisdata.root'

fileIterator = rat.dsreader(dataPath)

rays = []

for i in range(1000):
    node = fileIterator.next()

    tempMC = node.GetMC()

    print 'Num Tracks: '+str(tempMC.GetMCTrackCount())
    tempTrack = tempMC.GetMCTrack(0)
    tempRay = []
    for iStep in range(tempTrack.GetMCTrackStepCount()):
        tempStep = tempTrack.GetMCTrackStep(iStep)
        tempRay.append({'x':tempStep.GetEndpoint().x(),'y':tempStep.GetEndpoint().y(),'z':tempStep.GetEndpoint().z()})

    rays.append(tempRay)

fig = plt.figure()
ax = fig.add_subplot((111), projection='3d')
ax.set_aspect('equal')

ax.set_ylim(-200,200)
ax.set_xlim(-200,200)
ax.set_zlim(-200,200)

for line in rays:
    tempX = []
    tempY = []
    tempZ = []
    for row in line:
        tempX.append(row['x'])
        tempY.append(row['y'])
        tempZ.append(row['z'])

    ax.plot(tempX,tempY,tempZ)
    ax.scatter(tempX[-1],tempY[-1],tempZ[-1])
plt.show()

