####################################################################################################
# Some functions to manage UV optics data                                                          #
####################################################################################################

# Import all the things!
import ROOT
import array
import numpy
from numpy import sqrt

# Integrate a raw spectrum over a range of wavelengths passed to this function, and subtract that 
# off to make a baseline subtraction to remove any vertical offset from the spectrometer
def BaselineSubtraction(UnCorSpec, BLLo, BLHi):
  # UnCorSpec: non-baseline corrected spectrum (ROOT TH1D object)
  # BLLo: Wavelength for low edge of baseline integration window
  # BLHi: Wavelength for high edge of baseline integration window
  
  # Do the baseline integration
  ResidualBL = 0.
  ResidualBLBins = 0.
  for i in range(UnCorSpec.FindBin(BLLo), UnCorSpec.FindBin(BLHi) + 1):
    ResidualBL += UnCorSpec.GetBinContent(i)
    ResidualBLBins += 1.
  ResidualBL /= ResidualBLBins
  #print "Residual baseline level =", ResidualBL

  # Create a TH1D object for the corrected spectrum
  CorSpecName = UnCorSpec.GetName() + "_BLSub"
  CorSpecTitle = "Baseline Corrected" + UnCorSpec.GetName()
  CorSpec = ROOT.TH1D(CorSpecName, CorSpecTitle, UnCorSpec.GetNbinsX(), 
       UnCorSpec.GetXaxis().GetXmin(), UnCorSpec.GetXaxis().GetXmax())
  CorSpec.GetXaxis().SetTitle(UnCorSpec.GetXaxis().GetTitle())
  CorSpec.GetYaxis().SetTitle(UnCorSpec.GetYaxis().GetTitle())

  for i in range(CorSpec.GetNbinsX() + 1):
    CorSpec.SetBinContent(i, UnCorSpec.GetBinContent(i) - ResidualBL)
    
  return CorSpec, ResidualBL

# Take a TH1D file and apply a seven-point triangular smoothing filter to it, then return the
# smoothed histogtram
def SmoothHisto(UnCorSpec):
  # UnCorSpec: non-smoothed spectrum (ROOT TH1D object)
  # Create a TH1D object for the corrected spectrum
  CorSpecName = UnCorSpec.GetName() + "_Smooth"
  CorSpecTitle = "Smoothed" + UnCorSpec.GetName()
  CorSpec = ROOT.TH1D(CorSpecName, CorSpecTitle, UnCorSpec.GetNbinsX(), 
       UnCorSpec.GetXaxis().GetXmin(), UnCorSpec.GetXaxis().GetXmax())
  CorSpec.GetXaxis().SetTitle(UnCorSpec.GetXaxis().GetTitle())
  CorSpec.GetYaxis().SetTitle(UnCorSpec.GetYaxis().GetTitle())
  # Do the smoothing
  for i in range(CorSpec.GetNbinsX() + 1):
    if(i < 3):#At the start
      CorSpec.SetBinContent(i, (UnCorSpec.GetBinContent(0) + UnCorSpec.GetBinContent(1) + UnCorSpec.GetBinContent(2)) / 3.)
    if(i > CorSpec.GetNbinsX() - 4):#At the end
      CorSpec.SetBinContent(i, (UnCorSpec.GetBinContent(UnCorSpec.GetNbinsX() - 1) + UnCorSpec.GetBinContent(UnCorSpec.GetNbinsX() - 2) + UnCorSpec.GetBinContent(UnCorSpec.GetNbinsX() - 3)) / 3.)
    else:#and in the middle
      CorSpec.SetBinContent(i, ((1. / 16.) * UnCorSpec.GetBinContent(i - 3)) + ((2. / 16.) * UnCorSpec.GetBinContent(i - 2)) + ((3. / 16.) * UnCorSpec.GetBinContent(i - 1)) + ((4. / 16.) * UnCorSpec.GetBinContent(i)) + ((3. / 16.) * UnCorSpec.GetBinContent(i + 1)) +  ((2. / 16.) * UnCorSpec.GetBinContent(i + 2)) +  ((1. / 16.) * UnCorSpec.GetBinContent(i + 3)))
    
  return CorSpec

# Retrieve the acrylic transmittance data that Keith took at LANL/UNM for the 2011 TPB paper.
def GetAcrylicTransmittance():
  Wavelength = []
  Transmittance = []
    
  # Assume the first line is a header, so skip it...
  for line in open('/Users/chrisbenson/Documents/Research/VUV/Analysis_Scripts/VUV_Tools/suvt_transmittance.txt').readlines()[1:]:
    fields = map(float, line.split())
    Wavelength.append(fields[1])
    Transmittance.append(fields[2] / 100.0)

# Convert these lists to arrays
  Wavelength = array.array("f", Wavelength)
  Transmittance = array.array("f", Transmittance)
  
  return ROOT.TGraph(len(Wavelength), Wavelength, Transmittance)

# Retrieve the transmittance data for the fiber optic hardware (collimating lens, fiber optic feed-
# through and fiber optic cable) to get visible fluorescence light to the Ocean Optics spectrometer.
# This transmittance data was collected by Vic, Stan, and Keith at LANL for the 2011 TPB paper.
def GetFiberTransmittance():
	TransmittanceFile = ROOT.TFile.Open('/Users/chrisbenson/Documents/Research/VUV/Analysis_Scripts/VUV_Tools/transmittance.root')
	dudee = TransmittanceFile.Get("transmittance;1")
	return dudee
  
# Correct a spectrum (TH1D) with a the transmittance functions for the acrylic (TGraph) and the 
# fiber optic hardware (TProfile)
def TransmittanceCorrection(UncorrectedSpectrumHisto, AcrylicGraph, FiberProfile):
  CorSpecName = UncorrectedSpectrumHisto.GetName() + "_Cor"
  #print "Naming Corrected Spectrum", CorSpecName
  CorSpecTitle = UncorrectedSpectrumHisto.GetTitle() + ", Transmittance Corrected"
  #print "Titling Corrected Spectrum", CorSpecTitle
  CorrectedSpectrumHisto = ROOT.TH1D(CorSpecName, CorSpecTitle, UncorrectedSpectrumHisto.GetNbinsX(), 
       UncorrectedSpectrumHisto.GetXaxis().GetXmin(), UncorrectedSpectrumHisto.GetXaxis().GetXmax())
  CorrectedSpectrumHisto.GetXaxis().SetTitle(UncorrectedSpectrumHisto.GetXaxis().GetTitle())
  CorrectedSpectrumHisto.GetXaxis().SetTitleSize(UncorrectedSpectrumHisto.GetXaxis().GetTitleSize())
  CorrectedSpectrumHisto.GetXaxis().SetTitleOffset(UncorrectedSpectrumHisto.GetXaxis().GetTitleOffset())
  CorrectedSpectrumHisto.GetXaxis().SetLabelSize(UncorrectedSpectrumHisto.GetXaxis().GetLabelSize())
  CorrectedSpectrumHisto.GetYaxis().SetTitle(UncorrectedSpectrumHisto.GetYaxis().GetTitle())
  CorrectedSpectrumHisto.GetYaxis().SetTitleSize(UncorrectedSpectrumHisto.GetYaxis().GetTitleSize())
  CorrectedSpectrumHisto.GetYaxis().SetTitleOffset(UncorrectedSpectrumHisto.GetYaxis().GetTitleOffset())
  CorrectedSpectrumHisto.GetYaxis().SetLabelSize(UncorrectedSpectrumHisto.GetYaxis().GetLabelSize())
  CorrectedSpectrumHisto.SetLineColor(UncorrectedSpectrumHisto.GetLineColor())
  for iBin in range(UncorrectedSpectrumHisto.GetNbinsX()):
    CorrectedSpectrumHisto.SetBinContent(iBin, UncorrectedSpectrumHisto.GetBinContent(iBin) / AcrylicGraph.Eval(UncorrectedSpectrumHisto.GetBinCenter(iBin)) / FiberProfile.Interpolate(UncorrectedSpectrumHisto.GetBinCenter(iBin)))
                                    
  return CorrectedSpectrumHisto

# Correct a spectrum (TH1D) with a the transmittance function for the fiber optic hardware 
# (TProfile) only
def FiberTransmittanceCorrection(UncorrectedSpectrumHisto, FiberProfile):
  CorSpecName = UncorrectedSpectrumHisto.GetName() + "_Cor"
  #print "Naming Corrected Spectrum", CorSpecName
  CorSpecTitle = UncorrectedSpectrumHisto.GetTitle() + ", Transmittance Corrected"
  #print "Titling Corrected Spectrum", CorSpecTitle
  CorrectedSpectrumHisto = ROOT.TH1D(CorSpecName, CorSpecTitle, UncorrectedSpectrumHisto.GetNbinsX(), 
       UncorrectedSpectrumHisto.GetXaxis().GetXmin(), UncorrectedSpectrumHisto.GetXaxis().GetXmax())
  CorrectedSpectrumHisto.GetXaxis().SetTitle(UncorrectedSpectrumHisto.GetXaxis().GetTitle())
  CorrectedSpectrumHisto.GetXaxis().SetTitleSize(UncorrectedSpectrumHisto.GetXaxis().GetTitleSize())
  CorrectedSpectrumHisto.GetXaxis().SetTitleOffset(UncorrectedSpectrumHisto.GetXaxis().GetTitleOffset())
  CorrectedSpectrumHisto.GetXaxis().SetLabelSize(UncorrectedSpectrumHisto.GetXaxis().GetLabelSize())
  CorrectedSpectrumHisto.GetYaxis().SetTitle(UncorrectedSpectrumHisto.GetYaxis().GetTitle())
  CorrectedSpectrumHisto.GetYaxis().SetTitleSize(UncorrectedSpectrumHisto.GetYaxis().GetTitleSize())
  CorrectedSpectrumHisto.GetYaxis().SetTitleOffset(UncorrectedSpectrumHisto.GetYaxis().GetTitleOffset())
  CorrectedSpectrumHisto.GetYaxis().SetLabelSize(UncorrectedSpectrumHisto.GetYaxis().GetLabelSize())
  CorrectedSpectrumHisto.SetLineColor(UncorrectedSpectrumHisto.GetLineColor())
  for iBin in range(UncorrectedSpectrumHisto.GetNbinsX()):
    CorrectedSpectrumHisto.SetBinContent(iBin, UncorrectedSpectrumHisto.GetBinContent(iBin) 
                                    / FiberProfile.Interpolate(UncorrectedSpectrumHisto.GetBinCenter(iBin)))
    
  return CorrectedSpectrumHisto
  
# Read in the UV response of the photodiode cell and return it as a TGraphErrors object
def GetPDResponse_UV():
  Wavelength = []
  Responsivity = []
  Zeros = []
  RespUnc = []
  
  # Assume the first line is a header so skip it, step over the rest of the file...
  for line in open('NIST_photodiode_calibration.csv').readlines()[1:]:
    fields = map(float, line.split(','))
    Wavelength.append(fields[0])
    Responsivity.append(fields[1])
    Zeros.append(0.)
    RespUnc.append(0.01 * fields[3] * fields[1])

  # Convert these lists to arrays
  Wavelength = array.array("f", Wavelength)
  Responsivity = array.array("f", Responsivity)
  Zeros = array.array("f", Zeros)
  RespUnc = array.array("f", RespUnc)
  
  # Build and appropriately lable a TGraphErrors object, then return it
  UVRespFuncGraph = ROOT.TGraphErrors(len(Wavelength), Wavelength, Responsivity, Zeros, RespUnc)
  UVRespFuncGraph.SetName("UVRespFuncGraph")
  UVRespFuncGraph.SetTitle("IRD Photodiode Response from NIST")
  UVRespFuncGraph.GetXaxis().SetTitle("Wavelength [nm]")
  UVRespFuncGraph.GetYaxis().SetTitle("Photodiode Response [A/W]")
  return UVRespFuncGraph

# Read in the visible response of the photodiode cell and return it as a TGraphErrors object
def GetPDResponse_Vis():
  Wavelength = []
  Responsivity = []
  Zeros = []
  RespUnc = []
  
  # Assume the first line is a header so skip it, step over the rest of the file...
  for line in open('IRD_photodiode_calibration.csv').readlines()[1:]:
    fields = map(float, line.split(','))
    Wavelength.append(fields[0])
    Responsivity.append(fields[1])
    Zeros.append(0.)
    RespUnc.append(0.01 * fields[2] * fields[1])

  # Convert these lists to arrays
  Wavelength = array.array("f", Wavelength)
  Responsivity = array.array("f", Responsivity)
  Zeros = array.array("f", Zeros)
  RespUnc = array.array("f", RespUnc)

  # Build and appropriately lable a TGraphErrors object, then return it
  VisRespFuncGraph = ROOT.TGraphErrors(len(Wavelength), Wavelength, Responsivity, Zeros, RespUnc)
  VisRespFuncGraph.SetName("VisRespFuncGraph")
  VisRespFuncGraph.SetTitle("IRD Photodiode Response from IRD")
  VisRespFuncGraph.GetXaxis().SetTitle("Wavelength [nm]")
  VisRespFuncGraph.GetYaxis().SetTitle("Photodiode Response [A/W]")
  return VisRespFuncGraph

# Compute the rate of UV photons on the photodiode as a function of input wavelength
def GetUVRateGraph(LampCurrentGraph, DarkCurrentGraph, PDUVEffGraph):
  # LampCurrentGraph: TGraphErrors object containing the pAmeter data for the lamp shining on the 
  #                   photodiode through the open space in the filter wheel
  # DarkCurrentGraph: TGraphErrors object containing the pAmeter data for the lamp blocked by the 
  #                   opaque disk in the filter wheel blocking the photodiode
  # PDUVEffGraph: TGraphErrors object containing the photodiode UV light response function

  # Arrays to hold all the things I'm calculating
  UVPhotonWavelength = []
  UVPhotonWavelengthUnc = []
  UVPhotonRate = []
  UVPhotonRateUnc = []
  # hc for the photon energy
  hc = 1240. * 1.6022e-19
  #   eV x nm   J / eV
  # A ROOT TF1 object to be the monochromator response
  MonoChrResp = ROOT.TF1("MonoChrResp", "TMath::Exp(-1. * ((x - [0])^2) / (2. * ([1]^2))) / ([1] * TMath::Sqrt(2. * TMath::Pi()))", 50., 350.)
  MonoChrResp.SetParameter(0, LampCurrentGraph.GetX()[0])
  MonoChrResp.SetParameter(1, LampCurrentGraph.GetEX()[0])
  #MonoChrResp.Draw()
  #raw_input()
  
  # Step over the input wavelength array
  for iwl in range(0, LampCurrentGraph.GetN()):
    UVPhotonWavelength.append(LampCurrentGraph.GetX()[iwl])
    UVPhotonWavelengthUnc.append(LampCurrentGraph.GetEX()[iwl])
    UVPR = (LampCurrentGraph.GetY()[iwl] - DarkCurrentGraph.GetY()[iwl]) * 1.e-9#Convert nA to A
    #Initialize the denominator before integrating over the monochromator spectrum
    UVPRDenom = 0.
    UVPRDenomUncSq = 0.
    MonoChrResp.SetParameter(0, LampCurrentGraph.GetX()[iwl])
    MonoChrResp.SetParameter(1, LampCurrentGraph.GetEX()[iwl])
    #Integrate the denominator of the UV photon rate over the monochromator spectrum and PD response
    for jwl in range(0, PDUVEffGraph.GetN()):
      UVPRDenom += (hc / PDUVEffGraph.GetX()[jwl]) * PDUVEffGraph.GetY()[jwl] * MonoChrResp.Eval(PDUVEffGraph.GetX()[jwl])
      UVPRDenomUncSq += (PDUVEffGraph.GetEY()[jwl] * (hc / PDUVEffGraph.GetX()[jwl]) * MonoChrResp.Eval(PDUVEffGraph.GetX()[jwl]))**2.
    #Divide through by denominator and attache it to the list we are building
    UVPR /= UVPRDenom
    UVPhotonRate.append(UVPR)
    UVPRDenomUnc = UVPRDenomUncSq**0.5
    UVPRUnc = ((1.e-9 * LampCurrentGraph.GetEY()[iwl] / UVPRDenom)**2.) + ((1.e-9 * DarkCurrentGraph.GetEY()[iwl] / UVPRDenom)**2.) + ((UVPRDenomUnc * UVPR / UVPRDenom)**2.)
    UVPhotonRateUnc.append(UVPRUnc**0.5)
    #print UVPhotonRate[iwl],"+/-", UVPhotonRateUnc[iwl], "ultraviolet photons for input wavelength of", UVPhotonWavelength[iwl], "nm."

  # Turn turn all these python lists into arrays
  UVPhotonWavelength = array.array("f", UVPhotonWavelength)
  UVPhotonWavelengthUnc = array.array("f", UVPhotonWavelengthUnc)
  UVPhotonRate = array.array("f", UVPhotonRate)
  UVPhotonRateUnc = array.array("f", UVPhotonRateUnc)

  # Create a TGraphErrors object for the UV photon rate to ship back
  UVRateGraph = ROOT.TGraphErrors(LampCurrentGraph.GetN(), UVPhotonWavelength, UVPhotonRate, 
                                                        UVPhotonWavelengthUnc, UVPhotonRateUnc)
  #UVRateGraph.Draw("alp")
  #raw_input()
  
  return UVRateGraph
  
# Compute the rate of visible photons on the photodiode as a function of input wavelength
def GetVisRateGraph(SampleCurrentGraph, DarkCurrentGraph, PDVisEffGraph, 
                        SpectrumHisto125nm, SpectrumHisto160nm, SpectrumHisto175nm, SpectrumHisto245nm):
  # SampleCurrentGraph: TGraphErrors object containing the pAmeter data for the lamp shining on the 
  #                     sample film and the re-emitted light being viewed by the photodiode
  # DarkCurrentGraph: TGraphErrors object containing the pAmeter data for the lamp blocked by the 
  #                   opaque disk in the filter wheel blocking the photodiode
  # PDVisEffGraph: TGraphErrors object containing the photodiode visible light response function
  # SpectrumHisto125nm: TH1D object containing the corrected re-emission spectrum of the sample film 
  #                     when illuminated by 125 nm light from the monochromator
  # SpectrumHisto160nm: TH1D object containing the corrected re-emission spectrum of the sample film 
  #                     when illuminated by 160 nm light from the monochromator
  # SpectrumHisto175nm: TH1D object containing the corrected re-emission spectrum of the sample film 
  #                     when illuminated by 175 nm light from the monochromator
  # SpectrumHisto245nm: TH1D object containing the corrected re-emission spectrum of the sample film 
  #                     when illuminated by 245 nm light from the monochromator
  
  # Arrays to hold all the things I'm calculating
  UVPhotonWavelength = []
  UVPhotonWavelengthUnc = []
  VisPhotonRate = []
  VisPhotonRateUnc = []
  
  # hc for the photon energy
  hc = 1240. * 1.6022e-19
  #   eV x nm   J / eV
  
  # Value of the geometric efficiency from Stan's ray tracing Monte Carlo
  GeomEff = 0.01795
  GeomEffUnc = 0.#We might change this later...
  
  # Pick the range over which to integrate the visible PD response times the re-emission spectrum
  VisWLRangeLo = 350.
  VisWLRangeHi = 700.
  VisWLBinLo = 0
  VisWLBinHi = 0
  for jwl in range(0, PDVisEffGraph.GetN()):
    if ((PDVisEffGraph.GetX()[jwl] > VisWLRangeLo) & (VisWLBinLo == 0)):
      VisWLBinLo = jwl
    if ((PDVisEffGraph.GetX()[jwl] > VisWLRangeHi) & (VisWLBinHi == 0)):
      VisWLBinHi = jwl
  #print "Integrating Visble photodiode efficiency from bins", VisWLBinLo, "to", VisWLBinHi
  
  # Calculate the uncertainty in the film re-emission spectrum from the RMS at short wavelength
  VisSpecUnc125nm = GetTH1DRMS(310., 360., SpectrumHisto125nm)
  VisSpecUnc160nm = GetTH1DRMS(310., 360., SpectrumHisto160nm)
  VisSpecUnc175nm = GetTH1DRMS(310., 360., SpectrumHisto175nm)
  VisSpecUnc245nm = GetTH1DRMS(310., 360., SpectrumHisto245nm)
  #print "Re-emission spectrum uncertainties:", VisSpecUnc125nm, VisSpecUnc160nm, VisSpecUnc175nm, VisSpecUnc245nm

  # Set up the range over which we will use each re-emission spectrum
  Switch_125_160 = float(125. + (0.5 * (160. - 125.)))
  Switch_160_175 = float(160. + (0.5 * (175. - 160.)))
  Switch_175_245 = float(175. + (0.5 * (245. - 175.)))
  # Step over the input wavelength array
  for iwl in range(0, SampleCurrentGraph.GetN()):
    UVPhotonWavelength.append(SampleCurrentGraph.GetX()[iwl])
    UVPhotonWavelengthUnc.append(SampleCurrentGraph.GetEX()[iwl])
    VisPR =  (SampleCurrentGraph.GetY()[iwl] - DarkCurrentGraph.GetY()[iwl]) * 1.e-9 / GeomEff#The "1.e-9" is to convert nA to A
    #Initialize the denominator before integrating over the re-emission spectrum
    VisPRDenom = 0.
    VisPRDenomUncSq1 = 0.
    VisPRDenomUncSq2 = 0.
    # If in appropriate input wavelength range, integrate over 125 nm re-emission spectrum
    if(UVPhotonWavelength[iwl] < Switch_125_160):
      for jwl in range(VisWLBinLo, VisWLBinHi):
        VisPRDenom += (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl] * SpectrumHisto125nm.Interpolate(PDVisEffGraph.GetX()[jwl])
        VisPRDenomUncSq1 += (PDVisEffGraph.GetEY()[jwl] * (hc / PDVisEffGraph.GetX()[jwl]) * SpectrumHisto125nm.Interpolate(PDVisEffGraph.GetX()[jwl]))**2.
        VisPRDenomUncSq2 += (VisSpecUnc125nm * (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl])**2.
    # If in appropriate input wavelength range, integrate over 160 nm re-emission spectrum
    if((UVPhotonWavelength[iwl] >= Switch_125_160) & (UVPhotonWavelength[iwl] < Switch_160_175)):
      for jwl in range(VisWLBinLo, VisWLBinHi):
        VisPRDenom += (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl] * SpectrumHisto160nm.Interpolate(PDVisEffGraph.GetX()[jwl])
        VisPRDenomUncSq1 += (PDVisEffGraph.GetEY()[jwl] * (hc / PDVisEffGraph.GetX()[jwl]) * SpectrumHisto160nm.Interpolate(PDVisEffGraph.GetX()[jwl]))**2.
        VisPRDenomUncSq2 += (VisSpecUnc160nm * (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl])**2.
    # If in appropriate input wavelength range, integrate over 175 nm re-emission spectrum
    if((UVPhotonWavelength[iwl] >= Switch_160_175) & (UVPhotonWavelength[iwl] < Switch_175_245)):
      for jwl in range(VisWLBinLo, VisWLBinHi):
        VisPRDenom += (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl] * SpectrumHisto175nm.Interpolate(PDVisEffGraph.GetX()[jwl])
        VisPRDenomUncSq1 += (PDVisEffGraph.GetEY()[jwl] * (hc / PDVisEffGraph.GetX()[jwl]) * SpectrumHisto175nm.Interpolate(PDVisEffGraph.GetX()[jwl]))**2.
        VisPRDenomUncSq2 += (VisSpecUnc175nm * (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl])**2.
    # If in appropriate input wavelength range, integrate over 245 nm re-emission spectrum
    if(UVPhotonWavelength[iwl] >= Switch_175_245):
      for jwl in range(VisWLBinLo, VisWLBinHi):
        VisPRDenom += (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl] * SpectrumHisto245nm.Interpolate(PDVisEffGraph.GetX()[jwl])
        VisPRDenomUncSq1 += (PDVisEffGraph.GetEY()[jwl] * (hc / PDVisEffGraph.GetX()[jwl]) * SpectrumHisto245nm.Interpolate(PDVisEffGraph.GetX()[jwl]))**2.
        VisPRDenomUncSq2 += (VisSpecUnc245nm * (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl])**2.
    #Divide through by denominator and attach it to the list we are building
    VisPR /= VisPRDenom
    VisPhotonRate.append(VisPR)
    VisPRDenomUnc = (VisPRDenomUncSq1 + VisPRDenomUncSq2)**0.5
    VisPRUnc = ((GeomEffUnc * VisPhotonRate[iwl] / GeomEff)**2.) + ((1.e-9 * SampleCurrentGraph.GetEY()[iwl] * GeomEff / VisPRDenom)**2.) + ((1.e-9 * DarkCurrentGraph.GetEY()[iwl] * GeomEff / VisPRDenom)**2.) + ((VisPRDenomUnc * VisPR / VisPRDenom)**2.)
    VisPhotonRateUnc.append(VisPRUnc**0.5)
    #print VisPhotonRate[iwl],"+/-", VisPhotonRateUnc[iwl], "visible photons for input wavelength of", UVPhotonWavelength[iwl], "nm."

  # Turn turn all these python lists into arrays
  UVPhotonWavelength = array.array("f", UVPhotonWavelength)
  UVPhotonWavelengthUnc = array.array("f", UVPhotonWavelengthUnc)
  VisPhotonRate = array.array("f", VisPhotonRate)
  VisPhotonRateUnc = array.array("f", VisPhotonRateUnc)

  # Create a TGraphErrors object for the UV photon rate to ship back
  VisRateGraph = ROOT.TGraphErrors(SampleCurrentGraph.GetN(), UVPhotonWavelength, VisPhotonRate, 
                                                           UVPhotonWavelengthUnc, VisPhotonRateUnc)
  #VisRateGraph.Draw("alp")
  #raw_input()
  
  return VisRateGraph

# Compute the rate of visible photons on the photodiode as a function of input wavelength using only
# one visible spectrum for all input wavelengths
def GetVisRateGraph(SampleCurrentGraph, DarkCurrentGraph, PDVisEffGraph, VisSpectrumHisto):
  # SampleCurrentGraph: TGraphErrors object containing the pAmeter data for the lamp shining on the 
  #                     sample film and the re-emitted light being viewed by the photodiode
  # DarkCurrentGraph: TGraphErrors object containing the pAmeter data for the lamp blocked by the 
  #                   opaque disk in the filter wheel blocking the photodiode
  # PDVisEffGraph: TGraphErrors object containing the photodiode visible light response function
  # VisSpectrumHisto: TH1D object containing the corrected re-emission spectrum of the sample film 
  
  # Arrays to hold all the things I'm calculating
  UVPhotonWavelength = []
  UVPhotonWavelengthUnc = []
  VisPhotonRate = []
  VisPhotonRateUnc = []
  
  # hc for the photon energy
  hc = 1240. * 1.6022e-19
  #   eV x nm   J / eV
  
  # Value of the geometric efficiency from Stan's ray tracing Monte Carlo
  GeomEff = 0.01795
  GeomEffUnc = 0.#We might change this later...
  
  # Pick the range over which to integrate the visible PD response times the re-emission spectrum
  VisWLRangeLo = 350.
  VisWLRangeHi = 700.
  VisWLBinLo = 0
  VisWLBinHi = 0
  for jwl in range(0, PDVisEffGraph.GetN()):
    if ((PDVisEffGraph.GetX()[jwl] > VisWLRangeLo) & (VisWLBinLo == 0)):
      VisWLBinLo = jwl
    if ((PDVisEffGraph.GetX()[jwl] > VisWLRangeHi) & (VisWLBinHi == 0)):
      VisWLBinHi = jwl
  #print "Integrating Visble photodiode efficiency from bins", VisWLBinLo, "to", VisWLBinHi
  
  # Calculate the uncertainty in the film re-emission spectrum from the RMS at short wavelength
  VisSpecUnc = GetTH1DRMS(310., 360., VisSpectrumHisto)

  # Step over the input wavelength array
  for iwl in range(0, SampleCurrentGraph.GetN()):
    UVPhotonWavelength.append(SampleCurrentGraph.GetX()[iwl])
    UVPhotonWavelengthUnc.append(SampleCurrentGraph.GetEX()[iwl])
    VisPR =  (SampleCurrentGraph.GetY()[iwl] - DarkCurrentGraph.GetY()[iwl]) * 1.e-9 / GeomEff#The "1.e-9" is to convert nA to A
    #Initialize the denominator before integrating over the re-emission spectrum
    VisPRDenom = 0.
    VisPRDenomUncSq1 = 0.
    VisPRDenomUncSq2 = 0.
    for jwl in range(VisWLBinLo, VisWLBinHi):
      VisPRDenom += (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl] * VisSpectrumHisto.Interpolate(PDVisEffGraph.GetX()[jwl])
      VisPRDenomUncSq1 += (PDVisEffGraph.GetEY()[jwl] * (hc / PDVisEffGraph.GetX()[jwl]) * VisSpectrumHisto.Interpolate(PDVisEffGraph.GetX()[jwl]))**2.
      VisPRDenomUncSq2 += (VisSpecUnc * (hc / PDVisEffGraph.GetX()[jwl]) * PDVisEffGraph.GetY()[jwl])**2.
    #Divide through by denominator and attach it to the list we are building
    VisPR /= VisPRDenom
    VisPhotonRate.append(VisPR)
    VisPRDenomUnc = (VisPRDenomUncSq1 + VisPRDenomUncSq2)**0.5
    VisPRUnc = ((GeomEffUnc * VisPhotonRate[iwl] / GeomEff)**2.) + ((1.e-9 * SampleCurrentGraph.GetEY()[iwl] * GeomEff / VisPRDenom)**2.) + ((1.e-9 * DarkCurrentGraph.GetEY()[iwl] * GeomEff / VisPRDenom)**2.) + ((VisPRDenomUnc * VisPR / VisPRDenom)**2.)
    VisPhotonRateUnc.append(VisPRUnc**0.5)
    #print VisPhotonRate[iwl],"+/-", VisPhotonRateUnc[iwl], "visible photons for input wavelength of", UVPhotonWavelength[iwl], "nm."

  # Turn turn all these python lists into arrays
  UVPhotonWavelength = array.array("f", UVPhotonWavelength)
  UVPhotonWavelengthUnc = array.array("f", UVPhotonWavelengthUnc)
  VisPhotonRate = array.array("f", VisPhotonRate)
  VisPhotonRateUnc = array.array("f", VisPhotonRateUnc)

  # Create a TGraphErrors object for the UV photon rate to ship back
  VisRateGraph = ROOT.TGraphErrors(SampleCurrentGraph.GetN(), UVPhotonWavelength, VisPhotonRate, 
                                                           UVPhotonWavelengthUnc, VisPhotonRateUnc)
  #VisRateGraph.Draw("alp")
  #raw_input()
  
  return VisRateGraph

# Calculate the RMS of a TH1D object over a user defined range
def GetTH1DRMS(LoVal, HiVal, Histo):
  LoBin = Histo.FindBin(LoVal)
  HiBin = Histo.FindBin(HiVal)
  SpecAvg = 0.
  SpecSqAvg = 0.

  for iBin in range(LoBin, HiBin):
    SpecAvg += Histo.GetBinContent(iBin) / float(HiBin - LoBin)
    SpecSqAvg += (Histo.GetBinContent(iBin)**2.) / float(HiBin - LoBin)

  SpecRMS = (SpecSqAvg - (SpecAvg**2.))**0.5
  
  return SpecRMS
  
# Here are the efficiency calculation tools I got from Stan.  Hopefully, they will work better than 
# mine did...
def energy_per_photon(wavelength):
    '''Returns energy in J for photon wavelength in units of nm'''
    return 6.62606896E-34 * 299792458/(wavelength*1e-9)

def create_graph_from_file(filename, ycol=1):
    '''Assumes first line is header and skips it.  Works for space or comma delimited fields.
    First column in file will be x, and second column will be y.
    
      ycol: Override selection of y column.  Starts counting from zero.
    '''
    x = []
    y = []
    for line in open(filename).readlines()[1:]:
        fields = line.replace(',', ' ').split()
        x.append(float(fields[0]))
        y.append(float(fields[ycol]))
    x = numpy.array(x)
    y = numpy.array(y)
    return ROOT.TGraph(len(x), x, y)
    

def get_corrected_TPB_spectrum(pathtofile, histoname):
    f = ROOT.TFile.Open(pathtofile)
    h = f.Get(histoname)
    h.SetDirectory(0)
    f.Close()
    return h

def get_uncorrected_TPB_spectrum(pathtofile, histoname):
    f = ROOT.TFile.Open(pathtofile)
    h = f.Get(histoname)
    h.SetDirectory(0)
    f.Close()
    return h

def uv_efficiency(wavelength, monochrometer_sigma, NIST_photodiode_calibration, NIST_photodiode_calibration_uncert):
    '''Compute the UV responsivity coefficient (UV photons per second per amp)
    
       wavelength: numpy array of wavelength values
       monochrometer_sigma: RMS of monochrometer wavelength distribution
       NIST_photodiode_calibration: TGraph of A/W calibration for photodiode in the UV range
       NIST_photodiode_calibration_uncert: TGraph of uncertainties (in %) of NIST calibration
                                           used to compute an average uncert for integral
       Returns: tuple of (UV efficiency for all the wavelengths in the wavelength array, fractional uncertainties on efficiency)
                NOTE UNCERT IS FRACTIONAL, NOT PERCENT LIKE THE INPUT GRAPH
    '''
    photo_uv_efficiency = numpy.zeros_like(wavelength)
    photo_uv_efficiency_uncert = numpy.zeros_like(wavelength)

    for index, wl in enumerate(wavelength):
        sum_response = 0.0
        sum_response_percent_uncert = 0.0
        norm = 0.0        
        for tmp_wl in numpy.arange(wl - 3*monochrometer_sigma, wl + 3*monochrometer_sigma, monochrometer_sigma/100.0):
            spectrum_intensity = ROOT.TMath.Gaus(tmp_wl, wl, monochrometer_sigma, True)
            sum_response += NIST_photodiode_calibration.Eval(tmp_wl) * spectrum_intensity * energy_per_photon(tmp_wl)
            sum_response_percent_uncert += NIST_photodiode_calibration_uncert.Eval(tmp_wl) * spectrum_intensity
            norm += spectrum_intensity
            
        photo_uv_efficiency[index] = sum_response/norm
        photo_uv_efficiency_uncert[index] = sum_response_percent_uncert/norm/100.0 # Convert percent to fraction
    
    return photo_uv_efficiency, photo_uv_efficiency_uncert

def vis_efficiency(tpb_spectrum, IRD_photodiode_calibration, IRD_photodiode_calibration_uncert):
    '''Compute the visible responsivity coefficiency (vis photons per second per amp)
    
      tpb_spectrum: TH1 of TPB reemission spectrum
      IRD_photodiode_calibration: TGraph of A/W calibration for photodiode in the visible range
      IRD_photodiode_calibration_uncert: TGrahp of uncertainties (in %) of IRD calibration
      
      Returns: tuple of scalars (vis_efficiency, vis_efficiency_fractional_uncert)
               NOTE UNCERT IS FRACTIONAL, NOT PERCENT LIKE INPUT GRAPH
    '''
    
    # Average photodiode response over reemission spectrum
    sum_response = 0.0
    sum_response_percent_uncert = 0.0
    norm = 0.0
    for wl in numpy.arange(350.0, 650.0, 0.1):
        spectrum_intensity = tpb_spectrum.Interpolate(wl)
        sum_response += IRD_photodiode_calibration.Eval(wl) * spectrum_intensity * energy_per_photon(wl)
        sum_response_percent_uncert += IRD_photodiode_calibration_uncert.Eval(wl) * spectrum_intensity
        norm += spectrum_intensity

    return (sum_response/norm, sum_response_percent_uncert/norm/100.0)

def compute_eff(pdcurrentfile, name, wavelength_col, dark_col, lamp_start_col, tpb_col, lamp_stop_col, forward_eff=False):
    wavelength = []
    lamp_start = []
    dark = []
    tpb = []
    lamp_stop = []

    ## Read the required columns from the text file
    line_number = 0
    for line in open(pdcurrentfile).readlines()[1:]:
        fields = line.split(',')
        if float(fields[0]) < 117.0:
          continue
        
        # Only keep points on 10 nm values due to size of FWHM
        if float(fields[0])/10.0 - int(float(fields[0])/10.0) > 0.1:
            continue
        
        for index, values in [ (wavelength_col, wavelength),
                               (lamp_start_col, lamp_start),
                               (dark_col, dark),
                               (tpb_col, tpb),
                               (lamp_stop_col, lamp_stop)]:
            values.append(float(fields[index]))

    ## Convert the lists to numpy arrays for mathematical convenience
    wavelength = numpy.array(wavelength)
    
    # Find index of element closest to 130 nm.  We will print uncerts for this value as we go
    index_130nm = abs(wavelength - 130.0).argmin()
    
    lamp_start = numpy.array(lamp_start)
    dark = numpy.array(dark)
    tpb = numpy.array(tpb)
    lamp_stop = numpy.array(lamp_stop)

    ## Compute raw intensity ratio using average lamp intensity, removing dark current
    average_lamp_intensity = (lamp_start + lamp_stop)/2 - dark 
    efficiency = (tpb - dark) / average_lamp_intensity

    uncert_dark = numpy.std(dark)
    print "Frac uncert dark @ 130nm:", (uncert_dark/average_lamp_intensity)[index_130nm]
    uncert_tpb = uncert_dark
    # Taken from change in 120 nm current separated by 5 measurement rows
    uncert_average_lamp = 2 * uncert_dark
    frac_uncert_time_lamp = (2 * (0.14035 - 0.13849) / (0.14035 + 0.13849)) / 5
    print "Short time variation uncertainty in lamp (frac) @ 130nm:", frac_uncert_time_lamp

    # Frac uncert in dark subtracted TPB combined with uncert in lamp intensity and time variation in lamp
    efficiency_frac_uncert = sqrt( ((2 * uncert_dark) / (tpb - dark))**2 + (uncert_average_lamp/average_lamp_intensity)**2 + frac_uncert_time_lamp**2 )

    print 'Statistical uncertainty @ 130nm:', sqrt(efficiency_frac_uncert[index_130nm]**2 - frac_uncert_time_lamp**2)

    ## Scale factor: Photodiode UV efficiency
    
    monochrometer_fwhm = 8.5 # nm (10.4 nm measured, subtract 6 nm spectrometer resolution in quadrature)
    monochrometer_sigma = monochrometer_fwhm / 2.3548 # See Mathworld "Gaussian Function"
    monochrometer_sigma_uncert = 0.5 / 2.3548
    
    # load efficiency table
    NIST_photodiode_calibration = create_graph_from_file('NIST_photodiode_calibration.csv')
    # We load this separately so we can interpolate the errors to evaluate the uncert on the integral
    NIST_photodiode_calibration_uncert = create_graph_from_file('NIST_photodiode_calibration.csv', ycol=3)

    # Fill array with scale factors, integrating over the width of the Monochrometer spectrum
    photo_uv_efficiency, photo_uv_frac_uncert = uv_efficiency(wavelength, monochrometer_sigma, NIST_photodiode_calibration, NIST_photodiode_calibration_uncert)
    # Add uncert from uncertainties in the width of the monochrometer emission spectrum
    photo_uv_frac_uncert += abs( photo_uv_efficiency 
       - uv_efficiency(wavelength, monochrometer_sigma+monochrometer_sigma_uncert, NIST_photodiode_calibration, NIST_photodiode_calibration_uncert)[0] ) / photo_uv_efficiency

    print 'UV calibration uncert @ 130nm:', photo_uv_frac_uncert[index_130nm]

    efficiency *= photo_uv_efficiency
    efficiency_frac_uncert = sqrt(efficiency_frac_uncert**2 + photo_uv_frac_uncert**2)


    ## Scale factor: Photodiode visible efficiency
    # Load TPB reemission spectrum and IRD calibration table
    tpb_spectrum = get_corrected_TPB_spectrum("FluorescenceSpectrumCmp.root", "VisSpec_160nm_Corrected")
    tpb_spectrum_uncorrected = get_uncorrected_TPB_spectrum("MyPaint_160nm.root", "DarkCorrectedHist")
    IRD_photodiode_calibration = create_graph_from_file('IRD_photodiode_calibration.csv')
    IRD_photodiode_calibration_uncert = create_graph_from_file('IRD_photodiode_calibration.csv', ycol=2)

    # Average photodiode response over reemission spectrum
    photo_vis_efficiency, photo_vis_efficiency_frac_uncert = vis_efficiency(tpb_spectrum, IRD_photodiode_calibration, IRD_photodiode_calibration_uncert)
    # Add uncert in spectral shape by taking entire distortion from acrylic and optics as uncert
    photo_vis_efficiency_frac_uncert += abs(vis_efficiency(tpb_spectrum_uncorrected, IRD_photodiode_calibration, IRD_photodiode_calibration_uncert)[0] -
                                            photo_vis_efficiency) / photo_vis_efficiency

    print 'Vis calibration uncert @ 130nm:', photo_vis_efficiency_frac_uncert

    efficiency /= photo_vis_efficiency
    efficiency_frac_uncert = sqrt(efficiency_frac_uncert**2 + photo_vis_efficiency_frac_uncert**2)

    ## Scale factor: geometric factor
    
    if not forward_eff:
        # Assumption: Point source of light at diffraction grating with double lambertian 
        #             reemission at TPB and negligible reflections
        vis_geo_factor = 0.01795
        vis_geo_frac_uncert = numpy.zeros_like(wavelength)
    else:
        vis_geo_factor = 1.0
        vis_geo_frac_uncert = numpy.zeros_like(wavelength)

    # Cast up to numpy arr
    efficiency /= vis_geo_factor 
    efficiency_frac_uncert = sqrt(efficiency_frac_uncert**2 + vis_geo_frac_uncert**2)

    print 'Geometric factor uncert @ 130nm:', vis_geo_frac_uncert[index_130nm]
    print 'Sum fractional uncert @ 130nm:', efficiency_frac_uncert[index_130nm]



    dummy_zeros = numpy.zeros(len(wavelength))
    eff_graph = ROOT.TGraphErrors(len(wavelength), wavelength, efficiency,
                                  dummy_zeros, efficiency * efficiency_frac_uncert)
    eff_graph.SetTitle(';Wavelength (nm);Efficiency (# of vis photons/UV photon)')
    #eff_graph.GetHistogram().SetMinimum(0.5)
    eff_graph.SetName(name)                              
    return eff_graph
    
def compute_eff_unc(pdcurrentfile, name,  tpb_spectrum, tpb_spectrum_uncorrected, wavelength_col, dark_col, dark_unc_col, lamp_start_col, lamp_start_unc_col, tpb_col, tpb_unc_col, lamp_stop_col, lamp_stop_unc_col, forward_eff=False): 
    wavelength = []
    lamp_start = []
    lamp_start_unc = []
    dark = []
    dark_unc = []
    tpb = []
    tpb_unc = []
    lamp_stop = []
    lamp_stop_unc = []

    ## Read the required columns from the text file
    line_number = 0
    for line in open(pdcurrentfile).readlines()[1:]:
        fields = line.split(',')
        if float(fields[0]) < 29.0: #Default at 117. Why is this number important?
            continue
        
        # Only keep points on 10 nm values due to size of FWHM
#         if float(fields[0])/10.0 - int(float(fields[0])/10.0) > 0.1:
#         		print 'Skipping '+str(fields[0])
#         		continue

        for index, values in [ (wavelength_col, wavelength),
                               (lamp_start_col, lamp_start),
                               (lamp_start_unc_col, lamp_start_unc),
                               (dark_col, dark),
                               (dark_unc_col, dark_unc),
                               (tpb_col, tpb),
                               (tpb_unc_col, tpb_unc),
                               (lamp_stop_col, lamp_stop),
                               (lamp_stop_unc_col, lamp_stop_unc)]:
            values.append(float(fields[index]))

    #print "There seem to be", len(wavelength), "data points to consider."
    #print "Wavelength\tLamp Current [nA]\tDark Current [nA]\tWLS Current [nA]"
    #for i in range(len(wavelength)):
    #  print wavelength[i], "\t", lamp_start[i], "+/-", lamp_start_unc[i], "\t", dark[i], "+/-", dark_unc[i], "\t", tpb[i], "+/-", tpb_unc[i]

    ## Convert the lists to numpy arrays for mathematical convenience
    wavelength = numpy.array(wavelength)
    
    # Find index of element closest to 130 nm.  We will print uncerts for this value as we go
    index_130nm = abs(wavelength - 130.0).argmin()
    
    lamp_start = numpy.array(lamp_start)
    lamp_start_unc = numpy.array(lamp_start_unc)
    dark = numpy.array(dark)
    dark_unc = numpy.array(dark_unc)
    tpb = numpy.array(tpb)
    tpb_unc = numpy.array(tpb_unc)
    lamp_stop = numpy.array(lamp_stop)
    lamp_stop_unc = numpy.array(lamp_stop_unc)

    ## Compute raw intensity ratio using average lamp intensity, removing dark current
    average_lamp_intensity = (lamp_start + lamp_stop)/2 - dark 
    efficiency = (tpb - dark) / average_lamp_intensity
    print "Frac uncert dark @ 130nm:", (dark_unc/average_lamp_intensity)[index_130nm]
    # Taken from change in 120 nm current separated by 5 measurement rows--taken in 2011
    uncert_average_lamp = 2 * lamp_start_unc
    frac_uncert_time_lamp = (2 * (0.14035 - 0.13849) / (0.14035 + 0.13849)) / 5
    print "Short time variation uncertainty in lamp (frac) @ 130nm:", frac_uncert_time_lamp

    # Frac uncert in dark subtracted TPB combined with uncert in lamp intensity and time variation in lamp
    efficiency_frac_uncert = sqrt( ((tpb_unc) / (tpb - dark))**2 + ((dark_unc) / (tpb - dark))**2 + (uncert_average_lamp/average_lamp_intensity)**2 + frac_uncert_time_lamp**2 )

    print 'Statistical uncertainty @ 130nm:', sqrt(efficiency_frac_uncert[index_130nm]**2 - frac_uncert_time_lamp**2)

    ## Scale factor: Photodiode UV efficiency
    
    monochrometer_fwhm = 8.5 # nm (10.4 nm measured, subtract 6 nm spectrometer resolution in quadrature)
    monochrometer_sigma = monochrometer_fwhm / 2.3548 # See Mathworld "Gaussian Function"
    monochrometer_sigma_uncert = 0.5 / 2.3548
    
    # load efficiency table
    NIST_photodiode_calibration = create_graph_from_file('depend/NIST_photodiode_calibration.csv')
    # We load this separately so we can interpolate the errors to evaluate the uncert on the integral
    NIST_photodiode_calibration_uncert = create_graph_from_file('depend/NIST_photodiode_calibration.csv', ycol=3)

    # Fill array with scale factors, integrating over the width of the Monochrometer spectrum
    photo_uv_efficiency, photo_uv_frac_uncert = uv_efficiency(wavelength, monochrometer_sigma, NIST_photodiode_calibration, NIST_photodiode_calibration_uncert)
    # Add uncert from uncertainties in the width of the monochrometer emission spectrum
    photo_uv_frac_uncert += abs( photo_uv_efficiency 
       - uv_efficiency(wavelength, monochrometer_sigma+monochrometer_sigma_uncert, NIST_photodiode_calibration, NIST_photodiode_calibration_uncert)[0] ) / photo_uv_efficiency
    print 'UV calibration uncert @ 130nm:', photo_uv_frac_uncert[index_130nm]

    efficiency *= photo_uv_efficiency
    efficiency_frac_uncert = sqrt(efficiency_frac_uncert**2 + photo_uv_frac_uncert**2)


    ## Scale factor: Photodiode visible efficiency
    # Load TPB reemission spectrum and IRD calibration table
    #tpb_spectrum = get_corrected_TPB_spectrum("/Users/vmgehman/Documents/UVOptics/MyPaint/FluorescenceSpectrumCmp.root", "VisSpec_160nm_Corrected")
    #tpb_spectrum_uncorrected = get_uncorrected_TPB_spectrum("/Users/vmgehman/Documents/UVOptics/MyPaint/160nm/MyPaint_160nm.root", "DarkCorrectedHist")
    IRD_photodiode_calibration = create_graph_from_file('depend/IRD_photodiode_calibration.csv')
    IRD_photodiode_calibration_uncert = create_graph_from_file('depend/IRD_photodiode_calibration.csv', ycol=2)

    # Average photodiode response over reemission spectrum
    photo_vis_efficiency, photo_vis_efficiency_frac_uncert = vis_efficiency(tpb_spectrum, IRD_photodiode_calibration, IRD_photodiode_calibration_uncert)
    # Add uncert in spectral shape by taking entire distortion from acrylic and optics as uncert
    photo_vis_efficiency_frac_uncert += abs(vis_efficiency(tpb_spectrum_uncorrected, IRD_photodiode_calibration, IRD_photodiode_calibration_uncert)[0] -
                                            photo_vis_efficiency) / photo_vis_efficiency

    print 'Vis calibration uncert @ 130nm:', photo_vis_efficiency_frac_uncert

    efficiency /= photo_vis_efficiency
    efficiency_frac_uncert = sqrt(efficiency_frac_uncert**2 + photo_vis_efficiency_frac_uncert**2)

    ## Scale factor: geometric factor
    
    if not forward_eff:
        # Assumption: Point source of light at diffraction grating with double lambertian 
        #             reemission at TPB and negligible reflections
        vis_geo_factor = 0.01795
        vis_geo_frac_uncert = numpy.zeros_like(wavelength)
    else:
        vis_geo_factor = 1.0
        vis_geo_frac_uncert = numpy.zeros_like(wavelength)

    # Cast up to numpy arr
    efficiency /= vis_geo_factor 
    efficiency_frac_uncert = sqrt(efficiency_frac_uncert**2 + vis_geo_frac_uncert**2)

    print 'Geometric factor uncert @ 130nm:', vis_geo_frac_uncert[index_130nm]
    print 'Sum fractional uncert @ 130nm:', efficiency_frac_uncert[index_130nm]



    dummy_zeros = numpy.zeros(len(wavelength))
    eff_graph = ROOT.TGraphErrors(len(wavelength), wavelength, efficiency,
                                  dummy_zeros, efficiency * efficiency_frac_uncert)
    eff_graph.SetTitle(';Wavelength (nm);Efficiency (# of vis photons/UV photon)')
    #eff_graph.GetHistogram().SetMinimum(0.5)
    eff_graph.SetName(name)                              
    return eff_graph
