import globals as gb
import app
from Visualize import Visualize
from SignalReader import SignalReader
from Clustering import Clustering
import os
import math
import random
import datetime
import warnings
import numpy as np

# =================================================================
def getCombinations( L, nb=20, length=60 ):
	combs = set()
	while len(combs) < nb:
		combs.add( tuple(sorted(random.sample(L, length))) )
	return list(combs)
	
# =================================================================
if __name__ == "__main__":
	warnings.simplefilter(action = "ignore", category = FutureWarning)
	dbfiles = [gb.PATH + gb.VEHICLE + "_" + sig_id + ".db" for sig_id in gb.SIG_IDS]
	sigReaders = [ SignalReader(dbfile, preprocess=False) for dbfile in dbfiles ]
	
	# -----------------------------
	DATA = app.buildFeaturesData(sigReaders)
	
	features_combinations = getCombinations( range(len(DATA[0])) )
	# features_combinations = range(2, len(DATA[0]))
	
	combos=[]; qualities=[]; qualitiesSS=[]
	for id_combin, n_features in enumerate( features_combinations ):
		clust = Clustering(DATA, scale=True, features=n_features).dpgmm(k=5) # kmeans(k=2), gmm(k=2)
		
		quality = clust.quality()
		
		if not os.path.exists('plots/combs60/'): os.makedirs('plots/combs60/')
		path = 'plots/combs60/'+str(id_combin)+'_'+str(quality)+'_'
		app.logInformations( id_combin=id_combin, clust=clust, path=path )
		
		app.getLikelihoodsTransitions( sigReaders, clust, path= path )
		qualitySS = app.projectFeaturesData(sigReaders, clust, path= path )
		
		combos.append( id_combin )
		qualities.append(quality)
		qualitiesSS.append(qualitySS)
		
	Visualize().plot( [combos, qualities], axs_labels=['Combination (over features)', 'Quality'], marker="-", label="id_combin="+str(id_combin), fig="plots/quality-combos.png" )
	Visualize().plot( [combos, qualitiesSS], axs_labels=['Combination (over features)', 'qualitySS'], marker="-", label="id_combin="+str(id_combin), fig="plots/qualitySS-combos.png" )
	
	# -----------------------------
	map(lambda sr: sr.closeDB(), sigReaders)
	
	