import numpy as np
import math
import random
import matplotlib.pylab as plt

class ArtificialData(object):
	def __init__(self):
		self.highway_VS = (80, 80)
		self.highway_ES = (1300,  1300) # Should be very concentrated around 1300
		self.highway_APP = (0,  0)
		self.highway_BPP = (0,  0)
		
		self.countrySide_VS = (60,  80)
		self.countrySide_ES = (1000,  1100)
		self.countrySide_APP = (40,  60)
		self.countrySide_BPP = (0,  15)
		
		self.city_VS = (0,  60)
		self.city_ES = (500,  1000)  # Should be from time,  time very concentrated around 600 (stops)
		self.city_APP = (0,  40)
		self.city_BPP = (15,  30)
		
		self.coldEngine_ECT = (10,  70)
		self.hotEngine_ECT = (70,  85)
		
		self.noise = 1.
		
		self.normal_behaviour = 100
		self.agressive_behaviour = 10
		
	# -----------------------------------------------------------------------------
	def run(self, parts=1):
		modes_agg = []; modes_reg = []; modes_tem = []
		VS = []; ES = []; APP = []; BPP = []; ECT = []
		
		for _ in range(parts):
			agressive = 1 if random.uniform(0,1) < 0.5 else 0
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
		
		return VS, ES, APP, BPP, ECT
		
	# -----------------------------------------------------------------------------
	def randomized_line(self, n, interval):
		ratio = (interval[1]-interval[0])*1. / n
		
		L = [ interval[0] ]
		for _ in range(n):
			L.append( L[-1] + ratio )
		
		L = [ int(v) for v in L ]
		return L
	
	# -----------------------------------------------------------------------------
	def city(self, period=15*60, agressive=0):
		VS = []; ES = []; APP = []; BPP = []
		
		mini, maxi = self.city_VS
		while len(VS) < period:
			VS += self.randomized_line(n=maxi-mini, interval=(mini, maxi))
			
			if agressive==0: VS += self.randomized_line(n=random.randint(self.normal_behaviour-5,self.normal_behaviour+5), interval=(VS[-1], VS[-1]))
			else: VS += self.randomized_line(n=random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2), interval=(VS[-1], VS[-1]))
			
			mini = random.randint( self.city_VS[0], self.city_VS[1]-1 )
			maxi = random.randint( mini+1, self.city_VS[1] )
		
		ES = [ int(np.interp(v, self.city_VS, self.city_ES)+np.random.normal(0,30)) for v in VS ]
		
		mini, maxi = self.city_APP
		while len(APP) < period:
			APP += self.randomized_line(n=maxi-mini, interval=(mini, maxi))
			
			if agressive==0: APP += self.randomized_line(n=random.randint(self.normal_behaviour-5,self.normal_behaviour+5), interval=(APP[-1], APP[-1]))
			else: APP += self.randomized_line(n=random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2), interval=(APP[-1], APP[-1]))
			
			mini = random.randint( self.city_APP[0], self.city_APP[1]-1 )
			maxi = random.randint( mini+1, self.city_APP[1] )
		
		mini, maxi = self.city_BPP
		while len(BPP) < period:
			BPP += self.randomized_line(n=maxi-mini, interval=(mini, maxi))
			
			if agressive==0: BPP += self.randomized_line(n=random.randint(self.normal_behaviour-5,self.normal_behaviour+5), interval=(BPP[-1], BPP[-1]))
			else: BPP += self.randomized_line(n=random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2), interval=(BPP[-1], BPP[-1]))
			
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
			VS += self.randomized_line(n=maxi-mini, interval=(mini, maxi))
			
			if agressive==0: VS += self.randomized_line(n=random.randint(self.normal_behaviour-5,self.normal_behaviour+5), interval=(VS[-1], VS[-1]))
			else: VS += self.randomized_line(n=random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2), interval=(VS[-1], VS[-1]))
			
			mini = random.randint( self.countrySide_VS[0], self.countrySide_VS[1]-1 )
			maxi = random.randint( mini+1, self.countrySide_VS[1] )
		
		ES = [ int(np.interp(v, self.countrySide_VS, self.countrySide_ES)+np.random.normal(0,30)) for v in VS ]
		
		mini, maxi = self.countrySide_APP
		while len(APP) < period:
			APP += self.randomized_line(n=maxi-mini, interval=(mini, maxi))
			
			if agressive==0: APP += self.randomized_line(n=random.randint(self.normal_behaviour-5,self.normal_behaviour+5), interval=(APP[-1], APP[-1]))
			else: APP += self.randomized_line(n=random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2), interval=(APP[-1], APP[-1]))
			
			mini = random.randint( self.countrySide_APP[0], self.countrySide_APP[1]-1 )
			maxi = random.randint( mini+1, self.countrySide_APP[1] )
		
		mini, maxi = self.countrySide_BPP
		while len(BPP) < period:
			BPP += self.randomized_line(n=maxi-mini, interval=(mini, maxi))
			
			if agressive==0: BPP += self.randomized_line(n=random.randint(self.normal_behaviour-5,self.normal_behaviour+5), interval=(BPP[-1], BPP[-1]))
			else: BPP += self.randomized_line(n=random.randint(self.agressive_behaviour-2,self.agressive_behaviour+2), interval=(BPP[-1], BPP[-1]))
			
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
			if agressive==1: vs += np.random.normal(0,1)
			VS.append(vs)
		
		for t in range(period):
			es = random.randint( self.highway_ES[0], self.highway_ES[1] )
			if agressive==1: es += np.random.normal(0,5)
			ES.append(es)
		
		for t in range(period):
			app = random.randint( self.highway_APP[0], self.highway_APP[1] )
			if agressive==1: app += np.random.normal(0,1)
			APP.append(app)
		
		for t in range(period):
			bpp = random.randint( self.highway_BPP[0], self.highway_BPP[1] )
			if agressive==1: bpp += np.random.normal(0,1)
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

