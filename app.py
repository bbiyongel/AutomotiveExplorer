import globals as gb
from Visualize import Visualize
from SignalMerge import SignalMerge
from SignalFeatures import SignalFeatures
from sklearn.metrics import silhouette_score
from collections import defaultdict
import datetime
import time
import os
import random
import numpy as np
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
		
		if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]): #FIXME: add this validation directly to extractMany
			continue
		
		x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ]) #Warning: Future calls to extractMany should take the signals in same order
		DATA.append(x)
	
	return DATA
	
# =================================================================
def getLikelihoodsTransitions(sigReaders, clust, d_start=gb.D_START_MODEL_ESTIMARION, d_end=gb.D_END_MODEL_ESTIMARION, path=""):
	# ----------------- # This is the same as the first part of projectFeaturesData(...)
	dico = defaultdict(list)
	
	date = d_start
	while date < d_end:
		print "PROJECTION - MODEL ESTIMATION", date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		sigsNames = [ sr.signal_name for sr in sigReaders ] # FIXME: Out if the loop
		sigsTimeValues = [ sr.getSignal(start=date, end=gb.DURATION) for sr in sigReaders ]
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]): #FIXME: add this validation directly to extractMany
			continue
		
		x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ])
		y = clust.predict(x) # get the cluster id (i.e., cluster label)
		for signame, (times, values) in zip(sigsNames, sigsTimeValues):
			dico[signame+"TIMES"] += times
			dico[signame+"VALUES"] += values
			dico[signame+"PREDS"] += [y for _ in values]
	
	# ----------------- Transition model
	sr = sigReaders[0] # Transitions do not depend on the signal so we just use one of the signals
	seq_labels = dico[sr.signal_name+"PREDS"]
	uniq_labels = list(set(seq_labels))
	
	transitions = defaultdict(float)

	for t in range(1, len(seq_labels)):
		yi = seq_labels[t-1]
		yj = seq_labels[t]
		transitions[str(int(yi))+'-'+str(int(yj))] += 1
	
	normalizer = { str(int(yi)) : np.sum([ transitions[str(int(yi))+'-'+str(int(yk))] for yk in uniq_labels ]) for yi in uniq_labels }
	for yi in uniq_labels:
		for yj in uniq_labels:
			transitions[str(int(yi))+'-'+str(int(yj))] = transitions[str(int(yi))+'-'+str(int(yj))] / normalizer[str(int(yi))]
	
	print "transitions", transitions
	
	# ----------------- Likelihood model
	likelihoods = [ computeLikelihood( dico[sr.signal_name+"VALUES"] , dico[sr.signal_name+"PREDS"]) for sr in sigReaders ]
	print "likelihoods lens = ", [len(lkh) for lkh in likelihoods]
	
	# ----------------- Tracking equation test
	sigsTimeValues = [ ( dico[sr.signal_name+"TIMES"], dico[sr.signal_name+"VALUES"] ) for sr in sigReaders ]
	sigsTimeValues.append( ( dico[sigReaders[0].signal_name+"TIMES"], dico[sigReaders[0].signal_name+"PREDS"] ) ) # Add labels as an aditional timeseries
	
	times, axes = SignalMerge.merge( sigsTimeValues, interpolate=False )
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ]
	
	labels = [ int(y) for y in axes[-1] ]
	axes = axes[:-1]
	
	X = zip(*axes)
	
	for x in X:
		likeli_prod = np.product([ lk[x[ilk], y] for ilk, lk in enumerate(likelihoods) ])
		print likeli_prod

# =================================================================
def computeLikelihood(X, Y):
	foo = {}

	for (x, y) in zip(X, Y):
		bar = foo.setdefault(y, {})
		bar[x] = bar.setdefault(x, 0) + 1

	def prob(x, y, probDict):
		return 1.*probDict[y].get(x, 0) / np.sum(list(probDict[y].values()))

	# likelihood = defaultdict(float)
	likelihood = defaultdict(float)
	for x in list(set(X)):
		for y in list(set(Y)):
			# likelihood[str(x)+'-'+str(y)] = prob(x, y, foo)
			likelihood[x, y] = prob(x, y, foo)
	
	return likelihood
# =================================================================
def projectFeaturesData(sigReaders, clust, d_start=gb.D_START_PROJECTION, d_end=gb.D_END_PROJECTION, path=""):
	dico = defaultdict(list)
	
	date = d_start
	while date < d_end:
		print "PROJECTION", date, " --- ", date + datetime.timedelta(milliseconds=gb.DURATION)
		sigsNames = [ sr.signal_name for sr in sigReaders ] # FIXME: Out if the loop
		sigsTimeValues = [ sr.getSignal(start=date, end=gb.DURATION) for sr in sigReaders ]
		date += datetime.timedelta(milliseconds=gb.DURATION)
		
		if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]): #FIXME: add this validation directly to extractMany
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
		
		signame_labels = [ viz.colors[y%len(viz.colors)] for y in sig_y ]
		figurename = path+sr.signal_name+"_"+str(time.time())+".png"
		viz.plot( [sig_times, sig_values], axs_labels=['Time', sr.signal_name], color=signame_labels, fig=figurename )
	
	# -----------------
	sigsTimeValues = [ ( dico[sr.signal_name+"TIMES"], dico[sr.signal_name+"VALUES"] ) for sr in sigReaders ]
	sigsTimeValues.append( ( dico[sigReaders[0].signal_name+"TIMES"], dico[sigReaders[0].signal_name+"PREDS"] ) ) # Add labels as an aditional timeseries
	
	times, axes = SignalMerge.merge( sigsTimeValues, interpolate=False )
	axes = [ ax for ax in axes if all(not math.isnan(val) for val in ax) ]
	
	labels = [ int(y) for y in axes[-1] ]
	axes = axes[:-1]
	
	signame_labels = [ viz.colors[y%len(viz.colors)] for y in labels ]
	figurename = path+"_clustering_projection_AllSignals_"+str(time.time())+".png"
	viz.plot( axes, color=signame_labels, fig=figurename )
	
	X = zip(*axes)
	indexs = range(len(X)); random.shuffle(indexs)
	X = np.array([ X[i] for i in indexs[:10000] ])
	Y = np.array([ labels[i] for i in indexs[:10000] ])
	
	return silhouette_score( X, Y, metric='euclidean' )

# =================================================================
def logInformations( id_combin, clust, path="" ):
	print "id_combin", id_combin, "k", clust.k
	
	log = open( os.path.split(path)[0]+'/combins.txt', 'a' )
	log.write("COMB " + str(id_combin) + '\n')
	if clust.ids is not None:
		log.write(' - '.join(str(id) for id in clust.ids) + '\n')
		
	log.write(' - '.join( SignalFeatures().getFeaturesName(clust.ids) ) + '\n')
	log.write('\n')
	log.close()
	
	clust.plot( fig = path+'_clustering.png' )

# =================================================================
