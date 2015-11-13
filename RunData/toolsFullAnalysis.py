#!bin/python
import ROOT
import SpectraTools as ST
import UVLampTools as ULT # /Users/chrisbenson/Documents/Research/VUV/Analysis_Scripts/VUV_Tools/UVLampTools.py
import os
import pandas as pd
import matplotlib.pyplot as plt

class configParam:
	def __init__(self,objType):
		if objType == 1:
			# This is for a spectrum
			self.histTitle = 'default'
			self.histName = 'default'
			self.histColor = 1
			self.histLine = 1
			self.corrAcylic = False
			self.zeroFront = True
		elif objType == 2:
			# This is for current data
			self.histTitle = 'default'
			self.emissionSpectRun = None # required emission spectrum for analysis
			self.emissionSpectName = 'default'
			self.histColor = 1
			self.histLine = 1
			self.histName = 1
			self.histTitle = 'default'
			
			# need to add more when ready

# Configuration file "Notes.txt" parser
def parseConfig(dataPath,configType):
	configSet = configParam(configType)
	tempFile = open(dataPath+'/Notes.txt').read().split('\n')
	if configType == 1: # Type for spectrums
		for line in tempFile:
			if 'histName' in line:
				configSet.histName = line.split(':')[1]
				continue
			elif 'histTitle' in line:
				configSet.histTitle = line.split(':')[1]
				continue
			elif 'histColor' in line:
				configSet.histColor = int(line.split(':')[1])
				continue
			elif 'histLine' in line:
				configSet.histLine = int(line.split(':')[1])
				continue
			elif 'corrAcylic' in line:
				configSet.corrAcylic = bool(int(line.split(':')[1]))
				continue
			elif 'zeroFront' in line:
				configSet.zeroFront = bool(int(line.split(':')[1]))
				continue
	elif configType == 2: # current data
		for line in tempFile:
			if 'emissionSpectRun' in line:
				configSet.emissionSpectRun = int(line.split(':')[1])
				continue				
			elif 'emissionSpectName' in line:
				configSet.emissionSpectName = line.split(':')[1].replace('\r','')
				continue			
			elif 'histColor' in line:
				configSet.histColor = int(line.split(':')[1])
				continue
			elif 'histLine' in line:
				configSet.histLine = int(line.split(':')[1])
				continue
			elif 'histName' in line:
				configSet.histName = line.split(':')[1].replace('\r','')
				continue
			elif 'histTitle' in line:
				configSet.histTitle = line.split(':')[1].replace('\r','')
				continue
					
	
	return configSet
		
#### Tool Class for plotting spectra
class spectrum:
	def __init__(self,pathToData,pathToSave):
		# Check to see if a Notes.txt file exists with configurations
		self.pathToData = pathToData
		self.pathToSave = pathToSave
		
		fileList = os.listdir(pathToData)
		
		# Check for Notes.txt for configuration options
		self.configSet = None
		if 'Notes.txt' in fileList:
			# Yes we do have a configuration file so parse it!
			self.configSet = parseConfig(self.pathToData,1)
		else:
			self.configSet = configParam(1)
			
		# Parse the file list and sort light and dark files
		darkFiles = []
		lightFiles = []
		for fileName in fileList:
			if ('.txt' in fileName) and (('Dark' in fileName) or ('Light' in fileName)):
				if 'Dark' in fileName:
					darkFiles.append(fileName)
				elif 'Light' in fileName:
					lightFiles.append(fileName)
		# Make sure there is the same number of light and dark files
		if len(darkFiles) != len(lightFiles):	
			raise ValueError('Spectrum Processor: Dark and Light files in '+self.pathToData+' do not have the same number of files.')
		
		# Extract Fiber Transmittance
		self.TransmittanceFile = ROOT.TFile.Open('/Users/chrisbenson/Documents/Research/VUV/Analysis_Scripts/VUV_Tools/transmittance.root')
		self.fiber_transmittance = self.TransmittanceFile.Get("transmittance")
			
		self.baseline_sub_window_bottom = 750
		self.baseline_sub_window_top = 900
			
		# Determine if we want to correct for acrylic or not.
		self.acrylic_transmittance = None
		if self.configSet.corrAcylic:
			self.acrylic_transmittance = ULT.GetAcrylicTransmittance()
		else: 
			self.acrylic_transmittance = ST.NullAcrylicSpectrum()
			
		self.hist = ST.GetSpectrum(self.pathToData, len(darkFiles), self.configSet.histName , self.configSet.histTitle, self.acrylic_transmittance, self.fiber_transmittance, self.configSet.histColor, self.configSet.histLine)
		self.histUncorr = ST.GetSpectrum(self.pathToData, len(darkFiles), self.configSet.histName+'unCorr' , self.configSet.histTitle+'unCorr', ST.NullAcrylicSpectrum(), self.fiber_transmittance, self.configSet.histColor, self.configSet.histLine)

				
		# Shift the histogram baseline
		[self.hist, self.baseline_shift] = ULT.BaselineSubtraction(self.hist, self.baseline_sub_window_bottom, self.baseline_sub_window_top)
		 # Create and store fiber corrected and normalized spectrum 
		 
		self.correctedHist = ULT.TransmittanceCorrection(self.hist, self.acrylic_transmittance, self.fiber_transmittance)
		
		# zero bins less than 260.
		if self.configSet.zeroFront:
			keepGoing = True
			binIndex = -1
			while keepGoing:
				binIndex += 1
				if self.correctedHist.GetBinCenter(binIndex) < 275:
					self.correctedHist.SetBinContent(binIndex,0.0)
				else:
					keepGoing = False
					continue
		
	def writeHistos(self):
		# Method to write out all relevant histograms to root file
		fileOut = ROOT.TFile(self.pathToSave+'/'+'histOut.root',"RECREATE")
		self.hist.Write()
		self.correctedHist.Write()
		normHist = ST.NormalizeSpectrum(self.hist)
		normHist.SetTitle(self.configSet.histTitle+' Normalized')
		normHist.SetName(self.configSet.histName+'Normalized')
		normHist.Write()
		normCorrHist = ST.NormalizeSpectrum(self.correctedHist)
		normCorrHist.SetTitle(self.configSet.histTitle+' Corrected Normalized')
		normCorrHist.SetName(self.configSet.histName+'CorrNormalized')
		normCorrHist.Write()
		self.histUncorr.Write()
		
			
#### Efficiency calculation object
class efficency:
	def __init__(self,pathToData,pathToSave):
		self.pathToData = pathToData
		self.pathToSave = pathToSave
		
		fileList = os.listdir(pathToData)
		
		# Check for Notes.txt for configuration options
		self.configSet = None
		if 'Notes.txt' in fileList:
			# Yes we do have a configuration file so parse it!
			self.configSet = parseConfig(self.pathToData,2)
		else:
			self.configSet = configParam(2)
			
		newDirContents = os.listdir(self.pathToData)
		wavelengths = []
		wavelengthDir = []
		for fileName in newDirContents:	
			if ('nm' in fileName) and (not ('.' in fileName)):
				tempName = fileName.replace('nm','')
				wavelengths.append(int(tempName))
		# sort the wavelength directories in ascending order
		wavelengths = sorted(wavelengths,key=int)
		self.wavelengths = wavelengths
		# Look at the first wavelength to see what types of files are in there and create a panda dataframe
		testDataPath = pathToData+str(wavelengths[0])+'nm/'
		testDirContents = os.listdir(testDataPath)
		sampleNameList = []
		for testFileName in testDirContents:
			if '.txt' in testFileName:
				tempName = testFileName.replace((str(wavelengths[0])+'_nm_Sample_'),'')
				tempName = tempName.replace('.txt','')
				sampleNameList.append(tempName)
		
		orderedSampleNames = []
		legendNames = []
		pdColNames = []
		if 'D' in sampleNameList:
			orderedSampleNames.append('D')
			sampleNameList.pop(sampleNameList.index('D'))
			legendNames.append('Dark')
			pdColNames.append('Dark')
			pdColNames.append('uDark')
		if 'L' in sampleNameList:
			orderedSampleNames.append('L')
			sampleNameList.pop(sampleNameList.index('L'))
			legendNames.append('Light')
			pdColNames.append('Light')
			pdColNames.append('uLight')
		if 'A' in sampleNameList:
			orderedSampleNames.append('A')
			sampleNameList.pop(sampleNameList.index('A'))
			legendNames.append('Acrylic')
			pdColNames.append('Acrylic')
			pdColNames.append('uAcrylic')
		if 'Q' in sampleNameList:
			orderedSampleNames.append('Q')
			sampleNameList.pop(sampleNameList.index('Q'))
			legendNames.append('Quartz')
			pdColNames.append('Quartz')	
			pdColNames.append('uQuartz')	
		if 'T' in sampleNameList:
			orderedSampleNames.append('T')
			sampleNameList.pop(sampleNameList.index('T'))
			legendNames.append('TPB')
			pdColNames.append('TPB')	
			pdColNames.append('uTPB')	
			
		for remainItem in sampleNameList:
			orderedSampleNames.append(remainItem)
			legendNames.append(remainItem)
			pdColNames.append(remainItem)
			pdColNames.append('u'+remainItem)
			
		# Init the pandas dataframe for this object
		pdSet = pd.DataFrame(columns=pdColNames,index=wavelengths)
		
		for wIndex,wave in enumerate(wavelengths):
			for sIndex,sampleName in enumerate(orderedSampleNames):
				tempFileName = pathToData+str(wave)+'nm/'+str(wave)+'_nm_Sample_'+sampleName+'.txt'
				tempFile = open(tempFileName,'r').read().split('\n')[1].split(',')[2:]
				pdSet.loc[wave][pdColNames[2*sIndex]] = float(tempFile[0])
				pdSet.loc[wave][pdColNames[2*sIndex+1]] = float(tempFile[1])
			
		self.legendNames = legendNames
		self.pdSet = pdSet
		
		# Now that all of the data is initialized, we must create concatenated data set for efficiency calcs
		self.concatCurrentDataCSVOut() # This creates and stores the concatenated current data set in the format we need in the local results folder.
		
		# extract the corrected and uncorrected flur spectrum
		self.pathToSpectrum = '/Users/chrisbenson/Documents/Research/VUV/Data/RunDataResults/Run'+str(self.configSet.emissionSpectRun)+'/histOut.root'
		self.spectrumFile = ROOT.TFile(self.pathToSpectrum)
		corrSpectrumName = self.configSet.emissionSpectName+'CorrNormalized'
		uncorrSpectrumName = self.configSet.emissionSpectName+'unCorr'
		self.corrEmissionSpectrum = self.spectrumFile.Get(corrSpectrumName)
		self.uncorrEmissionSpectrum = self.spectrumFile.Get(uncorrSpectrumName)
		
		### Eff calculations
		self.Eff_Results = ULT.compute_eff_unc(self.pathToSave+'CurrentDataSet.csv', name="Eff_JustTPB", 
                                          tpb_spectrum = self.corrEmissionSpectrum, tpb_spectrum_uncorrected = self.uncorrEmissionSpectrum, 
                                          wavelength_col = 0, dark_col = 3, dark_unc_col = 4, 
                                          lamp_start_col = 5, lamp_start_unc_col = 6, 
                                          tpb_col = 7, tpb_unc_col = 8, 
                                          lamp_stop_col = 5, lamp_stop_unc_col = 6, forward_eff = True)

		### Loop through bins of results and store them in a csv file
		self.Eff_Results.SaveAs(self.pathToSave+'sampleEff.root')
		print 'Efficiency Results'
		masterString = 'wavelength,EffVal,Unc'
		for i in range(self.Eff_Results.GetN()): 
			print self.Eff_Results.GetX()[i], "\t", self.Eff_Results.GetY()[i], "+/-", self.Eff_Results.GetEY()[i]
			masterString += '\n'+str(self.Eff_Results.GetX()[i]) +',' +str(self.Eff_Results.GetY()[i]) +',' +str(self.Eff_Results.GetEY()[i])
		effTextOut = open(self.pathToSave+'effData.csv','w+')
		effTextOut.write(masterString)
		effTextOut.close()
		
		
	def rawDataToTextFile(self):
		for index,sampName in enumerate(self.pdSet.columns.values.tolist()):
			if index%2 == 0:
				pass
			else:
				continue
			# Store the data to disk
			tempFileOut = open(self.pathToSave+sampName+'.txt','w+')
			dataStringOut = ''
			vals = self.pdSet[sampName].values
			valUncert = self.pdSet['u'+sampName].values
			for index in range(len(vals)):
				dataStringOut += str(self.wavelengths[index])+','+str(vals[index])+','+str(valUncert[index])+'\n'
			
			tempFileOut.write(dataStringOut)
			tempFileOut.close()
	
	def rawAndDarkCurrentedCurrentPlots(self):
		for index,sampName in enumerate(self.pdSet.columns.values.tolist()):
			if index == 0:
				tempFig = plt.figure()
				tempAx = tempFig.add_subplot(111)
				tempAx.errorbar(self.pdSet.index.values,self.pdSet[sampName].values,yerr=self.pdSet['u'+sampName].values,xerr=None)
				tempAx.set_ylabel(sampName+' Photocurrent [nA]')
				tempAx.set_xlabel('Wavelength [nm]')
				tempFig.savefig(self.pathToSave+sampName+'CurrentData.pdf')
				continue
			elif index % 2 == 1:
				continue
			else:
				pass
				
			tempFig = plt.figure()
			tempAx = tempFig.add_subplot(111)
			corrVals = self.pdSet[sampName].values - self.pdSet['Dark'].values
			tempAx.errorbar(self.pdSet.index.values,corrVals,yerr=self.pdSet['u'+sampName].values,xerr=None)
			tempAx.set_ylabel('Dark Corrected '+sampName+' Photocurrent [nA]')
			tempAx.set_xlabel('Wavelength [nm]')
			tempAx.set_yscale('log')	
			tempAx.set_ylim(bottom=10**-5)
			tempFig.savefig(self.pathToSave+sampName+'CurrentData.pdf')
			
	def allCurrentPlotsTogether(self):
		allPlotFig = plt.figure()
		allAx = allPlotFig.add_subplot(111)		
		tempCounter = -1
		runningMax = 10**-5
		for index,sampName in enumerate(self.pdSet.columns.values.tolist()):
			if index % 2 == 1:
				continue
			if index == 0:
				tempCounter += 1
				corrVals = self.pdSet[sampName].values
			else:
				tempCounter += 1
				corrVals = self.pdSet[sampName].values - self.pdSet[self.pdSet.columns.values.tolist()[0]].values
			
			if corrVals.max() > runningMax:
				runningMax = corrVals.max()
			
			allAx.errorbar(self.pdSet.index.values,corrVals,yerr=self.pdSet['u'+sampName].values,xerr=None,label=self.legendNames[tempCounter])
			allAx.legend(loc='best')
			allAx.set_yscale('log')
			allAx.set_xlabel('Wavelength [nm]')
			allAx.set_ylabel('Dark Corrected Photocurrent [nA]')
			allAx.set_ylim(bottom=10**-5,top=1.5*runningMax)
			allPlotFig.savefig(self.pathToSave+'AllCurrentData.pdf')
			
	def concatCurrentDataCSVOut(self):
		masterString = 'Wavelength,Time,Pressure,Dark,DarkUnc,Lamp,LampUnc,Sample,SampleUnc'
		for wave in self.wavelengths:
			masterString +='\n'
			masterString += str(wave)+',,' # Not currently including time or pressure data
			rowSet = self.pdSet.loc[wave]
			for index,sampName in enumerate(self.pdSet.columns.values.tolist()):
				masterString += ','+str(rowSet[sampName])
		tempCSVFileOut = open(self.pathToSave+'CurrentDataSet.csv','w+')
		tempCSVFileOut.write(masterString)
		tempCSVFileOut.close()		
			
		
		