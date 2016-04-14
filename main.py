import globals as gb
import app
from Visualize import Visualize
from SignalReader import SignalReader
from SignalMerge import SignalMerge
from Clustering import Clustering
import os
import math
from itertools import combinations
import datetime
import warnings
import numpy as np

# =================================================================
if __name__ == "__main__":
	viz = Visualize()
	warnings.simplefilter(action = "ignore", category = FutureWarning)
	dbfiles = [gb.PATH + gb.VEHICLE + "_" + sig_id + ".db" for sig_id in gb.SIG_IDS]
	sigReaders = [ SignalReader(dbfile, preprocess=False) for dbfile in dbfiles ]
	
	#-----------------------------
	DATA = app.buildTrainData(sigReaders)
	
	# features_combinations = range(2, len(DATA[0]))
	features_combinations = [ comb for comb in combinations( range( len(DATA[0])/10 ), 4 ) ]
	
	for k in range(2, 6):
		combos=[]; qualities=[]
		
		for id_combin, n_features in enumerate( features_combinations ):
			
			clust = Clustering(DATA, scale=True, features=n_features).kmeans(k=k) # clust.plot()
			quality = clust.quality()
			# app.project(sigReaders, clust)
			
			combos.append( id_combin )
			qualities.append(quality)
	
			print "k=", k, " ------ combination=", id_combin, " ------ quality=", quality
			
		viz.do_plot( [combos, qualities], axs_labels=['Combination (over features)', 'Quality'], marker="-", color=viz.cl(k-1), label="k="+str(k) )
	viz.end_plot( fig="plots/quality-combos.png" )
	
	#-----------------------------
	'''
	dicTS = { gb.SIG_NAMES[isr] : sr.getSignal(start=gb.D_START_CLUSTERING, end=gb.D_END_CLUSTERING) for isr, sr in enumerate(sigReaders) }
	times, axes = SignalMerge.merge( dicTS.values() ) # TODO: integrate this in SignalFeatures by returning raw data instead of extracted features
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ] # FIXME
	
	viz = Visualize()
	
	for signame, (timestamps, values) in dicTS.items():
		viz.plot([timestamps, values], axs_labels=['Time', signame])
	
	viz.plot(axes)
	'''
	
	#-----------------------------
	map(lambda sr: sr.closeDB(), sigReaders)
	
	