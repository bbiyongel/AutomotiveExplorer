import numpy as np
import math
import random
import matplotlib.pylab as plt

class ArtificialData(object):
	def __init__(self, noise=1., ptrn=0.):
		self.noise = noise
		self.epsilon = ptrn # Patterns proximity (difficulty)
		
		# -------------------------
		self.highway_VS = (80, 80)
		self.highway_ES = (1300, 1300)
		self.highway_APP = (50, 100)
		self.highway_BPP = (0,  0)
		
		self.countrySide_VS = (60,  80)
		self.countrySide_ES = (1000, 1100)
		self.countrySide_APP = (40, 60)
		self.countrySide_BPP = (0,  20)
		
		self.city_VS = (0,  60)
		self.city_ES = (500, 1000)
		self.city_APP = (0,  50)
		self.city_BPP = (10,  30)
		
		self.coldEngine_ECT = (10, 70)
		self.hotEngine_ECT = (70,  85)
		
		self.normal_behaviour = 100
		self.agressive_behaviour = 6
		# -------------------------
		
		mean_VS = [ np.mean([ self.highway_VS[i], self.countrySide_VS[i], self.city_VS[i] ]) for i in [0,1] ]
		mean_ES = [ np.mean([ self.highway_ES[i], self.countrySide_ES[i], self.city_ES[i] ]) for i in [0,1] ]
		mean_APP = [ np.mean([ self.highway_APP[i], self.countrySide_APP[i], self.city_APP[i] ]) for i in [0,1] ]
		mean_BPP = [ np.mean([ self.highway_BPP[i], self.countrySide_BPP[i], self.city_BPP[i] ]) for i in [0,1] ]
		mean_ECT = [ np.mean([ self.coldEngine_ECT[i], self.hotEngine_ECT[i] ]) for i in [0,1] ]
		mean_Agg = np.mean([ self.normal_behaviour, self.agressive_behaviour ])
		
		self.highway_VS = tuple( np.array(self.highway_VS) + self.epsilon * ( np.array(mean_VS) - np.array(self.highway_VS) ) )
		self.highway_ES = tuple( np.array(self.highway_ES) + self.epsilon * ( np.array(mean_ES) - np.array(self.highway_ES) ) )
		self.highway_APP = tuple( np.array(self.highway_APP) + self.epsilon * ( np.array(mean_APP) - np.array(self.highway_APP) ) )
		self.highway_BPP = tuple( np.array(self.highway_BPP) + self.epsilon * ( np.array(mean_BPP) - np.array(self.highway_BPP) ) )
		
		self.countrySide_VS = tuple( np.array(self.countrySide_VS) + self.epsilon * ( np.array(mean_VS) - np.array(self.countrySide_VS) ) )
		self.countrySide_ES = tuple( np.array(self.countrySide_ES) + self.epsilon * ( np.array(mean_ES) - np.array(self.countrySide_ES) ) )
		self.countrySide_APP = tuple( np.array(self.countrySide_APP) + self.epsilon * ( np.array(mean_APP) - np.array(self.countrySide_APP) ) )
		self.countrySide_BPP = tuple( np.array(self.countrySide_BPP) + self.epsilon * ( np.array(mean_BPP) - np.array(self.countrySide_BPP) ) )
		
		self.city_VS = tuple( np.array(self.city_VS) + self.epsilon * ( np.array(mean_VS) - np.array(self.city_VS) ) )
		self.city_ES = tuple( np.array(self.city_ES) + self.epsilon * ( np.array(mean_ES) - np.array(self.city_ES) ) )
		self.city_APP = tuple( np.array(self.city_APP) + self.epsilon * ( np.array(mean_APP) - np.array(self.city_APP) ) )
		self.city_BPP = tuple( np.array(self.city_BPP) + self.epsilon * ( np.array(mean_BPP) - np.array(self.city_BPP) ) )
		
		self.coldEngine_ECT = tuple( np.array(self.coldEngine_ECT) + self.epsilon * ( np.array(mean_ECT) - np.array(self.coldEngine_ECT) ) )
		self.hotEngine_ECT = tuple( np.array(self.hotEngine_ECT) + self.epsilon * ( np.array(mean_ECT) - np.array(self.hotEngine_ECT) ) )
		
		self.normal_behaviour = self.normal_behaviour + self.epsilon * (mean_Agg - self.normal_behaviour)
		self.agressive_behaviour = self.agressive_behaviour + self.epsilon * (mean_Agg - self.agressive_behaviour)
		
		self.highway_VS = [int(v) for v in self.highway_VS]
		self.highway_ES = [int(v) for v in self.highway_ES]
		self.highway_APP = [int(v) for v in self.highway_APP]
		self.highway_BPP = [int(v) for v in self.highway_BPP]
		
		self.countrySide_VS = [int(v) for v in self.countrySide_VS]
		self.countrySide_ES = [int(v) for v in self.countrySide_ES]
		self.countrySide_APP = [int(v) for v in self.countrySide_APP]
		self.countrySide_BPP = [int(v) for v in self.countrySide_BPP]
		
		self.city_VS = [int(v) for v in self.city_VS]
		self.city_ES = [int(v) for v in self.city_ES]
		self.city_APP = [int(v) for v in self.city_APP]
		self.city_BPP = [int(v) for v in self.city_BPP]
		
		self.coldEngine_ECT = [int(v) for v in self.coldEngine_ECT]
		self.hotEngine_ECT = [int(v) for v in self.hotEngine_ECT]
		
		self.normal_behaviour = int(self.normal_behaviour)
		self.agressive_behaviour = int(self.agressive_behaviour)
		
		print self.highway_VS, self.highway_ES, self.highway_APP, self.highway_BPP
		print self.countrySide_VS, self.countrySide_ES, self.countrySide_APP, self.countrySide_BPP
		print self.city_VS, self.city_ES, self.city_APP, self.city_BPP
		print self.coldEngine_ECT, self.hotEngine_ECT
		print self.normal_behaviour, self.agressive_behaviour
		
	# -----------------------------------------------------------------------------
	def run(self, parts=1, agg = None):
		modes_agg = []; modes_reg = []; modes_tem = []
		VS = []; ES = []; APP = []; BPP = []; ECT = []
		
		for _ in range(parts):
			if agg is None: agressive = 1 if random.uniform(0,1) < 0.5 else 0
			else: agressive = agg
			
			period_agg = 60 * random.randint(3*60, 5*60)
			
			modes_agg += [ agressive for _ in range(period_agg) ]
			print "agressive =======>", agressive, period_agg
			
			# -------------------------------------
			total_time = 0
			while total_time < period_agg:
				region = random.choice([0,1,2])
				if region == 0: period_reg = 60 * random.randint(30, 2*60) # city
				if region == 1: period_reg = 60 * random.randint(30, 60) # countrySide
				if region == 2: period_reg = 60 * random.randint(10, 30) # highway
				total_time += period_reg
				
				modes_reg += [ region for _ in range(period_reg) ]
				print "region =======>", region, period_reg, total_time
				
				if region==0:
					VS_, ES_, APP_, BPP_ = self.city(period=period_reg, agressive=agressive)
				elif region==1:
					VS_, ES_, APP_, BPP_ = self.countrySide(period=period_reg, agressive=agressive)
				elif region==2:
					VS_, ES_, APP_, BPP_ = self.highway(period=period_reg, agressive=agressive)
				
				VS += VS_; ES += ES_; APP += APP_; BPP += BPP_
			
			# -------------------------------------
			total_time = 0
			cold = 0
			while total_time < period_agg:
				cold = 0 if cold==1 else 1
				period_tem = 60 * random.randint(50, 90)
				total_time += period_tem
				
				modes_tem += [ cold for _ in range(period_tem) ]
				print "cold =======>", cold, period_tem, total_time
				
				if cold==0: ECT += self.hotEngine(period=period_tem)
				elif cold==1: ECT += self.coldEngine(period=period_tem)
			
			# --------------------------------------
			modes_reg = modes_reg[:len(modes_agg)]
			modes_tem = modes_tem[:len(modes_agg)]
			
			VS = VS[:len(modes_agg)]
			ES = ES[:len(modes_agg)]
			APP = APP[:len(modes_agg)]
			BPP = BPP[:len(modes_agg)]
			ECT = ECT[:len(modes_agg)]

		# -------------------------------------
		# plt.scatter(range(len(VS)), VS, c=modes_reg, marker='o'); plt.show()
		# plt.scatter(range(len(ES)), ES, c=modes_reg); plt.show()
		# plt.scatter(range(len(APP)), APP, c=modes_reg); plt.show()
		# plt.scatter(range(len(BPP)), BPP, c=modes_reg); plt.show()
		# plt.scatter(range(len(ECT)), ECT, c=modes_tem); plt.show()
		
		print len(modes_agg), len(modes_reg), len(modes_tem)
		print set(modes_agg), set(modes_reg), set(modes_tem)
		
		if agg is None:
			combined_modes = zip(modes_agg, modes_reg)
			combined_modes_set = list(set(combined_modes))
			return [VS, ES, APP, BPP], [ combined_modes_set.index((a,b)) for (a,b) in combined_modes ]
		else:
			return [VS, ES, APP, BPP], modes_reg
		
	# -----------------------------------------------------------------------------
	def randomized_line(self, n, interval):
		ratio = (interval[1]-interval[0])*1. / n
		
		L = [ interval[0] ]
		for _ in range(n):
			L.append( L[-1] + ratio )
		
		L = [ int(v) for v in L ]
		return L
	
	# -----------------------------------------------------------------------------
	def get_random_ints(self, aggressive=False):
		if aggressive == False:
			rnd1 = random.randint(self.normal_behaviour-5,self.normal_behaviour+20)
			rnd2 = random.randint(self.normal_behaviour-20,self.normal_behaviour+5)
			rnd3 = random.randint(self.normal_behaviour-5,self.normal_behaviour+20)
		else:
			rnd1 = random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2)
			rnd2 = random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2)
			rnd3 = random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2)
			
		return rnd1, rnd2, rnd3
		
	# -----------------------------------------------------------------------------
	def city(self, period=15*60, agressive=0):
		VS = []; ES = []; APP = []; BPP = []
		
		mini, maxi = self.city_VS
		while len(VS) < period:
			if agressive==0:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=False)
				VS += self.randomized_line(n=rnd1, interval=(mini, maxi))
				VS += self.randomized_line(n=rnd2, interval=(VS[-1], VS[-1]))
				VS += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.city_VS[0], maxi-1)))
			else:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=True)
				VS += self.randomized_line(n=rnd1, interval=(mini, maxi))
				VS += self.randomized_line(n=rnd2, interval=(VS[-1], VS[-1]))
				VS += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.city_VS[0], maxi-1)))
			
			mini = random.randint( self.city_VS[0], self.city_VS[1]-1 )
			maxi = random.randint( mini+1, self.city_VS[1] )
		
		ES = [ int(np.interp(v, self.city_VS, self.city_ES)+np.random.normal(0,30)) for v in VS ]
		
		mini, maxi = self.city_APP
		while len(APP) < period:
			if agressive==0:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=False)
				APP += self.randomized_line(n=rnd1, interval=(mini, maxi))
				APP += self.randomized_line(n=rnd2, interval=(APP[-1], APP[-1]))
				APP += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.city_APP[0], maxi-1)))
			else:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=True)
				APP += self.randomized_line(n=rnd1, interval=(mini, maxi))
				APP += self.randomized_line(n=rnd2, interval=(APP[-1], APP[-1]))
				APP += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.city_APP[0], maxi-1)))
			
			mini = random.randint( self.city_APP[0], self.city_APP[1]-1 )
			maxi = random.randint( mini+1, self.city_APP[1] )
		
		mini, maxi = self.city_BPP
		while len(BPP) < period:
			if agressive==0:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=False)
				BPP += self.randomized_line(n=rnd1, interval=(mini, maxi))
				BPP += self.randomized_line(n=rnd2, interval=(BPP[-1], BPP[-1]))
				BPP += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.city_BPP[0], maxi-1)))
			else:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=True)
				BPP += self.randomized_line(n=rnd1, interval=(mini, maxi))
				BPP += self.randomized_line(n=rnd2, interval=(BPP[-1], BPP[-1]))
				BPP += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.city_BPP[0], maxi-1)))
			
			mini = random.randint( self.city_BPP[0], self.city_BPP[1]-1 )
			maxi = random.randint( mini+1, self.city_BPP[1] )
		
		if self.noise > 0:
			VS = [ int( v + np.random.normal(0, self.noise) ) for v in VS ][:period]
			ES = [ int( v + np.random.normal(0, self.noise) ) for v in ES ][:period]
			APP = [ int( v + np.random.normal(0, self.noise) ) for v in APP ][:period]
			BPP = [ int( v + np.random.normal(0, self.noise) ) for v in BPP ][:period]
		
		VS = [max(v,0) for v in VS]
		ES = [max(v,0) for v in ES]
		APP = [max(v,0) for v in APP]
		BPP = [max(v,0) for v in BPP]
		
		# plt.plot(VS); plt.show()
		# plt.plot(ES); plt.show()
		# plt.plot(APP); plt.show()
		# plt.plot(BPP); plt.show()
		
		return VS, ES, APP, BPP
	
	# -----------------------------------------------------------------------------
	def countrySide(self, period=15*60, agressive=0):
		VS = []; ES = []; APP = []; BPP = []
		
		mini, maxi = self.countrySide_VS
		while len(VS) < period:
			if agressive==0:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=False)
				VS += self.randomized_line(n=rnd1, interval=(mini, maxi))
				VS += self.randomized_line(n=rnd2, interval=(VS[-1], VS[-1]))
				VS += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.countrySide_VS[0], maxi-1)))
			else:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=True)
				VS += self.randomized_line(n=rnd1, interval=(mini, maxi))
				VS += self.randomized_line(n=rnd2, interval=(VS[-1], VS[-1]))
				VS += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.countrySide_VS[0], maxi-1)))
			
			mini = random.randint( self.countrySide_VS[0], self.countrySide_VS[1]-1 )
			maxi = random.randint( mini+1, self.countrySide_VS[1] )
		
		ES = [ int(np.interp(v, self.countrySide_VS, self.countrySide_ES)+np.random.normal(0,30)) for v in VS ]
		
		mini, maxi = self.countrySide_APP
		while len(APP) < period:
			if agressive==0:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=False)
				APP += self.randomized_line(n=rnd1, interval=(mini, maxi))
				APP += self.randomized_line(n=rnd2, interval=(APP[-1], APP[-1]))
				APP += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.countrySide_APP[0], maxi-1)))
			else:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=True)
				APP += self.randomized_line(n=rnd1, interval=(mini, maxi))
				APP += self.randomized_line(n=rnd2, interval=(APP[-1], APP[-1]))
				APP += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.countrySide_APP[0], maxi-1)))
			
			mini = random.randint( self.countrySide_APP[0], self.countrySide_APP[1]-1 )
			maxi = random.randint( mini+1, self.countrySide_APP[1] )
		
		mini, maxi = self.countrySide_BPP
		while len(BPP) < period:
			if agressive==0:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=False)
				BPP += self.randomized_line(n=rnd1, interval=(mini, maxi))
				BPP += self.randomized_line(n=rnd2, interval=(BPP[-1], BPP[-1]))
				BPP += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.countrySide_BPP[0], maxi-1)))
			else:
				rnd1, rnd2, rnd3 = self.get_random_ints(aggressive=True)
				BPP += self.randomized_line(n=rnd1, interval=(mini, maxi))
				BPP += self.randomized_line(n=rnd2, interval=(BPP[-1], BPP[-1]))
				BPP += self.randomized_line(n=rnd3, interval=(maxi, random.randint(self.countrySide_BPP[0], maxi-1)))
			
			mini = random.randint( self.countrySide_BPP[0], self.countrySide_BPP[1]-1 )
			maxi = random.randint( mini+1, self.countrySide_BPP[1] )
		
		if self.noise > 0:
			VS = [ int( v + np.random.normal(0, self.noise) ) for v in VS ][:period]
			ES = [ int( v + np.random.normal(0, self.noise) ) for v in ES ][:period]
			APP = [ int( v + np.random.normal(0, self.noise) ) for v in APP ][:period]
			BPP = [ int( v + np.random.normal(0, self.noise) ) for v in BPP ][:period]
		
		VS = [max(v,0) for v in VS]
		ES = [max(v,0) for v in ES]
		APP = [max(v,0) for v in APP]
		BPP = [max(v,0) for v in BPP]
		
		# plt.plot(VS); plt.show()
		# plt.plot(ES); plt.show()
		# plt.plot(APP); plt.show()
		# plt.plot(BPP); plt.show()
		
		return VS, ES, APP, BPP
		
	# -----------------------------------------------------------------------------
	def highway(self, period=15*60, agressive=0):
		VS = []; ES = []; APP = []; BPP = []
		
		for t in range(period):
			vs = random.randint( self.highway_VS[0], self.highway_VS[1] )
			if agressive==1:
				vs = random.randint( self.highway_VS[0]-1, self.highway_VS[1]+3 )
				vs += np.random.normal(0,1)
			VS.append(vs)
		
		for t in range(period):
			es = random.randint( self.highway_ES[0], self.highway_ES[1] )
			if agressive==1:
				es = random.randint( self.highway_ES[0]-1, self.highway_ES[1]+3 )
				es += np.random.normal(0,1)
			ES.append(es)
		
		for t in range(period):
			app = random.randint( self.highway_APP[0], self.highway_APP[1] )
			if agressive==1:
				app = random.randint( self.highway_APP[0]-1, self.highway_APP[1]+3 )
				app += np.random.normal(0,1)
			APP.append(app)
		
		for t in range(period):
			bpp = random.randint( self.highway_BPP[0], self.highway_BPP[1] )
			if agressive==1:
				bpp = random.randint( self.highway_BPP[0]-1, self.highway_BPP[1]+3 )
				bpp += np.random.normal(0,1)
			BPP.append(bpp)
		
		if self.noise > 0:
			VS = [ int( v + np.random.normal(0, self.noise/3.) ) for v in VS ][:period]
			ES = [ int( v + np.random.normal(0, self.noise/3.) ) for v in ES ][:period]
			APP = [ int( v + np.random.normal(0, self.noise/3.) ) for v in APP ][:period]
			BPP = [ int( v + np.random.normal(0, self.noise/3.) ) for v in BPP ][:period]
		
		VS = [max(v,0) for v in VS]
		ES = [max(v,0) for v in ES]
		APP = [max(v,0) for v in APP]
		BPP = [max(v,0) for v in BPP]
		
		# plt.plot(VS); plt.show()
		# plt.plot(ES); plt.show()
		# plt.plot(APP); plt.show()
		# plt.plot(BPP); plt.show()
		
		return VS, ES, APP, BPP
		
	# -----------------------------------------------------------------------------
	def coldEngine(self, period=15*60):
		ECT = self.randomized_line(n=period, interval=self.coldEngine_ECT)
		
		if self.noise > 0:
			ECT = [ int( v + np.random.normal(0, self.noise/3.) ) for v in ECT ][:period]

		# plt.plot(ECT); plt.show()
		return ECT
		
	# -----------------------------------------------------------------------------
	def hotEngine(self, period=15*60):
		ECT = []
		mini, maxi = self.hotEngine_ECT
		while len(ECT) < period:
			ECT += self.randomized_line(n=maxi-mini, interval=(mini, maxi))
			
			ECT += self.randomized_line(n=self.normal_behaviour, interval=(ECT[-1], ECT[-1]))
			
			mini = random.randint( self.hotEngine_ECT[0], self.hotEngine_ECT[1]-1 )
			maxi = random.randint( mini+1, self.hotEngine_ECT[1] )
		
		if self.noise > 0:
			ECT = [ int( v + np.random.normal(0, self.noise/3.) ) for v in ECT ][:period]

		# plt.plot(ECT); plt.show()
		return ECT
	
	# --------------------------------------------------------

