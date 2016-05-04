import pandas as pd
import math

class SignalMerge(object):
	def __init__(self):
		pass
		
	''' ... '''
	@staticmethod
	def merge(LTimeseries, interpolate=False):
		i = 0
		timestamps, values = LTimeseries[i]
		df = pd.DataFrame(zip(timestamps, values), columns=['Time', 'Values'])
		df.index = df['Time']		
		
		while True:
			i += 1
			timestamps, values = LTimeseries[i]
			df_new = pd.DataFrame(zip(timestamps, values), columns=['Time', 'Values'])
			df_new.index = df_new['Time']
			
			if i < len(LTimeseries)-1:
				df = df.merge(df_new, how='outer', on='Time')
			else:
				df = df.merge(df_new, how='outer', on='Time', sort='Time')
				break
		
		if interpolate:
			df.interpolate(method='linear', inplace=True)
		else:
			df.fillna(method='ffill', inplace=True)
			df.fillna(method='bfill', inplace=True)
		
		merged_data = df.get_values().tolist()
		axes = zip(*merged_data)
		
		times = axes[0]
		axes = axes[1:]
		
		axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ]
		
		return times, axes
		



