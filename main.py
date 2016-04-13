import globals as gb
import app
from Visualize import Visualize
from SignalReader import SignalReader
from SignalMerge import SignalMerge
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
	clust = app.cluster(sigReaders)
	clust.plot()
	
	app.project(sigReaders, clust)
	
	#-----------------------------
	exit(0)
	dicTS = { gb.SIG_NAMES[isr] : sr.getSignal(start=gb.D_START, end=gb.D_END) for isr, sr in enumerate(sigReaders) }
	
	times, axes = SignalMerge.merge( dicTS.values() )
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ] # FIXME
	
	#-----------------------------
	viz = Visualize()
	
	for signame, (timestamps, values) in dicTS.items():
		viz.plot([timestamps, values], axs_labels=['Time', signame])
	
	viz.plot(axes)
	map(lambda sr: sr.closeDB(), sigReaders)