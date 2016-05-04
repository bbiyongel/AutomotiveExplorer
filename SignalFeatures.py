import numpy as np
import scipy
import math
import globals as gb

class SignalFeatures(object):
	def __init__(self):
		# The name of features to be extracted on the derivative of the signal, must end with '_deriv'
		self.feature_names = [
		"mean", "median", "rms", "std", "maximum", "minimum", "skewness", "kurtosis", "dominantFreq", 
		"mean_deriv", "median_deriv", "rms_deriv", "std_deriv", "maximum_deriv", "minimum_deriv", "skewness_deriv", "kurtosis_deriv", "dominantFreq_deriv",  
		"decrease_ratio_deriv", "increase_ratio_deriv"#, "histo", "histo_deriv"
		]
		
		self.feature_funcs = [
		np.mean, np.median, self.rms, np.std, max, min, scipy.stats.skew, scipy.stats.kurtosis, self.dominantFrequency, 
		np.mean, np.median, self.rms, np.std, max, min, scipy.stats.skew, scipy.stats.kurtosis, self.dominantFrequency, 
		self.decrease_ratio, self.increase_ratio#, self.histogram, self.histogram
		]
		
		self.fmap = { fname : fcall for fname, fcall in zip(self.feature_names, self.feature_funcs) }
		
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
	def histogram(self, L):
		histo, _ = np.histogram( L, bins=3 )
		histo = histo.tolist()
		return histo
		
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
	def extractMany(self, L_sig_values):
		F = [ self.extract(sig_values) for sig_values in L_sig_values ]
		x = [ v for vv in F for v in vv ] # Flat list of features for all signals
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
	
	
	
	
	
	