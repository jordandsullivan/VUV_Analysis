##############################################################################
# Read in direct light spectra from the UV lamp and save it as a root object #
##############################################################################

# Header, import statements etc.
import sys
import ROOT
import string
import numpy
import array
import datetime

def RootifySpectraSuite(SpecFileName):
# My Root startup file
#ROOT.gROOT.ProcessLine(".x ~/.rootstartup")

# Open up the data file...
    #print 'Reading in spectrum data...'
    SpecDataIn = open(SpecFileName, 'rU')

# Lists to store the data...
    WavelengthList = []
    IntensityList = []
# Loop over the file and read in the data...
    RowNumber = 0
    for Row in SpecDataIn:
        WavelengthList.append(Row.split('\t')[0])
        IntensityList.append(Row.split('\t')[1])
        #print WavelengthList[RowNumber], " ", IntensityList[RowNumber]
        RowNumber = RowNumber + 1

# Convert the above lists to arrays of floats...
    WavelengthData = range(0, RowNumber)
    IntensityData  = range(0, RowNumber)
    for i in range(0, RowNumber):
        WavelengthData[i] = float(WavelengthList[i])
        IntensityData[i] = float(IntensityList[i])
    WavelengthData = array.array("f", WavelengthData)
    IntensityData  = array.array("f", IntensityData)

# Create a TH1D object to store this data
    TitleString = "Rootified " + SpecFileName
    SpecBinWidth = WavelengthData[5] - WavelengthData[4]
    SpecDataHist = ROOT.TH1D(SpecFileName, TitleString, RowNumber,WavelengthData[0] - (0.5 * SpecBinWidth),WavelengthData[RowNumber - 1] + (0.5 * SpecBinWidth))
    SpecDataHist.GetXaxis().SetTitle("Wavelength [nm]")
    SpecDataHist.GetXaxis().SetTitleSize(0.07)
    SpecDataHist.GetXaxis().SetTitleOffset(0.7)
    SpecDataHist.GetXaxis().SetLabelSize(0.05)
    SpecDataHist.GetYaxis().SetTitle("Spectral Intensity [ADC]")
    SpecDataHist.GetYaxis().SetTitleSize(0.07)
    SpecDataHist.GetYaxis().SetTitleOffset(0.8)
    SpecDataHist.GetYaxis().SetLabelSize(0.05)

# Write the spectral data to the TH1D...
    for i in range(0, RowNumber):
        SpecDataHist.SetBinContent(i, IntensityData[i])

# Return the spectrum histogram...
    return SpecDataHist