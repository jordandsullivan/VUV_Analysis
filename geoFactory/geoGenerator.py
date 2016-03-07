import math
import geoShapes as GS
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


geoFileName = 'VUV.geo'

#### TPB FILM SETTINGS #####
surfaceTPB = False ## If true, only TPB surface will be created, not volume. If false, surface deactivated and tpb volume.
tpbFilmThickness = 0.25  # in micrometers
saveTPB = True
############################
### Generate points on diffraction grating for simulation
generateSourcePoints = True
numNodes = 5
spacingPerNode = 0.1


masterString = ''

##### Create the world first
world = GS.boxVolume('world',400, 400,400)
world.material = 'aluminum'
world.mother = ''
world.invisible = 1
masterString = world.writeToString(masterString)

diffractionGraingAngle = 32
globalOffsetCoords = {'x':1.754*math.cos(diffractionGraingAngle*math.pi/180.0),'y':1.754*math.sin(diffractionGraingAngle*math.pi/180.0),'z':0.0}

#### Create the monochromator housing
monoHousing = GS.tubeVolume('monochrom_housing',7.048/2.0,4.86)
monoHousing.material = 'pmt_vacuum'
monoHousing.colorVect[3] = 0.2
monoHousing.mother = 'world'
masterString = monoHousing.writeToString(masterString)

#### Diffraction grating surface
diffractionGrating = GS.boxVolume('grating_vol',0.1,0.75,0.75)
diffractionGrating.rotation = [0.0,0.0,32.0]
diffractionGrating.mother = monoHousing.name
diffractionGrating.colorVect[3] = 1.0
diffractionGrating.material = 'aluminum'
diffractionGrating.center = {'x':-1*globalOffsetCoords['x'],'y':globalOffsetCoords['y'],'z':globalOffsetCoords['z']}
masterString = diffractionGrating.writeToString(masterString)


## we want the vertex of the center of the diffraction grating to be at 0,0,0
## UV beam wil be fired along +x axis.
distanceToSlit = 7.171 # inches

##### Now make a vac
shutterTunnel = GS.tubeVolume('shutterTunnel',1.25,8)
shutterTunnel.rotation = [0.0,90.0,0.0]
shutterTunnel.center = {'x':distanceToSlit-globalOffsetCoords['x'],'y':globalOffsetCoords['y'],'z':globalOffsetCoords['z']}
shutterTunnel.mother = 'world'
shutterTunnel.colorVect[3] = 0.2
shutterTunnel.material = 'pmt_vacuum'
masterString = shutterTunnel.writeToString(masterString)

### Sample wheel slit geometries
slitWidth = 0.07  # Default = 0.07"
slitHeight = 0.2 # Default = 0.2 Should probably measure again

### Left and right is defined looking down beam from source
sampleSlitRight = GS.boxVolume('sample_wheel_slit_right',0.05,2,3)
sampleSlitRight.center = {'x':0.0,'y':-1*sampleSlitRight.width/2.0-slitWidth/2.0,'z':0.0}
sampleSlitRight.mother = shutterTunnel.name
sampleSlitRight.material = 'acrylic_black'
sampleSlitRight.rotation = [0.0,90.0,0.0]
masterString = sampleSlitRight.writeToString(masterString)

sampleSlitLeft = GS.boxVolume('sample_wheel_slit_left',0.05,2,3)
sampleSlitLeft.center = {'x':0.0,'y':sampleSlitLeft.width/2.0+slitWidth/2.0,'z':0.0}
sampleSlitLeft.mother = shutterTunnel.name
sampleSlitLeft.material = 'acrylic_black'
sampleSlitLeft.rotation = [0.0,90.0,0.0]
sampleSlitLeft.invisible = 0.0
masterString = sampleSlitLeft.writeToString(masterString)

#### Now top and bottom slits
sampleSlitTop = GS.boxVolume('sample_wheel_slit_top',0.1,3,2)
sampleSlitTop.center = {'x':sampleSlitTop.depth/2.0+slitHeight/2.0,'y':0.0,'z':0.0}
sampleSlitTop.mother = shutterTunnel.name
sampleSlitTop.material = 'acrylic_black'
sampleSlitTop.rotation = [0.0,90.0,0.0]
sampleSlitTop.invisible = 0.0
masterString = sampleSlitTop.writeToString(masterString)

sampleSlitBottom = GS.boxVolume('sample_wheel_slit_bottom',0.1,3,2)
sampleSlitBottom.center = {'x':-1*sampleSlitTop.depth/2.0-slitHeight/2.0,'y':0.0,'z':0.0}
sampleSlitBottom.mother = shutterTunnel.name
sampleSlitBottom.material = 'acrylic_black'
sampleSlitBottom.rotation = [0.0,90.0,0.0]
sampleSlitBottom.invisible = 0.0
masterString = sampleSlitBottom.writeToString(masterString)

######### Now lets handle sample wheel ##########
distanceToFilterWheelFaceFromSlit = 0.69

sampleWheelHousing = GS.tubeVolume('sampleWheelTunnel',rMax=1.3,height=1.38,rMin=0.875/2.0)
sampleWheelHousing.mother = shutterTunnel.name
sampleWheelHousing.material = 'acrylic_black'
sampleWheelHousing.colorVect[3] = 0.3
sampleWheelHousing.center = {'x':0.0,'y':0.0,'z':-1*sampleWheelHousing.height/2.0-distanceToFilterWheelFaceFromSlit}
masterString = sampleWheelHousing.writeToString(masterString)

#### Add photodioded
distanceToPhotodiodeFromSampleWheel = 2.0/16.0

photodiodeVolume = GS.boxVolume('photodiodeVolume',0.395,0.395,0.05)
photodiodeVolume.mother = shutterTunnel.name
photodiodeVolume.material = 'acrylic_black'
photodiodeVolume.rotation = [0.0,0.0,40.0]
photodiodeVolume.center = {'x':0.0,'y':0.0,'z':sampleWheelHousing.center['z']-sampleWheelHousing.height/2-photodiodeVolume.depth/2.0-distanceToPhotodiodeFromSampleWheel}
masterString = photodiodeVolume.writeToString(masterString)

## Add detector volume which is what we tag off of when counting.
photodiodeDetectorVolume = GS.boxVolume('detector_vol_vac',photodiodeVolume.height,photodiodeVolume.width,0.01)
photodiodeDetectorVolume.mother = shutterTunnel.name
photodiodeDetectorVolume.material = 'pmt_vacuum'
photodiodeDetectorVolume.colorVect[3] = 0.7
photodiodeDetectorVolume.rotation = photodiodeVolume.rotation
photodiodeDetectorVolume.center = {'x':0.0,'y':0.0,'z':photodiodeVolume.center['z']+photodiodeVolume.depth/2.0+photodiodeDetectorVolume.depth/2.0}
masterString = photodiodeDetectorVolume.writeToString(masterString)


### Photodiode cavity 
photodiodeCavity = GS.tubeVolume('photodiodeCavity',rMax=shutterTunnel.rMax,height=3.0,rMin=1.365/2.0)
photodiodeCavity.mother = shutterTunnel.name
photodiodeCavity.material = 'aluminum'
photodiodeCavity.colorVect[3] = 0.1
photodiodeCavity.center = {'x':0.0,'y':0.0,'z':sampleWheelHousing.center['z']-sampleWheelHousing.height/2.0-photodiodeCavity.height/2.0}
masterString = photodiodeCavity.writeToString(masterString)

##### Plastic behind photodiode
distanceToPlasticBehindPhotodiodeFromSampleWheel = 1.0/4.0

backPlastic = GS.tubeVolume('plasticBehindPhotodiode',rMax=photodiodeCavity.rMin,height=1.0,rMin=0.0)
backPlastic.mother = shutterTunnel.name
backPlastic.material = 'acrylic_black'
backPlastic.colorVect[3] = 0.1
backPlastic.center = {'x':0.0,'y':0.0,'z':sampleWheelHousing.center['z']-sampleWheelHousing.height/2.0-backPlastic.height/2.0-distanceToPlasticBehindPhotodiodeFromSampleWheel}
masterString = backPlastic.writeToString(masterString)

#### Create the acrylic sample
acrylicDiskFaceDistanceFromFrontSampleWheel = 0.77

acrylicSampleDisk = GS.tubeVolume('acrylicSampleDisk',rMax=sampleWheelHousing.rMin,height=0.175,rMin=0.0)
acrylicSampleDisk.mother = shutterTunnel.name
acrylicSampleDisk.material = 'acrylic_suvt'
acrylicSampleDisk.colorVect[3] = 0.8
acrylicSampleDisk.center = {'x':0.0,'y':0.0,'z':sampleWheelHousing.center['z']+sampleWheelHousing.height/2.0-acrylicSampleDisk.height/2.0-acrylicDiskFaceDistanceFromFrontSampleWheel}
masterString = acrylicSampleDisk.writeToString(masterString)

###### Small vacuum layer 
tpbLayer = GS.tubeVolume('tpbVolume',rMax=acrylicSampleDisk.rMax,height=tpbFilmThickness*3.93701*10**-5,rMin=0.0)
tpbLayer.mother = shutterTunnel.name
if surfaceTPB:
    tpbLayer.material = acrylicSampleDisk.material
else:
    tpbLayer.material = 'tpb'
tpbLayer.center = {'x':0.0,'y':0.0,'z':acrylicSampleDisk.center['z']+acrylicSampleDisk.height/2.0+tpbLayer.height/2.0}
if saveTPB:
    masterString = tpbLayer.writeToString(masterString)

if surfaceTPB:
    tpbSurface = GS.border('TPBSurface',shutterTunnel.name,tpbLayer.name)
    tpbSurface.mother = shutterTunnel.name
    tpbSurface.surface = 'tpb_surface'
    if saveTPB:
        masterString = tpbSurface.writeToString(masterString)

##### A handy utility to generate the source nodes
if generateSourcePoints:
    diffractionGratingSurfaceLocation = diffractionGrating.center
    diffractionGratingSurfaceLocation['x'] = diffractionGrating.center['x']+diffractionGrating.height/(2.0*math.cos(diffractionGraingAngle*math.pi/180.0))+\
        0.01 #0.01 is a buffer to make sure off surface
    deltaX = spacingPerNode*math.cos((90-diffractionGraingAngle)*math.pi/180.0)
    deltaY = spacingPerNode*math.sin((90-diffractionGraingAngle)*math.pi/180.0)

    coordinatePairs = []
    middleRef = math.ceil(numNodes/2.0)
    indexCount = 0
    for yIndex in range(1,numNodes+1):
        tempYOffset = deltaY*(yIndex-middleRef)
        tempXOffset = deltaX*(yIndex-middleRef)
        for zIndex in range(1,numNodes+1):
            tempZOffset = spacingPerNode*(zIndex-middleRef)
            indexCount += 1
            tempDict = {'node':indexCount,'x':GS.inTomm(diffractionGratingSurfaceLocation['x']+tempXOffset),'y':GS.inTomm(diffractionGratingSurfaceLocation['y']+tempYOffset),'z':GS.inTomm(diffractionGratingSurfaceLocation['z']+tempZOffset)}
            coordinatePairs.append(tempDict)
    
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    for line in coordinatePairs:
        ax.scatter(line['x'],line['y'],line['z'],color='b')
    ax.scatter(diffractionGratingSurfaceLocation['x'],diffractionGratingSurfaceLocation['y'],diffractionGratingSurfaceLocation['z'],color='r')
    ax.scatter(diffractionGrating.center['x'],diffractionGrating.center['y'],diffractionGrating.center['z'],'g')
   
    coordFile = open('./sourceCoords.json','w+')
    json.dump(coordinatePairs,coordFile)
    coordFile.close()

###### NOW LETS ADD SOME MORE BORDERS
#### Vectical slits should be stainless
rightSlitBorder = GS.border('rightSlitBorder',shutterTunnel.name,sampleSlitRight.name)
rightSlitBorder.mother = shutterTunnel.name
rightSlitBorder.surface = 'stainless_steel'
masterString = rightSlitBorder.writeToString(masterString)

leftSlitBorder = GS.border('leftSlitBorder',shutterTunnel.name,sampleSlitRight.name)
leftSlitBorder.mother = shutterTunnel.name
leftSlitBorder.surface = 'stainless_steel'
masterString = leftSlitBorder.writeToString(masterString)

sampleWheelHousingBorder = GS.border('sampleWheelHousingBorder',shutterTunnel.name,sampleWheelHousing.name)
sampleWheelHousingBorder.mother = shutterTunnel.name
sampleWheelHousingBorder.surface = 'black_sheet'
masterString = sampleWheelHousingBorder.writeToString(masterString)

photodiodeCavitySurface = GS.border('photodiodeCavityBorder',shutterTunnel.name,photodiodeCavity.name)
photodiodeCavitySurface.mother = shutterTunnel.name
photodiodeCavitySurface.surface = 'stainless_steel' 
masterString = photodiodeCavitySurface.writeToString(masterString)


##### Write geo out to file.
#print masterString

geoOutFile = open(geoFileName,'w+')
geoOutFile.write(masterString)
geoOutFile.close()


