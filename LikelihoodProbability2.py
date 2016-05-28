import numpy as np
from scipy.stats import multivariate_normal
from mdp.utils import CovarianceMatrix
import mdp
from collections import defaultdict

# '''
class LikelihoodProbability(object):
	def __init__(self):
		self.foo = {}
	
	#  Compute the likelihood model according to data X and labels Y
	def fit(self, X, Y):
		if type(X) not in [list,tuple] and type(Y) not in [list,tuple]:
			X, Y = [X], [Y]
		
		for (x, y) in zip(X, Y):
			bar = self.foo.setdefault(y, {})
			bar[x] = bar.setdefault(x, 0) + 1
			
		return self
	
	# This returns the probability of the data x given label y (i.e., P(x | y))
	def proba(self, x, y):
		nb = 1.*self.foo[y].get(x, 0) if self.foo[y].get(x, 0) > 0. else 1. # FIXME (+1 / +n to avoid 0 proba)
		return nb / np.sum(list(self.foo[y].values()))
# '''

'''
class LikelihoodProbability(object):
	def __init__(self):
		self.comats = defaultdict(CovarianceMatrix)
		
	# Compute the likelihood model according to data X and labels Y
	def fit(self, X, Y):
		if type(X) not in [list,tuple] and type(Y) not in [list,tuple]:
			X, Y = [X], [Y]
		
		for (x, y) in zip(X, Y):
			dp = [float(x)] # because x is one value and need an array of data points in the mdp update method
			self.comats[y].update( np.array([dp]) )
		
		return self
	
	# This returns the probability of the data x given label y (i.e., P(x | y))
	def proba(self, x, y):
		cov_mtx, avg, tlen = self.fix( self.comats[y] )
		mean = avg
		cov = cov_mtx
		
		p = multivariate_normal.pdf(x, mean=mean, cov=cov)
		return p
	
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
'''
