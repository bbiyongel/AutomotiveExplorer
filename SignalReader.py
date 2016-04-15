import sqlite3
import datetime
from SignalPreProcessing import SignalPreProcessing
import globals as gb

class SignalReader(object):
	''' Open the database dbfile containing the signal. preprocess_duration defaults to 6 months '''
	def __init__(self, dbfile, preprocess=False, preprocess_duration=60000*60*24*30*6):
		self.conn = sqlite3.connect(dbfile)
		self.conn.row_factory = lambda cursor, row: row[0]
		self.cur = self.conn.cursor()
		
		self.init_date = datetime.datetime(year=2011, month=6, day=16, hour=5, minute=23, second=0)
		
		sig_id = dbfile.split('_')[1].split('.')[0]
		self.signal_name = gb.SIG_NAMES[sig_id] # FIXME: this should normally be an input to __init__
		
		self.extreme_values = gb.EXTREME[sig_id] # TODO test first if EXTREME is defined in globals
		if preprocess:
			timestamps, values = self.getSignal(end = preprocess_duration)
			self.extreme_values = SignalPreProcessing.getExtremeValue(timestamps, values)
		
	''' To properly close the database '''
	def closeDB(self):
		self.conn.close()
		
	''' Return a signal (timestamps and values) between the dates start and end. The parameter end could be a datetime
		or a duration in milliseconds '''
	def getSignal(self, start=None, end=None, dated=False):
		if isinstance( end, ( int, long, float ) ):
			end = (self.init_date if start is None else start) + datetime.timedelta(milliseconds=int(end))
		
		if start is None and end is None:
			query1 = 'SELECT value FROM Data'
			query2 = 'SELECT timestamp FROM Data'
		elif start is None:
			ts = self.getTimestamp(end)
			query1 = 'SELECT value FROM Data WHERE timestamp < ' + str(ts)
			query2 = 'SELECT timestamp FROM Data WHERE timestamp < ' + str(ts)
		elif end is None:
			ts = self.getTimestamp(start)
			query1 = 'SELECT value FROM Data WHERE timestamp >= ' + str(ts)
			query2 = 'SELECT timestamp FROM Data WHERE timestamp >= ' + str(ts)
		else:
			ts_start = self.getTimestamp(start)
			ts_end = self.getTimestamp(end)
			query1 = 'SELECT value FROM Data WHERE timestamp >= ' + str(ts_start) + ' AND timestamp < ' + str(ts_end)
			query2 = 'SELECT timestamp FROM Data WHERE timestamp >= ' + str(ts_start) + ' AND timestamp < ' + str(ts_end)
		
		self.cur.execute(query1)
		values = self.cur.fetchall()
		self.cur.execute(query2)
		timestamps = self.cur.fetchall()
		
		timestamps = [ts for its, ts in enumerate(timestamps) if values[its] not in self.extreme_values]
		values = [v for v in values if v not in self.extreme_values]
		
		if dated:
			timestamps = [self.getDate(ts) for ts in timestamps]
		
		return timestamps, values
		
	''' Returns the datetime corresponding to a given timestamp '''
	def getDate(self, ts):
		return self.init_date + datetime.timedelta(milliseconds=int(ts))
	
	''' Returns the timestamp corresponding to a given datetime '''
	def getTimestamp(self, dt):
		return (dt - self.init_date).total_seconds() * 1000 # milliseconds
