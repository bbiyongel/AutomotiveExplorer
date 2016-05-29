import numpy as np
import scipy
import math
import globals as gb

class SignalFeatures(object):
	def __init__(self):
		# The name of features to be extracted on the derivative of the signal, must end with '_deriv'
		
		self.fmap = {
		"mean":np.mean, "median":np.median, "rms":self.rms, "std":np.std, "maximum":max, "minimum":min, "skewness":scipy.stats.skew, "kurtosis":scipy.stats.kurtosis, "dominantFreq":self.dominantFrequency, 
		"mean_deriv":np.mean, "median_deriv":np.median, "rms_deriv":self.rms, "std_deriv":np.std, "maximum_deriv":max, "minimum_deriv":min, "skewness_deriv":scipy.stats.skew, "kurtosis_deriv":scipy.stats.kurtosis, "dominantFreq_deriv":self.dominantFrequency, 
		"decrease_ratio_deriv":self.decrease_ratio, "increase_ratio_deriv":self.increase_ratio#, "histo":self.histogram, "histo_deriv":self.histogram
		}
		
		self.feature_names = self.fmap.keys()
		
	# -------------------------------------------------------------
	def dominantFrequency(self, L):
		n = 1
		w = np.fft.fft(L)
		freqs = np.fft.fftfreq(len(L))
		abs_w = [abs(v) for v in w]
		ids = sorted(range(len(abs_w)), key=lambda i: abs_w[i])[-n:] # indexes of the top n values in abs_w
		dominant_freqs = [freqs[id] for id in ids]
		
		return dominant_freqs[0]
		
	# -------------------------------------------------------------
	def decrease_ratio(self, L):
		return len([v for v in L if v < 0]) * 1. / len(L)
		
	# -------------------------------------------------------------
	def increase_ratio(self, L):
		return len([v for v in L if v > 0]) * 1. / len(L)
		
	# -------------------------------------------------------------
	def histogram(self, L, L_range=None):
		histo, _ = np.histogram( L, bins=10, range=L_range ); histo = histo.tolist()
		return [float(v) for v in histo]
		
	# -------------------------------------------------------------
	def increase_ratio(self, L):
		return len([v for v in L if v > 0]) * 1. / len(L)
		
	# -------------------------------------------------------------
	def rms(self, L):
		return np.sqrt(np.mean(np.square(L)))
		
	# -------------------------------------------------------------
	''' Extract some simple features from a timeseries '''
	def extract(self, sig_values):
		sig_values_deriv = np.gradient(sig_values)
		res = [ self.fmap[fname]( sig_values_deriv if '_deriv' in fname else sig_values ) for fname in self.feature_names]
		
		return [ float(v) for v in res ]
	
	# --------------------------------------------------------------------------------------
	''' Extract some simple features from many timeseries '''
	def extractMany(self, L_sig_values, L_sig_range=None):
		F = [ self.extract(sig_values) for sig_values in L_sig_values ]
		x = [ v for vv in F for v in vv ] # Flat list of features for all signals
		
		# '''
		if L_sig_range is not None:
			L_sig_range_orig = [ range[:2] for range in L_sig_range ]
			L_sig_range_deriv = [ range[2:] for range in L_sig_range ]
			
			histos_orig = [self.histogram(sig_values, sig_range) for (sig_values, sig_range) in zip(L_sig_values, L_sig_range_orig)]
			histos_deriv = [self.histogram(np.gradient(sig_values), sig_range) for (sig_values, sig_range) in zip(L_sig_values, L_sig_range_deriv)]
			
			x_hists = [ v for vv in histos_orig for v in vv ] + [ v for vv in histos_deriv for v in vv ]
			x += x_hists
		# '''
		
		return x
	
	# --------------------------------------------------------------------------------------
	''' Return the features name returned by the method extractMany (restricted to ids) '''
	def getFeaturesName(self, ids=None):
		signames = [ gb.SIG_NAMES[sigid] for sigid in gb.SIG_IDS ]
		all_features = []
		for signame in signames:
			for fname in self.feature_names:
				all_features.append(signame+"_"+fname)
		
		if ids is None:
			return all_features
		else:
			return [ all_features[id] for id in ids ]
	
	# --------------------------------------------------------------------------------------
	
	
	
	
	
	