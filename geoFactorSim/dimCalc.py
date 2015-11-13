#!bin/python
import math
import matplotlib.pyplot as plt
import numpy as np

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def inTomm(inch):
	return inch*25.4
	
def lawCosAlpha(a,b,c):
	# returns alpha (rad) from law of cosines
	alpha = math.acos((b**2 + c**2 - a**2)/(2*b*c))
	return alpha

### Monochromator housing	
category = 'monochrom_housing'
print category+':'
monRad = inTomm(3.52)
monZ = inTomm(4.86/2.0)

print 'radius:'+str(monRad)
print 'z:'+str(monZ)
print 'pos: [0,0,0]'
print ''


#### shutter_tunnel
category = 'shutter_tunnel'
print category+':'
shutTunRad = inTomm(2.5/2.0)
shutTunZ = inTomm((2.75+2*1.38)/2.0)  #inTomm(2.75/2.0) # old setup
shutTunFluff = inTomm(0.7)/2.0
shutAlpha = lawCosAlpha(inTomm(1.75),monRad,inTomm(4.93))
shutTunoffsetX = round(monRad*math.cos(shutAlpha),2)
shutTunoffsetY = round(monRad*math.sin(shutAlpha),2)

print 'radius: '+str(shutTunRad)
print 'z: '+str(shutTunZ+shutTunFluff)
print 'pos: ['+str(shutTunoffsetX+shutTunZ-shutTunFluff)+','+str(shutTunoffsetY)+',0]'
print 'rot: [0.0,90.0,0.0]'
print ''

## Point source location:
sourceX = shutTunoffsetX-inTomm(4.93)
sourceY = shutTunoffsetY

print 'Source Location:'
print 'X Offset: '+str(sourceX)
print 'Y Offset: '+str(sourceY)
print ''

######## Filter Wheel Hole steel
category = 'filter_wheel'
print category+':'
filterHoleRadmax = shutTunRad
filterHoleRadmin = inTomm(0.875/2.0)
filterHolez = inTomm(1.38/2.0)
filterHolePos = [0.0,0.0,shutTunZ-(inTomm(2.75)+filterHolez)]

print 'r_max: '+str(filterHoleRadmax)
print 'r_min: '+str(filterHoleRadmin)
print 'z: '+str(filterHolez)
print 'pos: '+str(filterHolePos)
#print 'rot: [0.0,90.0,0.0]'
print ''

########## MONOCHROMATOR SLIT ##################
######## Monochrom slit 1
cateogry = 'monochrom slit 1'
print cateogry+':'
monoChromSlitGap = inTomm(0.59)
monochromSlitDims1 = [inTomm(1/16.0),inTomm(0.5),inTomm(1.5)] # 1/2 dims for 1.
monochromSlitOffset1 = [shutTunoffsetX-inTomm(0.945),shutTunoffsetY+monochromSlitDims1[1]+monoChromSlitGap/2.0,0.0]

print 'dims: '+str(monochromSlitDims1)
print 'pos: '+str(monochromSlitOffset1)
print ''

######## Monochrom slit 2
cateogry = 'monochrom slit 2'
print cateogry+':'
monochromSlitDims2 = [inTomm(1/16.0),inTomm(0.5),inTomm(1.5)] # 1/2 dims for 1.
monochromSlitOffset2 = [shutTunoffsetX-inTomm(0.945),shutTunoffsetY-monochromSlitDims2[1]-monoChromSlitGap/2.0,0.0]

print 'dims: '+str(monochromSlitDims2)
print 'pos: '+str(monochromSlitOffset2)
print ''

######## Monochrom slit 3 (top)
cateogry = 'monochrom slit top'
print cateogry+':'
monochromVertSlitGap = inTomm(1.12)
monochromSlitDims3 = [inTomm(1/16.0),monoChromSlitGap/2.0,inTomm(0.5)] # 1/2 dims for 1.
monochromSlitOffset3 = [shutTunoffsetX-inTomm(0.945),shutTunoffsetY,monochromVertSlitGap/2.0+monochromSlitDims3[2]]

print 'dims: '+str(monochromSlitDims3)
print 'pos: '+str(monochromSlitOffset3)
print ''

######## Monochrom slit 4 (bottom)
cateogry = 'monochrom slit bottom'
print cateogry+':'
monochromSlitDims4 = [inTomm(1/16.0),monoChromSlitGap/2.0,inTomm(0.5)] # 1/2 dims for 1.
monochromSlitOffset4 = [shutTunoffsetX-inTomm(0.945),shutTunoffsetY,-1*monochromVertSlitGap/2.0-monochromSlitDims4[2]]

print 'dims: '+str(monochromSlitDims4)
print 'pos: '+str(monochromSlitOffset4)
print ''
########## MONOCHROMATOR SLIT END ##################

########## SHUTTER TUNNER SLIT START ##################
cateogry = 'sample_wheel_slit_1'
print cateogry+':'
sampleWheelSlitGapHorz = inTomm(0.07) # Was set to 0.07 in
sampleWheelSlitDims1 = [inTomm(1.5),inTomm(1.25/2.0),inTomm(1/16.0)]
sampleWheelSlitOffset1 = [0.0,sampleWheelSlitDims1[1]+sampleWheelSlitGapHorz/2.0,(filterHolePos[2]+filterHolez+inTomm(0.69))]

print 'dims: '+str(sampleWheelSlitDims1)
print 'pos: '+str(sampleWheelSlitOffset1)
print ''

###################
cateogry = 'sample_wheel_slit_2'
print cateogry+':'
sampleWheelSlitDims2 = [inTomm(1.5),inTomm(1.25/2.0),inTomm(1/16.0)]
sampleWheelSlitOffset2 = [0.0,-1*sampleWheelSlitDims2[1]-sampleWheelSlitGapHorz/2.0,(filterHolePos[2]+filterHolez+inTomm(0.69))]

print 'dims: '+str(sampleWheelSlitDims2)
print 'pos: '+str(sampleWheelSlitOffset2)
print ''

###################
cateogry = 'sample_wheel_slit_top'
print cateogry+':'
sampleWheelSlitGapVert = inTomm(0.28)
sampleWheelSlitDims3 = [inTomm(1.25/2.0),inTomm(1.5),inTomm(1/16.0)]
sampleWheelSlitOffset3 = [sampleWheelSlitDims3[0]+sampleWheelSlitGapVert/2.0,0.0,(filterHolePos[2]+filterHolez+inTomm(0.69))]

print 'dims: '+str(sampleWheelSlitDims3)
print 'pos: '+str(sampleWheelSlitOffset3)
print ''

###################
cateogry = 'sample_wheel_slit_bottom'
print cateogry+':'
sampleWheelSlitDims4 = [inTomm(1.25/2.0),inTomm(1.5),inTomm(1/16.0)]
sampleWheelSlitOffset4 = [-1*sampleWheelSlitDims4[0]-sampleWheelSlitGapVert/2.0,0.0,(filterHolePos[2]+filterHolez+inTomm(0.69))]

print 'dims: '+str(sampleWheelSlitDims4)
print 'pos: '+str(sampleWheelSlitOffset4)
print ''


########## SHUTTER TUNNER SLIT END ##################

###### Sample in beam ######
cateogry = 'acrylicSample'
print cateogry+':'
sampleZ = inTomm(1/(8.0*2)) # Sample Width
sampleRmax = filterHoleRadmin
backsideSampleOffset = inTomm(0.5) # offset dimensions from the backside of the filter wheel to sample back surface
offsetDims = [0.0,0.0,filterHolePos[2]-filterHolez+backsideSampleOffset+sampleZ]

print 'radius: '+str(sampleRmax)
print 'z: '+str(sampleZ)
print 'offset dims:'+str(offsetDims)
print ''


#### Small TPB vacuum volume for interface
cateogry = 'tpbFilm'
print cateogry+':'
tpbVacuumZ = 1.0*10**-6*10**3/2.0
tpbVacuumRMax = sampleRmax
tpbVacuumOffset = offsetDims[:]
tpbVacuumOffset[2] += sampleZ + tpbVacuumZ

print 'radius: '+str(tpbVacuumRMax)
print 'z: '+str(tpbVacuumZ)
print 'offset dims:'+str(tpbVacuumOffset)
print ''

###### DETECTOR VOLUME #########

# Large detector surface
cateogry = 'detectorVol'
print cateogry+':box'
sensorDistFromSampleBack = inTomm(1/8.0)
detectorVoldims = [10.0/2,10.0/2,3.0/2]
detectorVolRot = [0.0,0.0,45.0]
detectorVolPos = filterHolePos[:]
detectorVolPos[2] -= filterHolez + sensorDistFromSampleBack + detectorVoldims[2]

print 'dims: '+str(detectorVoldims)
print 'rot: '+str(detectorVolRot)
print 'pos: '+str(detectorVolPos)
print ''

# Detector vacuum film for volume id
cateogry = 'detectorVolVac'
print cateogry+':box'
detectorVolVacdims = [10.0/2,10.0/2,0.00001/2]
detectorVolVacRot = [0.0,0.0,45.0]
detectorVolVacPos = detectorVolPos
detectorVolPos[2] += detectorVoldims[2] + detectorVolVacdims[2]

print 'dims: '+str(detectorVolVacdims)
print 'rot: '+str(detectorVolVacRot)
print 'pos: '+str(detectorVolVacPos)
print ''

# Cylinder around diode
cateogry = 'photodiodeCylinder'
print cateogry+':tube'
photodiodeCylMaxR = shutTunRad
photodiodeCylMinR = inTomm(1.365/2.0) 
photodiodeCylZ = inTomm(3.0/2)
photodiodeCylPos = filterHolePos[:]
photodiodeCylPos[2] -= filterHolez+photodiodeCylZ

print 'maxR: '+str(photodiodeCylMaxR)
print 'minR: '+str(photodiodeCylMinR)
print 'z: '+str(photodiodeCylZ)
print 'pos: '+str(photodiodeCylPos)
print ''

# black plastic behind photodiode
cateogry = 'plasticBehindPhotodiode'
print cateogry+':tube'
photodiodeGap = inTomm(0.25)
plasticBehindPhotodiodeRMax = photodiodeCylMinR
plasticBehindPhotodiodeZ = inTomm(1.0/2)
plasticBehindPhotodiodePos = filterHolePos[:]
plasticBehindPhotodiodePos[2] -= filterHolez+photodiodeGap+plasticBehindPhotodiodeZ

print 'photodiode gap: '+str(photodiodeGap)
print 'maxR: '+str(plasticBehindPhotodiodeRMax)
print 'z: '+str(plasticBehindPhotodiodeZ)
print 'pos: '+str(plasticBehindPhotodiodePos)
print ''

###### Source positions
sourceCenterX = sourceY
sourceCenterY = 0
XPositionVect = []
YPositionVect = []
overalWidth = inTomm(0.75)
overalHeight = inTomm(0.75)
numberOfNodesLRofCenter = 5
XSpacing = overalWidth/float(numberOfNodesLRofCenter*2)
YSpacing = overalHeight/float(numberOfNodesLRofCenter*2)
for index in range(-1*numberOfNodesLRofCenter,numberOfNodesLRofCenter+1):
	XPositionVect.append(index*XSpacing+sourceCenterX)
	YPositionVect.append(index*YSpacing+sourceCenterY)

print 'Soucre locations'
print XPositionVect
print YPositionVect

### Gaussian intensity output
#haha = gaussian(np.linspace(-3, 3, 120), mu, sig)
dist = 'flat'

YIntensityFactors = None
ZIntensityFactors = None
if dist == 'gaus':
	y_mu = sourceCenterX
	z_mu = sourceCenterY
	y_sig = (overalWidth/2.0)/2.0
	z_sig = (overalHeight/2.0)/2.0
	YIntensityFactors = gaussian(np.array(XPositionVect),y_mu,y_sig)
	ZIntensityFactors = gaussian(np.array(YPositionVect),z_mu,z_sig)
	YIntensityFactors = list(YIntensityFactors)
	ZIntensityFactors = list(ZIntensityFactors)
elif dist == 'flat':
	YIntensityFactors = [1.0]*len(XPositionVect)
	ZIntensityFactors = [1.0]*len(XPositionVect)

print 'Y Intenstiy vs position: '+str(list(YIntensityFactors))
print 'Z Intesntiy vs position: '+str(list(ZIntensityFactors))




