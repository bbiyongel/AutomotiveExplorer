import globals as gb
from Visualize import Visualize
from SignalFeatures import SignalFeatures
from Clustering import Clustering
import datetime
import time
import pylab as plt

# =================================================================
def cluster(sigReaders, d_start=gb.D_START_CLUSTERING, d_end=gb.D_END_CLUSTERING):
	DATA = []
	date = d_start
	while date < d_end:
		print date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		dicTS = { gb.SIG_NAMES[isr] : sr.getSignal(start=date, end=gb.DURATION) for isr, sr in enumerate(sigReaders) }
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<3 for times, values in dicTS.values() ]): #FIXME: add this validation directly to extractMany
			continue
		
		x = SignalFeatures.extractMany([ values for times, values in dicTS.values() ])
		DATA.append(x)
		
	Visualize().plot( zip(*DATA) )
	clust = Clustering(DATA, scale=True).kmeans(k=3)
	return clust

# =================================================================
def project(sigReaders, clust, d_start=gb.D_START_PROJECTION, d_end=gb.D_END_PROJECTION):
	viz = Visualize()
	allPeriods_dicTS = [] # list of dicTS (subsequence of each signal), over all periods
	allPeriods_predY = [] # list of the predicted cluster id for dicTS, over all periods
	
	date = d_start
	while date < d_end:
		print date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		dicTS = { sr.signal_name : sr.getSignal(start=date, end=gb.DURATION) for sr in sigReaders }
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<3 for times, values in dicTS.values() ]): #FIXME: add this validation directly to extractMany
			continue
		
		x = SignalFeatures.extractMany([ values for times, values in dicTS.values() ])
		y = clust.predict(x) # get the cluster id (i.e., cluster label)
		
		allPeriods_dicTS.append( dicTS )
		allPeriods_predY.append( y )
		
		# for signame, (timestamps, values) in dicTS.items():
			# figurename = "plots/"+signame+"_"+str(y)+"_"+str(date).replace(":","-")+"_"+str(time.time())+".png"
			# viz.plot( [timestamps, values], axs_labels=['Time', signame], color=viz.colors[y%len(viz.colors)], fig=figurename )
		
	# -----------------
	signames = [ sr.signal_name for sr in sigReaders ]
	for signame in signames:
		signame_timestamps = []
		signame_values = []
		signame_labels = []
		
		times_vales_y = [ (dicTS[signame], y) for (dicTS, y) in zip(allPeriods_dicTS, allPeriods_predY) ]
		for (timestamps, values), y in times_vales_y:
			signame_timestamps += timestamps
			signame_values += values
			signame_labels += [ viz.colors[y%len(viz.colors)] for _ in values]
			
		figurename = "plots/"+signame+"_"+str(time.time())+".png"
		viz.plot( [signame_timestamps, signame_values], axs_labels=['Time', signame], color=signame_labels, fig=figurename )
	
	
# =================================================================
