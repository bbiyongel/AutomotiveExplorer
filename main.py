import globals as gb
from App import App
from Visualize import Visualize
from SignalReader import SignalReader
from Clustering import Clustering
from ArtificialData import ArtificialData
import os
import math
import random
import datetime
import warnings
import numpy as np

# =================================================================
def getCombinations( L, nb=20, length=3 ):
	combs = set()
	counter = 0
	while len(combs) < nb:
		combs.add( tuple(sorted(random.sample(L, length))) )
		
		counter += 1
		if counter > nb+10: break # FIXME: a quick hack to avoid looping for a long time
		
	return list(combs)
	
# =================================================================
if __name__ == "__main__":
	warnings.simplefilter(action = "ignore", category = FutureWarning)
	
	# art = ArtificialData()
	# art.run(parts=5)
	# exit(0)
	
	# -----------------------------
	dbfiles = [gb.DATA_PATH + gb.VEHICLE + "_" + sig_id + ".db" for sig_id in gb.SIG_IDS]
	sigReaders = [ SignalReader(dbfile, preprocess=False) for dbfile in dbfiles ]
	
	# -----------------------------
	app = App(sigReaders)
	DATA = app.build_features_data()
	
	k = 4
	
	features_combinations = getCombinations( range(len(DATA[0])), nb=20, length=2 )
	# features_combinations = range(2, len(DATA[0]))
	
	combos=[]; qualitiesFSP=[]; qualitiesSSP=[]
	for id_combin, n_features in enumerate( features_combinations ):
		clust = Clustering(DATA, scale=True, features=None).dpgmm(k=k) # kmeans, dpgmm
		# clust = Clustering(DATA, scale=True, features=n_features).gmm(k=k)
		
		app.init_clust_tracker(clust)
		
		PLOT_PATH = gb.PLOT_PATH + str(id_combin) + '/'
		
		if not os.path.exists(PLOT_PATH): os.makedirs(PLOT_PATH)
		path = PLOT_PATH+str(id_combin)+'_'
		app.logInformations( id_combin=id_combin, clust=clust, path=path )
		
		qualityFSP, qualitySSP = app.tracking(path=path)
		
		combos.append( id_combin )
		qualitiesFSP.append(qualityFSP)
		qualitiesSSP.append(qualitySSP)
		break
	
	print "qualitiesFSP/qualitiesSSP", zip(qualitiesFSP, qualitiesSSP)
	Visualize().plot( [combos, qualitiesFSP], axs_labels=['Combination (over features)', 'Quality'], marker="-", label="id_combin="+str(id_combin), fig="plots/quality-combos.png" )
	Visualize().plot( [combos, qualitiesSSP], axs_labels=['Combination (over features)', 'qualitySS'], marker="-", label="id_combin="+str(id_combin), fig="plots/qualitySS-combos.png" )
	
	# -----------------------------
	map(lambda sr: sr.closeDB(), sigReaders)
	
	