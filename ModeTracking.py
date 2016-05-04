import globals as gb
import numpy as np
from TransitionProbability import TransitionProbability
from LikelihoodProbability import LikelihoodProbability

class ModeTracking(object):
	def __init__(self, nb_sigs = len(gb.SIG_IDS)):
		self.transition = TransitionProbability()
		self.likelihoods = [ LikelihoodProbability() for _ in range(nb_sigs) ]
		
		self.uniq_labels = []
		self.posterior_current = []
		
		
	# ------------------------------------------------------
	''' ... '''
	def track(self, x):
		posterior = []
		
		for mode in self.uniq_labels:
			likeli_prod = np.product([ lk.proba( x[ilk], mode ) for ilk, lk in enumerate(self.likelihoods) ])
			sum_previous = np.sum([ self.transition.proba(mode_prev, mode) * self.posterior_current[id] for id, mode_prev in enumerate(self.uniq_labels) ])
			posterior.append( likeli_prod * sum_previous )
		
		posterior = [ v/np.sum(posterior) for v in posterior ]
		self.posterior_current = posterior[:]
		
		return self.uniq_labels[ np.argmax(posterior) ]
	
	# ------------------------------------------------------
	''' '''
	def update_transition(self, labels_seq):
		self.transition.fit(labels_seq)
		self.update_modes_info(labels_seq)
		
	# ------------------------------------------------------
	''' '''
	def update_likelihoods(self, axes, labels):
		for iax in range(len(axes)):
			self.likelihoods[iax].fit( axes[iax], labels )
		
		self.update_modes_info(labels)
	
	# ------------------------------------------------------
	''' '''
	def update_modes_info(self, labels):
		if type(labels) not in [list,tuple]:
			labels = [labels]
			
		set_labels = set(labels)
		new_labels = [ y for y in set_labels if y not in self.uniq_labels ]
		self.uniq_labels += new_labels
		self.posterior_current += [ 1. / len(self.uniq_labels) for _ in new_labels ]
	
	# ------------------------------------------------------
	
	
	