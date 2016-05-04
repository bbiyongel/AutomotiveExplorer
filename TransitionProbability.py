from collections import defaultdict

class TransitionProbability(object):
	def __init__(self):
		self.transitions = defaultdict(float)
		self.normalizer = defaultdict(float)
	
	''' Update the transition model according to a sequence of states '''
	def fit(self, seq_states):
		for t in range(1, len(seq_states)):
			yi, yj = seq_states[t-1], seq_states[t]
			self.transitions[yi, yj] += 1.
			self.normalizer[yi] += 1.
			
		return self
	
	''' This returns the probability of transition from state_a to state_b (i.e., P(state_b | state_a)) '''
	def proba(self, state_a, state_b):
		return 0. if self.transitions[state_a, state_b] == 0. else self.transitions[state_a, state_b] / self.normalizer[state_a]
	
	def getStates(self):
		return sorted( list(self.normalizer.keys()) )
