import pandas as pd
import math

class SignalMerge(object):
	def __init__(self):
		mode_duration = 10 * 60
		
		highway_VehicleSpeed = [80 for i in range(mode_duration)]
		highway_EngineSpeed = [1300 for i in range(mode_duration)]
		highway_AcceleratorPedalPos = [0 for i in range(mode_duration)]
	#
	
	def VehicleSpeed(self):
		pass



