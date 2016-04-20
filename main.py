import globals as gb
import app
from Visualize import Visualize
from SignalReader import SignalReader
from Clustering import Clustering
import os
import math
import random
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
	
	# -----------------------------
	DATA = app.buildFeaturesData(sigReaders)
	
	ranges_comb = list(range( len(DATA[0]) )); random.shuffle(ranges_comb)
	
	for k in range(2, 4):
		combos=[]; qualities=[]
		
		# features_combinations = combinations( ranges_comb, 3 )
		features_combinations = range(2, len(DATA[0]))
		
		for id_combin, n_features in enumerate( features_combinations ):
			# clust = Clustering(DATA, scale=True, features=None).kmeans(k=k)
			clust = Clustering(DATA, scale=True, features=n_features).kmeans(k=k)
			
			quality = clust.quality()
			
			path = 'plots/'+str(id_combin)+'/'
			app.logInformations( id_combin=id_combin, clust=clust, path=path )
			
			app.projectFeaturesData(sigReaders, clust, path= path )
			
			combos.append( id_combin )
			qualities.append(quality)
			
		viz.do_plot( [combos, qualities], axs_labels=['Combination (over features)', 'Quality'], marker="-", color=viz.cl(k-1), label="k="+str(k) )
	viz.end_plot( fig="plots/quality-combos.png" )
	
	# -----------------------------
	'''
	dicTS = { sr.signal_name : sr.getSignal(start=gb.D_START_CLUSTERING, end=gb.D_END_CLUSTERING) for sr in sigReaders }
	times, axes = SignalMerge.merge( dicTS.values() ) # TODO: integrate this in SignalFeatures by returning raw data instead of extracted features
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ] # FIXME
	
	
	'''
	
	# -----------------------------
	map(lambda sr: sr.closeDB(), sigReaders)
	
	