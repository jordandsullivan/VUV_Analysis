import ROOT
import SpectraTools as ST
import UVLampTools as ULT

# Class for creating spectra objects for each sample.
class sample_spectra_set:
	def __init__(self,path_to_data,number_of_files,acrylic_corr=True,hist_name='default',hist_color=1,hist_line=1,leg=''):
		# Save input params as attributes
		self.path = path_to_data
		self.num_files = number_of_files
		# transmittance corrections
# 		self.fiber_transmittance = ULT.GetFiberTransmittance()
		TransmittanceFile = ROOT.TFile.Open('/Users/chrisbenson/Documents/Research/VUV/Analysis_Scripts/VUV_Tools/transmittance.root')
		self.fiber_transmittance = TransmittanceFile.Get("transmittance")
		self.acrylic_corrected = acrylic_corr
		# Histogram settings
		self.hist_color = hist_color
		self.hist_line = hist_line
		self.hist_name = hist_name
		self.legend_name = leg
		# baseline shifting settings
		self.baseline_sub_window_bottom = 750
		self.baseline_sub_window_top = 900
		
		if acrylic_corr:
			self.acrylic_transmittance = ULT.GetAcrylicTransmittance()
		else: 
			self.acrylic_transmittance = ST.NullAcrylicSpectrum()
		
		# Initialize histogram
		self.hist = ST.GetSpectrum(self.path, self.num_files, self.hist_name, self.hist_name, self.acrylic_transmittance, self.fiber_transmittance, self.hist_color, self.hist_line)

		[self.hist, self.baseline_shift] = ULT.BaselineSubtraction(self.hist, self.baseline_sub_window_bottom, self.baseline_sub_window_top)
		# Reset some of the histogram properties after baseline subtraction.
		self.hist.SetLineColor(self.hist_color)
		self.hist.SetTitle('')
		
	# Method to normalise self.hist spectrum
	def normalize_spectra(self):
		self.hist = ST.NormalizeSpectrum(self.hist)
		
	# Recreate histogram if some of the attributes have changed.
	def recreate_hist(self):
		self.hist = ST.GetSpectrum(self.path, self.num_files, self.hist_name, self.hist_name, self.acrylic_transmittance, self.fiber_transmittance, self.hist_color, self.hist_line)
		self.baseline_shift = False
		
	def shift_baseline(self):
		[self.hist, self.baseline_shift] = ULT.BaselineSubtraction(self.hist, self.baseline_sub_window_bottom, self.baseline_sub_window_top)
		self.hist.SetLineColor(self.hist_color)
		self.hist.SetTitle('')
		
		