import numpy as np

class SignalPreProcessing(object):
	def __init__(self):
		pass
		
	''' Remove outliers from the signal '''
	@staticmethod
	def removeOutliers(timestamps, values, alpha=2):
		mean = np.mean(values)
		std = np.std(values)

		new_timestamps = []
		new_values = []
		
		for iv, v in enumerate(values):
			if abs(v - mean) < alpha * std:
				new_values.append(v)
				new_timestamps.append(timestamps[iv])
			
		return new_timestamps, new_values
	
	''' Remove extreme values from the signal '''
	@staticmethod
	def removeExtremeValue(timestamps, values, alpha=2):
		mean = np.mean(values)
		std = np.std(values)
		
		max_value = max(values)
		if abs(max_value - mean) >= alpha * std:
			timestamps = [ts for its, ts in enumerate(timestamps) if values[its] != max_value]
			values = [v for v in values if v != max_value]
		
		min_value = min(values)
		if abs(min_value - mean) >= alpha * std:
			timestamps = [ts for its, ts in enumerate(timestamps) if values[its] != min_value]
			values = [v for v in values if v != min_value]
			
		return timestamps, values
	
	''' Return extreme values in the signal '''
	@staticmethod
	def getExtremeValue(timestamps, values, alpha=2):
		mean = np.mean(values)
		std = np.std(values)
		
		extreme_values = []
		
		max_value = max(values)
		if abs(max_value - mean) >= alpha * std:
			extreme_values.append( max_value )
		
		min_value = min(values)
		if abs(min_value - mean) >= alpha * std:
			extreme_values.append( min_value )
			
		return extreme_values
		