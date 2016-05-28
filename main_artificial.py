import globals as gb
from App import App
from Visualize import Visualize
from SignalReader import SignalReader
from SignalReaderArtificial import SignalReaderArtificial
from Clustering import Clustering
from ArtificialData import ArtificialData
import itertools
import os
import math
import random
import datetime
import warnings
import numpy as np

# =================================================================
if __name__ == "__main__":
	warnings.simplefilter(action = "ignore", category = FutureWarning)
	random.seed(1234)
	viz = Visualize()
	
	# -----------------------------
	parts = 30
	enable_agg = False
	
	# -----------------------------
	# Ks = [3, 6] # Clusters
	# Ds = [1, 5, 10, 15, 30, 60] # Duration window
	# Ns = [0., 5., 10., 15., 20.] # Noise level
	# Ps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] # Patterns similarity (difficulty)
	
	Ks = [3]
	Ds = [10]
	Ns = [1.]
	Ps = [0.1]
	
	# combos = list(itertools.product(Ks, Ds, Ns)); combo_name = ("Ks", "Ds", "Ns"); params = Ps
	combos = list(itertools.product(Ks, Ps, Ns)); combo_name = ("Ks", "Ps", "Ns"); params = Ds
	
	for comb in combos:
		# (K, D, N) = comb
		(K, P, N) = comb
		vals = []; fsp_acc = []; ssp_acc = []
		
		for param in params:
			# P = param
			D = param
			
			id_combin = "-".join([ str(vn)+str(v) for v,vn in zip(comb, combo_name) ]) + "-Agg"+str(enable_agg)
			vals.append(param)
			gb.K = K
			gb.DURATION = D * 60*1000
			
			signalsValues, modes = ArtificialData(noise=N, ptrn=P).run(parts=parts, enable_agg=enable_agg) # VS, ES, APP, BPP, ECT
			sigReaders = [ SignalReaderArtificial(signame="Signal"+str(i), sigvalues=values, modes=modes) for i,values in enumerate(signalsValues) ]
			app = App(sigReaders)
			
			DATA = app.build_features_data()
			clust = Clustering(DATA, scale=True, features=None).dpgmm(k=gb.K) # kmeans, dpgmm
			app.init_clust_tracker(clust)
			
			PLOT_PATH = gb.PLOT_PATH + str(id_combin) + '/' + str(param) + '/'
			if not os.path.exists(PLOT_PATH): os.makedirs(PLOT_PATH)
			path = PLOT_PATH+str(id_combin)+'_'
			app.logInformations( id_combin=id_combin, clust=clust, path=path )
			
			qualityFSP, qualitySSP = app.tracking(path=path)
			fsp_acc.append(qualityFSP)
			ssp_acc.append(qualitySSP)
			
		viz.do_plot( [vals, fsp_acc], axs_labels=['Parameter values', 'Acc'], marker="-", color="red", label="fsp_acc" )
		viz.do_plot( [vals, ssp_acc], axs_labels=['Parameter values', 'Acc'], marker="-", color="blue", label="ssp_acc" )
		viz.end_plot( fig="plots/Acc_"+str(id_combin)+".png" )
	
	# -----------------------------
	map(lambda sr: sr.closeDB(), sigReaders)
	
	