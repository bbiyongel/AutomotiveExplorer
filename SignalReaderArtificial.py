import datetime
# import globals as gb

class SignalReaderArtificial(object):
	''' Open the database dbfile containing the signal. preprocess_duration defaults to 6 months '''
	def __init__(self, signame, sigvalues, modes):
		self.init_date = datetime.datetime(year=2011, month=6, day=16, hour=5, minute=23, second=0)
		
		self.signal_name = signame
		self.signal_values = sigvalues
		self.modes = modes
		
	''' To properly close the database '''
	def closeDB(self):
		pass
		
	''' Return a signal (timestamps and values) between the dates start and end. The parameter end could be a datetime
		or a duration in milliseconds '''
	def getSignal(self, start=None, end=None, dated=False, get_modes=False):
		if isinstance( end, ( int, long, float ) ):
			end = (self.init_date if start is None else start) + datetime.timedelta(milliseconds=int(end))
		
		if start is None and end is None:
			values = self.signal_values
			timestamps = range(len(self.signal_values))
			modes = self.modes
		elif start is None:
			ts = self.getTimestamp(end) / 1000
			values = self.signal_values[:ts] # 'SELECT value FROM Data WHERE timestamp < ' + str(ts)
			timestamps = range(len(self.signal_values))[:ts] # 'SELECT timestamp FROM Data WHERE timestamp < ' + str(ts)
			modes = self.modes[:ts]
		elif end is None:
			ts = self.getTimestamp(start) / 1000
			values = self.signal_values[ts:] # 'SELECT value FROM Data WHERE timestamp >= ' + str(ts)
			timestamps = range(len(self.signal_values))[ts:] # 'SELECT timestamp FROM Data WHERE timestamp >= ' + str(ts)
			modes = self.modes[ts:]
		else:
			ts_start = self.getTimestamp(start) / 1000
			ts_end = self.getTimestamp(end) / 1000
			
			values = self.signal_values[ts_start:ts_end] # 'SELECT value FROM Data WHERE timestamp >= ' + str(ts_start) + ' AND timestamp < ' + str(ts_end)
			timestamps = range(len(self.signal_values))[ts_start:ts_end] # 'SELECT timestamp FROM Data WHERE timestamp >= ' + str(ts_start) + ' AND timestamp < ' + str(ts_end)
			modes = self.modes[ts_start:ts_end]
			
		if dated:
			timestamps = [self.getDate(ts) for ts in timestamps]
		
		if not get_modes:
			return timestamps, values
		else:
			return timestamps, values, modes
		
	''' Returns the datetime corresponding to a given timestamp '''
	def getDate(self, ts):
		return self.init_date + datetime.timedelta(milliseconds=int(ts))
	
	''' Returns the timestamp corresponding to a given datetime '''
	def getTimestamp(self, dt):
		ts = (dt - self.init_date).total_seconds() * 1000 # milliseconds
		return int(ts)
