import numpy as np

class LikelihoodProbability(object):
	def __init__(self):
		self.foo = {}
	
	''' Compute the likelihood model according to data X and labels Y '''
	def fit(self, X, Y):
		if type(X) not in [list,tuple] and type(Y) not in [list,tuple]:
			X, Y = [X], [Y]
		
		for (x, y) in zip(X, Y):
			bar = self.foo.setdefault(y, {})
			bar[x] = bar.setdefault(x, 0) + 1
			
		return self
	
	''' This returns the probability of the data x given label y (i.e., P(x | y)) '''
	def proba(self, x, y):
		nb = 1.*self.foo[y].get(x, 0) if self.foo[y].get(x, 0) > 0. else 1. # FIXME (+1 / +n to avoid 0 proba)
		return nb / np.sum(list(self.foo[y].values()))
	