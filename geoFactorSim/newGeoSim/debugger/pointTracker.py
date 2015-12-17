import rat
import ROOT
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dataPath = '../data/isotropic_flat_intensity_tpb_surface/'

fileIterator = rat.dsreader(dataPath+'pos1.root')

rays = []

for i in range(1000):
    tempEntry = fileIterator.next()
    
    tempMC = tempEntry.GetMC()
    
    print 'Num Tracks: '+str(tempMC.GetMCTrackCount())
    tempTrack = tempMC.GetMCTrack(0)
    tempRay = []
    for iStep in range(tempTrack.GetMCTrackStepCount()):
        tempStep = tempTrack.GetMCTrackStep(iStep)
        tempRay.append({'x':tempStep.GetEndpoint().x(),'y':tempStep.GetEndpoint().y(),'z':tempStep.GetEndpoint().z()})
    
    rays.append(tempRay)

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

for line in rays:
    tempX = []
    tempY = []
    tempZ = []
    for row in line:
        tempX.append(row['x'])
        tempY.append(row['y'])
        tempZ.append(row['z'])

    ax.plot(tempX,tempY,tempZ)
