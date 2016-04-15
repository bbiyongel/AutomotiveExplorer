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
	
	# -----------------------------
	DATA = app.buildTrainData(sigReaders)
	
	features_combinations = range(2, len(DATA[0]))
	# features_combinations = combinations( range( len(DATA[0]) ), 2 )
	
	# log = open('plots/combins.txt','a')
	
	for k in range(3, 6):
		combos=[]; qualities=[]
		
		for id_combin, n_features in enumerate( features_combinations ):
			log = open('plots/combins.txt','a')
			
			clust = Clustering(DATA, scale=True, features=n_features).kmeans(k=k)
			quality = clust.quality()
			
			print "k=", k, " ------ combination=", id_combin, " ------ quality=", quality, n_features
			if not os.path.exists("plots/k"+str(k)+"/"): os.makedirs("plots/k"+str(k)+"/")
			if not os.path.exists("plots/k"+str(k)+"/"+str(id_combin)+"/"): os.makedirs("plots/k"+str(k)+"/"+str(id_combin)+"/")
			plot_path = "plots/k"+str(k)+"/"+str(id_combin)+"/"
			
			log.write("COMB " + str(id_combin) + '\n')
			log.write('-'.join(str(id) for id in clust.ids) + '\n')
			log.write('-'.join( clust.getFeaturesName(clust.ids) ) + '\n')
			log.write('\n')
			log.close()
			
			# clust.plot( fig = plot_path+"_COMB"+'-'.join(str(id) for id in clust.ids)+"_QLT"+str(quality)+".png" )
			clust.plot( fig = plot_path+"_COMB_"+str(id_combin)+"_QLT"+str(quality)+".png" )
			app.project(sigReaders, clust, plot_path=plot_path)
			
			combos.append( id_combin )
			qualities.append(quality)
			
		viz.do_plot( [combos, qualities], axs_labels=['Combination (over features)', 'Quality'], marker="-", color=viz.cl(k-1), label="k="+str(k) )
	viz.end_plot( fig="plots/quality-combos.png" )
	
	# log.close()
	
	# -----------------------------
	'''
	dicTS = { sr.signal_name : sr.getSignal(start=gb.D_START_CLUSTERING, end=gb.D_END_CLUSTERING) for sr in sigReaders }
	times, axes = SignalMerge.merge( dicTS.values() ) # TODO: integrate this in SignalFeatures by returning raw data instead of extracted features
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ] # FIXME
	
	viz = Visualize()
	
	for signame, (timestamps, values) in dicTS.items():
		viz.plot([timestamps, values], axs_labels=['Time', signame])
	
	viz.plot(axes)
	'''
	
	# -----------------------------
	map(lambda sr: sr.closeDB(), sigReaders)
	
	