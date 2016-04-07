#!/bin/python
import trackTools as TT
import ROOT
import sys

argss = sys.argv

basePath = '/data/snoplus/home/cbenson/VUV/data/groupTest/'
fileName = 'pos25.root'
#totalFileName = basePath+fileName

totalFileName = argss[0]

data = TT.trackSorter(totalFileName)

numScintPhotons = float(sum(data.caseCount[4:]))
numdetected = data.caseCount[8]

print data.caseCount
print 'Number of simulated photons: '+str(data.caseCount[2])
print 'Number of sintilation photons: '+str(numScintPhotons)
print 'Number of detected photons: '+str(numdetected)
try:
	geoFactor = numdetected/numScintPhotons
	print 'Geometric Factor:'+str(geoFactor)
except:
	pass

C1 = ROOT.TCanvas()
lambdaStart = ROOT.TH1D("startLambda","startLambda",100,350,600)
lambdaEnd = ROOT.TH1D("endLambda","endLambda",100,350,600)
for index,startVal in enumerate(data.WLS_Start):
	lambdaStart.Fill(startVal)
	lambdaEnd.Fill(data.WLS_End[index])
lambdaStart.Draw()

C2 = ROOT.TCanvas()
lambdaEnd.Draw("E1")

data.testFigure.show()




