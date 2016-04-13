import globals as gb
from Visualize import Visualize
from SignalFeatures import SignalFeatures
from Clustering import Clustering
import datetime
import time
import pylab as plt

# =================================================================
def cluster(sigReaders):
	DATA = []
	date = gb.D_START
	while date < gb.D_END:
		print date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		dicTS = { gb.SIG_NAMES[isr] : sr.getSignal(start=date, end=gb.DURATION) for isr, sr in enumerate(sigReaders) }
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<2 for times, values in dicTS.values() ]):
			continue
		
		x = SignalFeatures.extractMany([ values for times, values in dicTS.values() ])
		DATA.append(x)
		
	# Visualize().plot( zip(*DATA) )
	clust = Clustering(DATA).kmeans(k=5)
	return clust

# =================================================================
def project(sigReaders, clust):
	viz = Visualize()
	
	date = gb.D_START
	while date < gb.D_END:
		print date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		dicTS = { gb.SIG_NAMES[isr] : sr.getSignal(start=date, end=gb.DURATION) for isr, sr in enumerate(sigReaders) }
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<2 for times, values in dicTS.values() ]):
			continue
		
		x = SignalFeatures.extractMany([ values for times, values in dicTS.values() ])
		y = clust.project(x) # get the cluster id (i.e. cluster label)
		
		for signame, (timestamps, values) in dicTS.items():
			figurename = "plots/"+signame+"_"+str(y)+"_"+str(date).replace(":","-")+"_"+str(time.time())+".png"
			viz.plot( [timestamps, values], axs_labels=['Time', signame], color=viz.colors[y%len(viz.colors)], fig=figurename )
		
		# date += datetime.timedelta(milliseconds=gb.DURATION)
		
# =================================================================
