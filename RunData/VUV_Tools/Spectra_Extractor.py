import sys
import ROOT
import string
import numpy
import array
import datetime
import RootifySpectraSuite
import RootPlotLibs
import UVLampTools

def Spectra_Extractor(file_path,num_files,color_int,vacuum_only=0):

	# Some useful variables used for scaling later.	
	RebinFactor = 6
	XLo = 305.
	XHi = 710.
	YLo = -0.001
	YHi =  0.015

	#Get the transmittance corrections
	AcrylicTransGraph = UVLampTools.GetAcrylicTransmittance()
	FiberTransProfile = UVLampTools.GetFiberTransmittance()
	
	# Initialize lists which will be populated with spectrum data from txt files.
	DarkSpecHist = []
	LightSpecHist = []
	
	# Loop through files in file_path director and pull out dark and light txt and append to respective list.
	for i in range(0, num_files):
		DarkFileName = file_path+"Dark_%0*d.txt" % (2, i)
		DarkSpecHist.append(RootifySpectraSuite.RootifySpectraSuite(DarkFileName))
		# Light data
		LightFileName = file_path+"Light_%0*d.txt" % (2, i)
		LightSpecHist.append(RootifySpectraSuite.RootifySpectraSuite(LightFileName))
	
	# Create a TH1D histogram object	
	Light_Histo = ROOT.TH1D("LightHisto", "",LightSpecHist[0].GetNbinsX(),LightSpecHist[0].GetXaxis().GetXmin(),LightSpecHist[0].GetXaxis().GetXmax())
	
	for i in range(0, num_files):
		Light_Histo.Add(LightSpecHist[i], 1. / float(num_files)) # Add weighted light spectra to histogram
		Light_Histo.Add(DarkSpecHist[i], -1. / float(num_files)) # Subracted weighted dark spectra from historgram
		
	# Correct for fiber transmittance and acrylic substrate
	if vacuum_only == False:
		# Correct for fiber and acrylic substrate transmittance
		Currected_Light_Histo = UVLampTools.TransmittanceCorrection(Light_Histo, AcrylicTransGraph, FiberTransProfile)
	elif vacuum_only == True:
		# Just correct for fiber transmittance
		Currected_Light_Histo = UVLampTools.FiberTransmittanceCorrection(Light_Histo, FiberTransProfile)
		
	spectrumBW = Currected_Light_Histo.GetBinCenter(26) - Currected_Light_Histo.GetBinCenter(25)
	#Currected_Light_Histo.Scale(1. / (spectrumBW * Currected_Light_Histo.Integral()))
	#Currected_Light_Histo.GetYaxis().SetTitle("Spectral Density [nm ^{-1}]")
	
	for iBin in range(Currected_Light_Histo.GetNbinsX()):
		print Currected_Light_Histo.GetBinContent(iBin)
	
	Light_Histo.SetLineColor(color_int)
	return Light_Histo
	
	
	
test_path = '/Users/chrisbenson/Documents/Research/VUV/Setup_work/Long_Wavelength_Study/Lamp_Only/New_Lamp/'
num_files = 50

haha = Spectra_Extractor(test_path,num_files,1)

path2 = '/Users/chrisbenson/Documents/Research/VUV/Setup_work/Long_Wavelength_Study/Lamp_Only/Old_Lamp/'
dude = Spectra_Extractor(path2,num_files,2)

haha.Draw()
dude.Draw('same')
