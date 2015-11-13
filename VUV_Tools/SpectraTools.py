# Make this a Spectrum tools module

# Header, import statements etc.
import sys
import ROOT
import array
import RootifySpectraSuite
import RootPlotLibs
import UVLampTools

def GetSpectrum(path, nfiles, name, title, substratecorrection, fibercorrection, color, linestyle):
	# Read in the data and create dark corrected histograms for each film
	DarkSpecHist = []
	LightSpecHist = []
	# Loop over the files
	for i in range(0, nfiles):
		FileName = path + "Dark_%0*d.txt" % (2, i)
		DarkSpecHist.append(RootifySpectraSuite.RootifySpectraSuite(FileName))
		FileName = path + "Light_%0*d.txt" % (2, i)
		LightSpecHist.append(RootifySpectraSuite.RootifySpectraSuite(FileName))
	# Set up the histogram
	TitleSize = 0.05
	TitleOffset = 0.8
	LabelSize = 0.03
	ThisSpectrum = ROOT.TH1D(name, title, LightSpecHist[0].GetNbinsX(), 
										LightSpecHist[0].GetXaxis().GetXmin(),
										LightSpecHist[0].GetXaxis().GetXmax())
	for i in range(0, nfiles):
		ThisSpectrum.Add(LightSpecHist[i], 1. / float(nfiles))
		ThisSpectrum.Add(DarkSpecHist[i], -1. / float(nfiles))
	ThisSpectrum = UVLampTools.TransmittanceCorrection(ThisSpectrum, substratecorrection, fibercorrection)
	ThisSpectrum.SetName(name)
	ThisSpectrum.SetTitle(title)
	ThisSpectrum.GetXaxis().SetTitle("Wavelength [nm]")
	ThisSpectrum.GetXaxis().SetTitleSize(TitleSize)
	ThisSpectrum.GetXaxis().SetTitleOffset(TitleOffset)
	ThisSpectrum.GetXaxis().SetLabelSize(LabelSize)
	ThisSpectrum.GetYaxis().SetTitle("Net Spectral Intensity [ADC]")
	ThisSpectrum.GetYaxis().SetTitleSize(TitleSize)
	ThisSpectrum.GetYaxis().SetTitleOffset(1.15 * TitleOffset)
	ThisSpectrum.GetYaxis().SetLabelSize(LabelSize)
	ThisSpectrum.SetLineColor(color)
	ThisSpectrum.SetLineStyle(linestyle)
	return ThisSpectrum

def NormalizeSpectrum(spectrum):
	spectrumBW = spectrum.GetBinCenter(26) - spectrum.GetBinCenter(25)
	spectrum.Scale(1. / abs(spectrumBW * spectrum.Integral()))
	spectrum.GetYaxis().SetTitle("Spectral Density [nm ^{-1}]")
	return spectrum
  
# Return a unity acrylic curve to substitute for not having acrylic in the way.
def NullAcrylicSpectrum():
	AcrylicTransGraph = UVLampTools.GetAcrylicTransmittance()
	UnitTransWL = []
	Ones = []
	for i in range(0, AcrylicTransGraph.GetN()):
		UnitTransWL.append(float(AcrylicTransGraph.GetX()[i]))
		Ones.append(float(1.))
	UnitTransWL = array.array("f", UnitTransWL)
	Ones = array.array("f", Ones)
	UnitTransmittanceGraph = ROOT.TGraph(AcrylicTransGraph.GetN(), UnitTransWL, Ones)
	
	return UnitTransmittanceGraph

