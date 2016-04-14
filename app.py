import globals as gb
from Visualize import Visualize
from SignalFeatures import SignalFeatures
from collections import defaultdict
import datetime
import time
import pylab as plt

# =================================================================
# TODO create a class with methods buildTrainData, project
def buildTrainData(sigReaders, d_start=gb.D_START_CLUSTERING, d_end=gb.D_END_CLUSTERING):
	DATA = []
	date = d_start
	while date < d_end:
		print date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		sigsTimeValues = [ sr.getSignal(start=date, end=gb.DURATION) for sr in sigReaders ]
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<3 for times, values in sigsTimeValues ]): #FIXME: add this validation directly to extractMany
			continue
		
		x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ]) #Warning: Future calls to extractMany should take the signals in same order
		DATA.append(x)
	
	return DATA

# =================================================================
def project(sigReaders, clust, d_start=gb.D_START_PROJECTION, d_end=gb.D_END_PROJECTION):
	viz = Visualize()
	dico = defaultdict(list)
	
	date = d_start
	while date < d_end:
		print date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		sigsNames = [ sr.signal_name for sr in sigReaders ] # Out
		sigsTimeValues = [ sr.getSignal(start=date, end=gb.DURATION) for sr in sigReaders ]
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<3 for times, values in sigsTimeValues ]): #FIXME: add this validation directly to extractMany
			continue
		
		x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ])
		y = clust.predict(x) # get the cluster id (i.e., cluster label)
		for signame, (times, values) in zip(sigsNames, sigsTimeValues):
			dico[signame+"TIMES"] += times
			dico[signame+"VALUES"] += values
			dico[signame+"PREDS"] += [y for _ in values]
		
	# -----------------
	for sr in sigReaders:
		sig_times, sig_values, sig_y = dico[sr.signal_name+"TIMES"], dico[sr.signal_name+"VALUES"], dico[sr.signal_name+"PREDS"]
		
		signame_labels = [ viz.colors[y%len(viz.colors)] for y in sig_y]
		figurename = "plots/"+sr.signal_name+"_"+str(time.time())+".png"
		viz.plot( [sig_times, sig_values], axs_labels=['Time', sr.signal_name], color=signame_labels, fig=figurename )

# =================================================================
