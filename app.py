import globals as gb
from Visualize import Visualize
from SignalMerge import SignalMerge
from SignalFeatures import SignalFeatures
from collections import defaultdict
import datetime
import time
import math
import pylab as plt

# =================================================================
def buildRawData(sigReaders, d_start=gb.D_START_CLUSTERING, d_end=gb.D_END_CLUSTERING):
	sigsTimeValues = [ sr.getSignal(start=d_start, end=d_end) for sr in sigReaders ]
	
	times, axes = SignalMerge.merge( sigsTimeValues )
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ]
	# Visualize().plot(axes) # FOR DEBUG
	
	DATA = zip(*axes)
	DATA = [list(x) for x in DATA]
	
	return DATA

# =================================================================
def projectRawData(sigReaders, clust, d_start=gb.D_START_PROJECTION, d_end=gb.D_END_PROJECTION, path=""):
	sigsTimeValues = [ sr.getSignal(start=d_start, end=d_end) for sr in sigReaders ]
	
	times, axes = SignalMerge.merge( sigsTimeValues, interpolate=False )
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ]
	# Visualize().plot(axes) # FOR DEBUG
	
	DATA = zip(*axes)
	Y = clust.predictAll(DATA) # get the cluster id (i.e., cluster label) for each instance un DATA
	
	dico = defaultdict(list)
	sigsNames = [ sr.signal_name for sr in sigReaders ]
	
	for signame, values in zip(sigsNames, axes):
		dico[signame+"TIMES"] = times
		dico[signame+"VALUES"] = values
		dico[signame+"PREDS"] = Y
	
	# for tm, x in zip(times, DATA):
		# y = clust.predict(x) 
		# for ix, signame in enumerate(sigsNames):
			# dico[signame+"TIMES"].append( tm )
			# dico[signame+"VALUES"].append( x[ix] )
			# dico[signame+"PREDS"].append( y )
			
	# -----------------
	viz = Visualize()
	for sr in sigReaders:
		sig_times, sig_values, sig_y = dico[sr.signal_name+"TIMES"], dico[sr.signal_name+"VALUES"], dico[sr.signal_name+"PREDS"]
		
		signame_labels = [ viz.colors[y%len(viz.colors)] for y in sig_y]
		figurename = path+sr.signal_name+"_"+str(time.time())+".png"
		viz.plot( [sig_times, sig_values], axs_labels=['Time', sr.signal_name], color=signame_labels, fig=figurename )
		
# =================================================================
def buildFeaturesData(sigReaders, d_start=gb.D_START_CLUSTERING, d_end=gb.D_END_CLUSTERING):
	DATA = []
	date = d_start
	while date < d_end:
		print date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		sigsTimeValues = [ sr.getSignal(start=date, end=gb.DURATION) for sr in sigReaders ]
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<3 for times, values in sigsTimeValues ]): #FIXME: add this validation directly to extractMany
			continue
		
		x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ]) #Warning: Future calls to extractMany should take the signals in same order
		DATA.append(x)
	
	return DATA
	
# =================================================================
def projectFeaturesData(sigReaders, clust, d_start=gb.D_START_PROJECTION, d_end=gb.D_END_PROJECTION, path=""):
	dico = defaultdict(list)
	
	date = d_start
	while date < d_end:
		print "PROJECTION", date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		sigsNames = [ sr.signal_name for sr in sigReaders ] # FIXME: Out if the loop
		sigsTimeValues = [ sr.getSignal(start=date, end=gb.DURATION) for sr in sigReaders ]
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<3 for times, values in sigsTimeValues ]): #FIXME: add this validation directly to extractMany
			continue
		
		x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ])
		y = clust.predict(x) # get the cluster id (i.e., cluster label)
		for signame, (times, values) in zip(sigsNames, sigsTimeValues):
			dico[signame+"TIMES"] += times
			dico[signame+"VALUES"] += values
			dico[signame+"PREDS"] += [y for _ in values]
		
	# -----------------
	viz = Visualize()
	for sr in sigReaders:
		sig_times, sig_values, sig_y = dico[sr.signal_name+"TIMES"], dico[sr.signal_name+"VALUES"], dico[sr.signal_name+"PREDS"]
		
		signame_labels = [ viz.colors[y%len(viz.colors)] for y in sig_y]
		figurename = path+sr.signal_name+"_"+str(time.time())+".png"
		viz.plot( [sig_times, sig_values], axs_labels=['Time', sr.signal_name], color=signame_labels, fig=figurename )

# =================================================================
def logInformations( id_combin, clust, path="" ):
	print "id_combin", id_combin, "k", clust.k
	
	log = open( 'plots/combins.txt', 'a' )
	log.write("COMB " + str(id_combin) + '\n')
	if clust.ids is not None:
		log.write(' - '.join(str(id) for id in clust.ids) + '\n')
		
	log.write(' - '.join( SignalFeatures().getFeaturesName(clust.ids) ) + '\n')
	log.write('\n')
	log.close()
	
	clust.plot( fig = path+'_clustering.png' )

# =================================================================
