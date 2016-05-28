import globals as gb
import numpy as np
from TransitionProbability import TransitionProbability
from LikelihoodProbability import LikelihoodProbability

class ModeTracking(object):
	def __init__(self, type="empirical"):
		self.transition = TransitionProbability()
		self.likelihood = LikelihoodProbability(type=type)
		
		self.uniq_labels = []
		self.prev_posterior = []
		self.prev_y = None
		
	# ------------------------------------------------------
	''' ... '''
	def track(self, x, update=False):
		posterior = []
		
		for mode in self.uniq_labels:
			likeli_prod = self.likelihood.proba( x, mode )
			
			sum_previous = np.sum([ self.transition.proba(mode_prev, mode) * self.prev_posterior[id] for id, mode_prev in enumerate(self.uniq_labels) ])
			posterior.append( likeli_prod * sum_previous )
			
		posterior = [ v/np.sum(posterior) for v in posterior ]
		self.prev_posterior = posterior[:]
		
		predicted_mode = self.uniq_labels[ np.argmax(posterior) ]
		
		# -------------
		if update and self.prev_y is not None:
			self.update_transition( [self.prev_y, predicted_mode] )
			self.update_likelihoods( [ [v] for v in x ],  [predicted_mode] )
			
		self.prev_y = predicted_mode
		# -------------
		
		return predicted_mode
	
	# ------------------------------------------------------
	''' '''
	def update_transition(self, labels_seq):
		self.transition.fit(labels_seq)
		self.update_modes_info(labels_seq)
		
	# ------------------------------------------------------
	''' '''
	def update_likelihoods(self, axes, labels):
		self.likelihood.fit( axes, labels )
		self.update_modes_info(labels)
	
	# ------------------------------------------------------
	''' '''
	def update_modes_info(self, labels):
		if type(labels) not in [list,tuple]:
			labels = [labels]
			
		set_labels = set(labels)
		new_labels = [ y for y in set_labels if y not in self.uniq_labels ]
		self.uniq_labels += new_labels
		self.prev_posterior += [ 1. / len(self.uniq_labels) for _ in new_labels ]
	
	# ------------------------------------------------------
	
	
	