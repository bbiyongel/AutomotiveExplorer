import globals as gb
from Visualize import Visualize
from SignalMerge import SignalMerge
from SignalFeatures import SignalFeatures
from ModeTracking import ModeTracking
from sklearn.metrics import silhouette_score
from collections import defaultdict
import datetime
import time
import os
import sys
import random
import numpy as np
import math
import pylab as plt

class App:
	def __init__(self, sigReaders):
		self.sigReaders = sigReaders
	
	# -----------------------------------------
	def build_features_data(self, d_start=gb.D_START_CLUSTERING, d_end=gb.D_END_CLUSTERING):
		DATA = []
		date = d_start
		while date < d_end:
			sys.stdout.write("\r%s" % "build_features_data --- " + str(date)); sys.stdout.flush()
			sigsTimeValues = [ sr.getSignal(start=date, end=gb.DURATION) for sr in self.sigReaders ]
			date += datetime.timedelta(milliseconds=gb.DURATION)
			
			if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]):
				continue
			
			x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ]) #Warning: Future calls to extractMany should take the signals in same order
			DATA.append(x)
		
		return DATA
		
	# -----------------------------------------
	''' Predict from the clustering done in the feature space '''
	def predict_fsp(self, d_start, d_end):
		dico = defaultdict(list)
		
		date = d_start
		while date < d_end:
			sys.stdout.write("\r%s" % "predict_fsp --- " + str(date)); sys.stdout.flush()
			sigsNames = [ sr.signal_name for sr in self.sigReaders ] # FIXME: Out if the loop
			sigsTimeValues = [ sr.getSignal(start=date, end=gb.DURATION, dated=True) for sr in self.sigReaders ]
			date += datetime.timedelta(milliseconds=gb.DURATION)
			
			if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]):
				continue
			
			x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ])
			y = self.clust.predict(x) # get the cluster id (i.e., cluster label)
			for signame, (times, values) in zip(sigsNames, sigsTimeValues):
				dico[signame+"TIMES"] += times
				dico[signame+"VALUES"] += values
				dico[signame+"PREDS"] += [y for _ in values]
		
		# ----------------- Merging signals
		sigsTimeValues = [ ( dico[sr.signal_name+"TIMES"], dico[sr.signal_name+"VALUES"] ) for sr in self.sigReaders ]
		sigsTimeValues.append( ( dico[self.sigReaders[0].signal_name+"TIMES"], dico[self.sigReaders[0].signal_name+"PREDS"] ) ) # Add labels as an aditional timeseries
		if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]):
			return [], [], []
		
		times, axes = SignalMerge.merge( sigsTimeValues, interpolate=False )
		
		labels = [ int(y) for y in axes[-1] ]
		axes = axes[:-1]
		
		return times, axes, labels
	
	# -----------------------------------------
	def predict_ssp(self, d_start, d_end):
		sigsTimeValues = [ sr.getSignal(start=d_start, end=d_end, dated=True) for sr in self.sigReaders ]
		if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]):
			return [], [], []
		
		times, axes = SignalMerge.merge( sigsTimeValues, interpolate=False )
		
		X = zip(*axes)
		labels = []
		
		for t, x in enumerate(X):
			pred_mode = self.tracker.track(x)
			labels.append(pred_mode)
			# print "predict_ssp", "\t pred_mode", pred_mode, "\t progress", t*100./len(X), times[t]
			sys.stdout.write("\r%s" % "predict_ssp \t pred_mode " + str(pred_mode) + "\t progress " + str(t*100./len(X)) + " " + str(times[t])); sys.stdout.flush()
		
		return times, axes, labels
		
	# -----------------------------------------
	def plot_colored_signals(self, times, axes, labels, path, figname):
		viz = Visualize()
		signame_labels = [ viz.colors[y%len(viz.colors)] for y in labels ]
		
		for isr, sr in enumerate(self.sigReaders):
			figurename = path+sr.signal_name+"_"+str(time.time())+figname
			viz.plot( [ times, axes[isr] ], axs_labels=['Time', sr.signal_name], color=signame_labels, fig=figurename )
			
		figurename = path+"_clustering_projection_AllSignals_"+str(time.time())+figname
		viz.plot( axes, color=signame_labels, fig=figurename )
	
	# -----------------------------------------
	def init_clust_tracker(self, clust, d_start=gb.D_START_CLUSTERING, d_end=gb.D_END_CLUSTERING):
		self.clust = clust
		self.tracker = ModeTracking()
		
		# ------------- Initialize the Transition and Likelihoods based on the clustering result
		step = 86400000 * 3 # read chunk by chunk of (each chunk is of 'step' milliseconds)
		date = d_start
		while date < d_end:
			times, axes, labels = self.predict_fsp(d_start=date, d_end=date + datetime.timedelta(milliseconds=step))
			date = date + datetime.timedelta(milliseconds=step)
			
			self.tracker.update_transition( labels )
			self.tracker.update_likelihoods( axes, labels )
		
	# -----------------------------------------
	def track_and_update(self, d_start=gb.D_START_TRACKING, d_end=gb.D_END_TRACKING):
		step = 86400000 * 3  # read chunk by chunk of (each chunk is of 'step' milliseconds)
		date = d_start
		while date < d_end:
			times, axes, labels = self.predict_ssp(d_start=d_start, d_end=date + datetime.timedelta(milliseconds=step))
			date = date + datetime.timedelta(milliseconds=step)
			print "track_and_update", date
			
			self.tracker.update_transition( labels )
			self.tracker.update_likelihoods( axes, labels )
			
		
	# -----------------------------------------
	def projecting(self, d_start=gb.D_START_PROJECTION, d_end=gb.D_END_PROJECTION, path=""):
		times, axes, labels = self.predict_fsp(d_start=d_start, d_end=d_end)
		self.plot_colored_signals(times, axes, labels, path, figname="_FeatureSpace.png")
		silhouette_fsp = None#self.silhouette(axes, labels)
		
		times, axes, labels = self.predict_ssp(d_start=d_start, d_end=d_end)
		self.plot_colored_signals(times, axes, labels, path, figname="_SignalSpace.png")
		silhouette_ssp = None#self.silhouette(axes, labels)
		
		return silhouette_fsp, silhouette_ssp
		
	# -----------------------------------------
	def silhouette(self, axes, labels):
		limit = 10000 # FIXME: this is a quick hack to avoid memory error (for big amount of data)
		X = zip(*axes)
		indexs = range(len(X))
		random.shuffle(indexs)
		X = np.array([ X[i] for i in indexs[:limit] ])
		Y = np.array([ labels[i] for i in indexs[:limit] ])
		
		return silhouette_score( X, Y, metric='euclidean' )
		
	# -----------------------------------------
	def logInformations(self, id_combin, clust, path="" ):
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
