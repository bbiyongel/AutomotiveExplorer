import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
from signalreader import SignalReader
import datetime

class TestSignalReader(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestSignalReader, self).__init__(*args, **kwargs)
		
		dbfile = "C:/Users/mohbou/Desktop/MachineLearning Toolbox/datasets/kungsbacka/375_16929.db"
		self.sig = SignalReader(dbfile = dbfile)

	def test_getDate(self):
		ts = 1234567
		self.assertEqual( self.sig.getTimestamp( self.sig.getDate(ts) ), ts )
	
	def test_getTimestamp(self):
		dt = datetime.datetime(year=2013, month=06, day=21, hour=0, minute=0, second=0, microsecond=0)
		self.assertEqual( self.sig.getDate( self.sig.getTimestamp(dt) ), dt )
	
	def test_getSignal_all(self):
		timestamps, values = self.sig.getSignal()
		self.assertEqual( len(timestamps), len(values) )
		
	def test_getSignal_start(self):
		d_start = datetime.datetime(year=2013, month=06, day=21, hour=0, minute=0, second=0, microsecond=0)
		timestamps, values = self.sig.getSignal(start = d_start)
		self.assertEqual( len(timestamps), len(values) )
		self.assertTrue( all(self.sig.getDate(ts) >= d_start for ts in timestamps) )
		
	def test_getSignal_end(self):
		d_end = datetime.datetime(year=2014, month=10, day=30, hour=0, minute=0, second=0, microsecond=0)
		timestamps, values = self.sig.getSignal(end = d_end)
		self.assertEqual( len(timestamps), len(values) )
		self.assertTrue( all(self.sig.getDate(ts) < d_end for ts in timestamps) )
		
	def test_getSignal_end_duration(self):
		d_end = datetime.datetime(year=2014, month=10, day=30, hour=0, minute=0, second=0, microsecond=0)
		duration = (d_end - self.sig.init_date).total_seconds() * 1000 # milliseconds
		timestamps, values = self.sig.getSignal(end = duration)
		self.assertEqual( len(timestamps), len(values) )
		self.assertTrue( all(self.sig.getDate(ts) < d_end for ts in timestamps) )
		
	def test_getSignal_start_end(self):
		d_start = datetime.datetime(year=2013, month=06, day=21, hour=0, minute=0, second=0, microsecond=0)
		d_end = datetime.datetime(year=2014, month=10, day=30, hour=0, minute=0, second=0, microsecond=0)
		timestamps, values = self.sig.getSignal(start = d_start, end = d_end)
		self.assertEqual( len(timestamps), len(values) )
		self.assertTrue( all(self.sig.getDate(ts) >= d_start and self.sig.getDate(ts) < d_end for ts in timestamps) )
		
	def test_getSignal_start_end_duration(self):
		d_start = datetime.datetime(year=2013, month=06, day=21, hour=0, minute=0, second=0, microsecond=0)
		d_end = datetime.datetime(year=2014, month=10, day=30, hour=0, minute=0, second=0, microsecond=0)
		duration = (d_end - d_start).total_seconds() * 1000 # milliseconds
		timestamps, values = self.sig.getSignal(start = d_start, end = duration)
		self.assertEqual( len(timestamps), len(values) )
		self.assertTrue( all(self.sig.getDate(ts) >= d_start and self.sig.getDate(ts) < d_end for ts in timestamps) )
		
if __name__ == '__main__':
	unittest.main()
	
	
	