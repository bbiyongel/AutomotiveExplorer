import numpy as np
import math
import random
import matplotlib.pylab as plt

class ArtificialData(object):
	def __init__(self):
		self.highway_VS = (80, 81)
		self.highway_ES = (1250,  1300) # Should be very concentrated around 1300
		self.highway_APP = (0,  0) #(40,  60)
		self.highway_BPP = (0,  0)
		
		self.countrySide_VS = (70,  80)
		self.countrySide_ES = (1000,  1100)
		self.countrySide_APP = (40,  60)
		self.countrySide_BPP = (0,  15)
		
		self.city_VS = (0,  60)
		self.city_ES = (500,  1000)  # Should be from time,  time very concentrated around 600 (stops)
		self.city_APP = (0,  40)
		self.city_BPP = (15,  30)
		
		self.coldEngine_ECT = (10,  70) # Should be increasing
		self.hotEngine_ECT = (70,  85)
		
		self.noise = 1
		
	# -----------------------------------------------------------------------------
	def run(self, parts=2):
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
				if region == 0: period_reg = 60 * random.randint(30, 2*60)
				if region == 1: period_reg = 60 * random.randint(30, 60)
				if region == 2: period_reg = 60 * random.randint(10, 30)
				total_time += period_reg
				
				modes_reg += [ region for _ in range(period_reg) ]
				# TODO generate values
				print "region =======>", region, period_reg, total_time
			
			modes_reg = modes_reg[:len(modes_agg)]
			# -------------------------------------
			total_time = 0
			cold = 0
			while total_time < period_agg:
				cold = 0 if cold==1 else 1
				period_tem = 60 * random.randint(50, 90)
				total_time += period_tem
				
				modes_tem += [ cold for _ in range(period_tem) ]
				# TODO generate values
				print "cold =======>", cold, period_tem, total_time
			
			modes_tem = modes_tem[:len(modes_agg)]
		# -------------------------------------
		
		print len(modes_agg), len(modes_reg), len(modes_tem)
		print set(modes_agg), set(modes_reg), set(modes_tem)
		
	# -----------------------------------------------------------------------------
	def randomized_line(self, n, interval):
		ratio = int( (interval[1]-interval[0]) / n )
		L = [ interval[0] ]
		for _ in range(n):
			L.append( L[-1] + ratio )
		
		# L = [ int( v + np.random.normal(0, self.noise) ) for v in L ]
		
		# plt.plot(L); plt.show()
		return L
	
	# -----------------------------------------------------------------------------
	def randomized_sine(self, n, interval):
		mi, ma = interval
		
		L = [ int( ma * math.sin(i) if math.sin(i) > 0 else 0 ) for i in range(n) ]
		L = [ int( v + abs(np.random.normal(0, 10)) ) for v in L ]
		
		plt.plot(L); plt.show()
		return L
	
	# -----------------------------------------------------------------------------
	def city(self, period=15*60, agressive=0, coldEng=0):
		VS = []; ES = []; APP = []; BPP = []; ECT = []
		
		# VS = self.randomized_sine(n=period, interval=self.city_VS)
		
		for t in range(period):
			vs = random.randint( self.city_VS[0], self.city_VS[1] )
			VS.append(vs)
		
		for t in range(period):
			es = random.randint( self.city_ES[0], self.city_ES[1] )
			ES.append(es)
		
		for t in range(period):
			app = random.randint( self.city_APP[0], self.city_APP[1] )
			APP.append(app)
		
		for t in range(period):
			bpp = random.randint( self.city_BPP[0], self.city_BPP[1] )
			BPP.append(bpp)
		
		ECT = self.coldEngine(period=period) if coldEng==1 else self.hotEngine(period=period)
		
		plt.plot(VS); plt.show()
		# plt.plot([500-5, 2000]); plt.plot(ES); plt.show()
		# plt.plot([0-5, 100]); plt.plot(APP); plt.show()
		# plt.plot([0-5, 40]); plt.plot(BPP); plt.show()
		# plt.plot([10-5, 85]); plt.plot(ECT); plt.show()
	
	# -----------------------------------------------------------------------------
	def countrySide(self, period=15*60, agressive=0, coldEng=0):
		VS = []; ES = []; APP = []; BPP = []; ECT = []
		
		for t in range(period):
			vs = random.randint( self.countrySide_VS[0], self.countrySide_VS[1] )
			VS.append(vs)
		
		for t in range(period):
			es = random.randint( self.countrySide_ES[0], self.countrySide_ES[1] )
			ES.append(es)
		
		for t in range(period):
			app = random.randint( self.countrySide_APP[0], self.countrySide_APP[1] )
			APP.append(app)
		
		for t in range(period):
			bpp = random.randint( self.countrySide_BPP[0], self.countrySide_BPP[1] )
			BPP.append(bpp)
		
		ECT = self.coldEngine(period=period) if coldEng==1 else self.hotEngine(period=period)
		
		plt.plot([0-5, 85]); plt.plot(VS); plt.show()
		plt.plot([500-5, 2000]); plt.plot(ES); plt.show()
		plt.plot([0-5, 100]); plt.plot(APP); plt.show()
		plt.plot([0-5, 40]); plt.plot(BPP); plt.show()
		plt.plot([10-5, 85]); plt.plot(ECT); plt.show()
	
	# -----------------------------------------------------------------------------
	def highway(self, period=15*60, agressive=0, coldEng=0):
		VS = []; ES = []; APP = []; BPP = []; ECT = []
		
		for t in range(period):
			vs = random.randint( self.highway_VS[0], self.highway_VS[1] )
			VS.append(vs)
		
		for t in range(period):
			es = random.randint( self.highway_ES[0], self.highway_ES[1] )
			ES.append(es)
		
		for t in range(period):
			app = random.randint( self.highway_APP[0], self.highway_APP[1] )
			APP.append(app)
		
		for t in range(period):
			bpp = random.randint( self.highway_BPP[0], self.highway_BPP[1] )
			BPP.append(bpp)
		
		ECT = self.coldEngine(period=period) if coldEng==1 else self.hotEngine(period=period)
		
		plt.plot([0-5, 85]); plt.plot(VS); plt.show()
		plt.plot([500-5, 2000]); plt.plot(ES); plt.show()
		plt.plot([0-5, 100]); plt.plot(APP); plt.show()
		plt.plot([0-5, 40]); plt.plot(BPP); plt.show()
		plt.plot([10-5, 85]); plt.plot(ECT); plt.show()
	
	# -----------------------------------------------------------------------------
	def coldEngine(self, period=15*60):
		ECT = []
		for t in range(period):
			ect = random.randint( self.coldEngine_ECT[0], self.coldEngine_ECT[1] )
			ECT.append(ect)
		return ECT
		
	# -----------------------------------------------------------------------------
	def hotEngine(self, period=15*60):
		ECT = []
		for t in range(period):
			ect = random.randint( self.hotEngine_ECT[0], self.hotEngine_ECT[1] )
			ECT.append(ect)
		return ECT
	
	# --------------------------------------------------------
	def divide(self, val, num=5, minSize=4):
		''' Divides val into # num chunks with each being at least of size minSize.
		It limits max size of a chunk using math.ceil(val/(num-len(chunks)))'''
		import random
		import math
		chunks = []
		for i in xrange(num-1):
			maxSize = math.ceil(val/(num-len(chunks)))
			newSize = random.randint(minSize, maxSize)
			val = val - newSize
			chunks.append(newSize)
		chunks.append(val)
		return chunks

