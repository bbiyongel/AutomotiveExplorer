import numpy as np
import math
import random
import matplotlib.pylab as plt
from Visualize import Visualize
import globals as gb
import time

class ArtificialData(object):
	def __init__(self, noise=1., ptrn=0.):
		self.noise = noise
		self.epsilon = ptrn # Patterns proximity (difficulty)
		
		# -------------------------

		self.highway_VS = (80, 80)
		self.countrySide_VS = (60,  80)
		self.city_VS = (0,  60)

		# -------------------------
		
		mean_VS = [ np.mean([ self.highway_VS[i], self.countrySide_VS[i], self.city_VS[i] ]) for i in [0,1] ]
		
		self.highway_VS = tuple( np.array(self.highway_VS) + self.epsilon * ( np.array(mean_VS) - np.array(self.highway_VS) ) )
		self.countrySide_VS = tuple( np.array(self.countrySide_VS) + self.epsilon * ( np.array(mean_VS) - np.array(self.countrySide_VS) ) )
		self.city_VS = tuple( np.array(self.city_VS) + self.epsilon * ( np.array(mean_VS) - np.array(self.city_VS) ) )
		
		self.highway_VS = [int(v) for v in self.highway_VS]
		self.countrySide_VS = [int(v) for v in self.countrySide_VS]
		self.city_VS = [int(v) for v in self.city_VS]

		self.normal_behaviour = 300
		# print self.highway_VS, self.countrySide_VS, self.city_VS

	# -----------------------------------------------------------------------------
	def run(self, parts=1):
		VS = []
		modes_reg = []
		
		for _ in range(parts):
			period_agg = 60 * random.randint(3*60, 5*60)
			# -------------------------------------
			total_time = 0
			while total_time < period_agg:
				region = random.choice([0,1,2])
				# if region == 0: period_reg = 60 * random.randint(30, 2*60) # city
				# if region == 1: period_reg = 60 * random.randint(30, 60) # countrySide
				# if region == 2: period_reg = 60 * random.randint(10, 30) # highway
				# Sepideh
				if region == 0: period_reg = 60 * random.randint(100, 120) # city
				if region == 1: period_reg = 60 * random.randint(100, 120) # countrySide
				if region == 2: period_reg = 60 * random.randint(10, 30) # highway
				total_time += period_reg
				
				modes_reg += [ region for _ in range(period_reg) ]
				# print "region =======>", region, period_reg, total_time

				VS_ = []
				if region==0:
					VS_ = self.city(period=period_reg)
				elif region==1:
					VS_ = self.countrySide(period=period_reg)
				elif region==2:
					VS_ = self.highway(period=period_reg)
				
				VS += VS_

		# viz = Visualize()
		# signame_labels = [viz.colors[y % len(viz.colors)] for y in modes_reg]
        #
		# #plt.scatter(range(len(VS)), VS, c=ground_truth); plt.show()
        #
		# viz.do_plot( VS, axs_labels=['Input Vehicle Speed'], marker="-", color=signame_labels)
		# viz.end_plot( fig=gb.PLOT_PATH+"/VM_Input---"+str(time.time())+".png" )


		return [VS], modes_reg
		
	# -----------------------------------------------------------------------------
	def randomized_line(self, n, interval):
		ratio = (interval[1]-interval[0])*1. / n
		
		L = [ interval[0] ]
		for _ in range(n):
			L.append( L[-1] + ratio )
		
		L = [ int(v) for v in L ]
		return L
	
	# -----------------------------------------------------------------------------
	def get_random_ints(self):
		rnd1 = random.randint(self.normal_behaviour-5,self.normal_behaviour+20)
		rnd2 = random.randint(self.normal_behaviour-20,self.normal_behaviour+5)
		rnd3 = random.randint(self.normal_behaviour-5,self.normal_behaviour+20)

		return rnd1, rnd2, rnd3
		
	# -----------------------------------------------------------------------------
	def city(self, period=15*60):
		VS = []
		
		mini, maxi = self.city_VS
		while len(VS) < period:
			rnd1, rnd2, rnd3 = self.get_random_ints()
			VS += self.randomized_line(n=rnd1, interval=(mini, maxi))
			VS += self.randomized_line(n=rnd2, interval=(VS[-1], VS[-1]))
			VS += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.city_VS[0], maxi-1)))

			mini = random.randint( self.city_VS[0], self.city_VS[1]-1 )
			maxi = random.randint( mini+1, self.city_VS[1] )

		if self.noise > 0:
			VS = [ int( v + np.random.normal(0, self.noise) ) for v in VS ][:period]
		
		VS = [max(v,0) for v in VS]

		#plt.plot(VS); plt.show()
		
		return VS
	
	# -----------------------------------------------------------------------------
	def countrySide(self, period=15*60):
		VS = []

		mini, maxi = self.countrySide_VS
		while len(VS) < period:
			rnd1, rnd2, rnd3 = self.get_random_ints()
			VS += self.randomized_line(n=rnd1, interval=(mini, maxi))
			VS += self.randomized_line(n=rnd2, interval=(VS[-1], VS[-1]))
			VS += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.countrySide_VS[0], maxi-1)))

			mini = random.randint( self.countrySide_VS[0], self.countrySide_VS[1]-1 )
			maxi = random.randint( mini+1, self.countrySide_VS[1] )

		if self.noise > 0:
			VS = [ int( v + np.random.normal(0, self.noise) ) for v in VS ][:period]

		VS = [max(v,0) for v in VS]

		# plt.plot(VS); plt.show()

		return VS
		
	# -----------------------------------------------------------------------------
	def highway(self, period=15*60):
		VS = []
		
		for t in range(period):
			vs = random.randint( self.highway_VS[0], self.highway_VS[1] )
			VS.append(vs)

		if self.noise > 0:
			VS = [ int( v + np.random.normal(0, self.noise/3.) ) for v in VS ][:period]

		VS = [max(v,0) for v in VS]

		# plt.plot(VS); plt.show()

		return VS
