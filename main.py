import globals as gb
import app
from Visualize import Visualize
from SignalReader import SignalReader
from SignalMerge import SignalMerge
from Clustering import Clustering
import os
import math
import datetime
import warnings
import numpy as np

# =================================================================
if __name__ == "__main__":
	warnings.simplefilter(action = "ignore", category = FutureWarning)
	dbfiles = [gb.PATH + gb.VEHICLE + "_" + sig_id + ".db" for sig_id in gb.SIG_IDS]
	sigReaders = [ SignalReader(dbfile, preprocess=False) for dbfile in dbfiles ]
	
	#-----------------------------
	DATA = app.buildTrainData(sigReaders)
	
	combinations=[]
	qualities=[]
	for n_features in range(2, len(DATA[0])):
		for k in range(2, 5):
			clust = Clustering(DATA, scale=True, n_features=n_features).kmeans(k=k)
			
			quality = clust.quality()
			print "n_features=", n_features, " ------ k=", k, " ------ quality=", quality
			# clust.plot()
			
			combinations.append( int(str(n_features)+str(k)) )
			qualities.append(quality)
	
			# app.project(sigReaders, clust)
	
	Visualize().plot( [combinations, qualities], axs_labels=['Combination ID (n_features k)', 'Quality'], marker="-" )
	
	
	#-----------------------------
	#-----------------------------
	#-----------------------------
	#-----------------------------
	exit(0) #FIXME
	dicTS = { gb.SIG_NAMES[isr] : sr.getSignal(start=gb.D_START_CLUSTERING, end=gb.D_END_CLUSTERING) for isr, sr in enumerate(sigReaders) }
	times, axes = SignalMerge.merge( dicTS.values() ) # TODO: integrate this in SignalFeatures by returning raw data instead of extracted features
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ] # FIXME
	
	#-----------------------------
	viz = Visualize()
	
	for signame, (timestamps, values) in dicTS.items():
		viz.plot([timestamps, values], axs_labels=['Time', signame])
	
	viz.plot(axes)
	map(lambda sr: sr.closeDB(), sigReaders)