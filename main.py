import globals as gb
from Visualize import Visualize
from signalreader import SignalReader
from signalmerge import SignalMerge
from signalfeatures import SignalFeatures
from Clustering import Clustering
import os
import math
import datetime
import warnings
import numpy as np

# =================================================================
if __name__ == "__main__":
	warnings.simplefilter(action = "ignore", category = FutureWarning)
	viz = Visualize()
	
	#-----------------------------
	dbfiles = [gb.PATH + gb.VEHICLE + "_" + sig_id + ".db" for sig_id in gb.SIG_IDS]
	sigReaders = [ SignalReader(dbfile, preprocess=False) for dbfile in dbfiles ]
	
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
	
		times, axes = SignalMerge.merge( dicTS.values() )
		axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ] # FIXME
	
		# viz.plot(axes)
		
	viz.plot( zip(*DATA) )
	
	clu = Clustering(DATA).kmeans(k=5)
	clu.plot()
	
	exit(0)
	#-----------------------------
	dicTS = { gb.SIG_NAMES[isr] : sr.getSignal(start=gb.D_START, end=gb.D_END) for isr, sr in enumerate(sigReaders) }
	
	times, axes = SignalMerge.merge( dicTS.values() )
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ] # FIXME
	
	#-----------------------------
	for signame, (timestamps, values) in dicTS.items():
		viz.plot([timestamps, values], axs_labels=['Time', signame])
	
	viz.plot(axes)
	map(lambda sr: sr.closeDB(), sigReaders)