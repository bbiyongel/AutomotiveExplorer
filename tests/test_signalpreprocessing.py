import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
from signalpreprocessing import SignalPreProcessing

class TestSignalPreProcessing(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestSignalPreProcessing, self).__init__(*args, **kwargs)
		
	def test_removeOutliers(self):
		pass #TODO
		
	def test_removeExtremeValue_once(self):
		timestamps = [1234567, 1234777, 1235555, 1245454, 1444444, 2233224, 2433224]
		values1 = [3, 7, 20, 9, 6, 2, 8]
		values2 = [13, 17, 15, 19, 0, 12, 18]
		
		T1, V1 = SignalPreProcessing.removeExtremeValue(timestamps, values1)
		T2, V2 = SignalPreProcessing.removeExtremeValue(timestamps, values2)
		
		self.assertEqual(V1, [3, 7, 9, 6, 2, 8])
		self.assertEqual(V2, [13, 17, 15, 19, 12, 18])
		
		self.assertEqual(T1, [1234567, 1234777, 1245454, 1444444, 2233224, 2433224])
		self.assertEqual(T2, [1234567, 1234777, 1235555, 1245454, 2233224, 2433224])
	
	def test_removeExtremeValue_all(self):
		timestamps = [1234567, 1234777, 1235555, 1245454, 1444444, 2233224, 2433224, 3433224, 4433224, 5433224, 6433224, 7433224]
		values1 = [3, 7, 25, 9, 6, 25, 7, 8, 8, 8, 8, 8]
		values2 = [13, 17, 15, 19, 0, 12, 0, 15, 15, 15, 15, 15]
		
		T1, V1 = SignalPreProcessing.removeExtremeValue(timestamps, values1)
		T2, V2 = SignalPreProcessing.removeExtremeValue(timestamps, values2)
		
		self.assertEqual(V1, [3, 7, 9, 6, 7, 8, 8, 8, 8, 8])
		self.assertEqual(V2, [13, 17, 15, 19, 12, 15, 15, 15, 15, 15])
		
		self.assertEqual(T1, [1234567, 1234777, 1245454, 1444444, 2433224, 3433224, 4433224, 5433224, 6433224, 7433224])
		self.assertEqual(T2, [1234567, 1234777, 1235555, 1245454, 2233224, 3433224, 4433224, 5433224, 6433224, 7433224])
	
if __name__ == '__main__':
	unittest.main()
	
	
	