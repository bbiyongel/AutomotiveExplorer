import globals as gb
from signalreader import SignalReader
from signalmerge import SignalMerge
from signalfeatures import SignalFeatures
import os
import math
import datetime
import warnings
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

def plotting(axes):
	if len(axes) > 3:
		dim = 3
		pca = PCA(n_components=dim); X = zip(*axes); axes = zip(* pca.fit(X).transform(X) )
	
	if len(axes) == 3:
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(axes[0], axes[1], axes[2]); plt.show()
	elif len(axes) == 2:
		plt.scatter(axes[0], axes[1]); plt.show()
	elif len(axes) == 1:
		plt.scatter(range(len(axes[0])), axes[0]); plt.show()
	
# =================================================================
if __name__ == "__main__":
	matplotlib.rcParams['agg.path.chunksize']  = 20000
	warnings.simplefilter(action = "ignore", category = FutureWarning)
	
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
	
		# plotting(axes)
		
	plotting( zip(*DATA) )
	
	#-----------------------------
	dicTS = { gb.SIG_NAMES[isr] : sr.getSignal(start=gb.D_START, end=gb.D_END) for isr, sr in enumerate(sigReaders) }
	
	times, axes = SignalMerge.merge( dicTS.values() )
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ] # FIXME
	
	#-----------------------------
	# for signame, (timestamps, values) in dicTS.items():
		# plt.xlabel('Time'); plt.ylabel(signame); plt.plot(timestamps, values, 'b.'); plt.show()
	
	plotting(axes)
	map(lambda sr: sr.closeDB(), sigReaders)