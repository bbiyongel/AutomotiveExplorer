import numpy as np
from scipy.stats import multivariate_normal
from mdp.utils import CovarianceMatrix
import mdp
from collections import defaultdict

# ===============================================================================================
class LikelihoodProbability(object):
	def __init__(self, type="empirical"):
		self.lp = LikelihoodProbabilityDependence() if type == "multivariate" else LikelihoodProbabilityIndependence(type=type)
		
	def fit(self, axes, labels):
		return self.lp.fit(axes, labels)
		
	def proba(self, x, y):
		return self.lp.proba(x, y)

# ===============================================================================================
class LikelihoodProbabilityDependence(object): # Not assuming independence between signals
	def __init__(self):
		self.dict = defaultdict(CovarianceMatrix)
	
	def fit(self, axes, labels):
		data = zip(*axes)
		
		for (x, y) in zip(data, labels):
			x = [float(v) for v in x]
			self.dict[y].update( np.array([ x ]) )
			
		return self
		
	def proba(self, x, y): # x is a data point, y is a label
		cov_mtx, avg, tlen = self.fix( self.dict[y] )
		mean = avg
		cov = cov_mtx
		
		p = multivariate_normal.pdf(x, mean=mean, cov=cov)
		return p
		
	def fix(self, cova, center=True):
		numx = mdp.numx
		tlen = cova._tlen * 1
		avg = np.array(cova._avg)
		cov_mtx = np.array(cova._cov_mtx)

		if cova.bias:
			cov_mtx /= tlen
		else:
			cov_mtx /= tlen - 1

		if center:
			avg_mtx = numx.outer(avg, avg)
			if cova.bias:
				avg_mtx /= tlen*(tlen)
			else:
				avg_mtx /= tlen*(tlen - 1)
			cov_mtx -= avg_mtx
			
		avg /= tlen

		return cov_mtx, avg, tlen
		
# ===============================================================================================
class LikelihoodProbabilityIndependence(object): # Assuming independence between signals
	def __init__(self, type="empirical", MAX_DIM = 1000):
		self.likelihoods = [ UnivariateLikelihoodProbability(type=type) for _ in range(MAX_DIM) ]
	
	def fit(self, axes, labels):
		for iax in range(len(axes)):
			self.likelihoods[iax].fit( axes[iax], labels )
		
	def proba(self, x, y): # x is a data point, y is a label
		likeli_prod = np.product([ lk.proba( x[ilk], y ) for ilk, lk in enumerate( self.likelihoods[:len(x)] ) ])
		return likeli_prod
		
# ===============================================================================================
class UnivariateLikelihoodProbability(object):
	def __init__(self, type="empirical"):
		self.type = type
		self.dict = {} if type == "empirical" else defaultdict(CovarianceMatrix)
		
	def fit(self, X, Y):
		if self.type == "empirical": return self.fit_empirical(X, Y)
		else: return self.fit_normal(X, Y)
	
	def proba(self, x, y):
		if self.type == "empirical": return self.proba_empirical(x, y)
		else: return self.proba_normal(x, y)
		
	# -------------------------------------------------------------------------
	#  Compute the likelihood model according to data X and labels Y
	def fit_empirical(self, AX, Y):
		for (v, y) in zip(AX, Y):
			bar = self.dict.setdefault(y, {})
			bar[v] = bar.setdefault(v, 0) + 1
			
		return self
	
	# -------------------------------------------------------------------------
	# This returns the probability of the data x given label y (i.e., P(x | y))
	def proba_empirical(self, x, y):
		nb = 1.*self.dict[y].get(x, 0) if self.dict[y].get(x, 0) > 0. else 1. # FIXME (+1 / +n to avoid 0 proba)
		return nb / np.sum(list(self.dict[y].values()))
	
	# -------------------------------------------------------------------------
	# Compute the likelihood model according to data X and labels Y
	def fit_normal(self, AX, Y):
		for (v, y) in zip(AX, Y):
			dp = [float(v)] # because v is one value, but we need an array of data points in the mdp update method
			self.dict[y].update( np.array([dp]) )
		
		return self
	
	# -------------------------------------------------------------------------
	# This returns the probability of the data x given label y (i.e., P(x | y))
	def proba_normal(self, x, y):
		cov_mtx, avg, tlen = self.fix( self.dict[y] )
		mean = avg
		cov = cov_mtx
		
		p = multivariate_normal.pdf(x, mean=mean, cov=cov)
		return p
	
	# -------------------------------------------------------------------------
	# This returns the appropriate covariance matrix, mean vector, and number of observations
	def fix(self, cova, center=True):
		numx = mdp.numx
		tlen = cova._tlen * 1
		avg = np.array(cova._avg)
		cov_mtx = np.array(cova._cov_mtx)

		if cova.bias:
			cov_mtx /= tlen
		else:
			cov_mtx /= tlen - 1

		if center:
			avg_mtx = numx.outer(avg, avg)
			if cova.bias:
				avg_mtx /= tlen*(tlen)
			else:
				avg_mtx /= tlen*(tlen - 1)
			cov_mtx -= avg_mtx
			
		avg /= tlen

		return cov_mtx, avg, tlen
# ===============================================================================================
