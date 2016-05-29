import globals as gb
from Visualize import Visualize
from SignalMerge import SignalMerge
from SignalFeatures import SignalFeatures
from ModeTracking import ModeTracking
from sklearn.metrics import silhouette_score, adjusted_rand_score
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
		
		sigsTimeValues = [ sr.getSignal() for sr in self.sigReaders ]
		sigsValues = [ values for times, values in sigsTimeValues ]
		self.sigsRanges = [ (min(values), max(values), min(np.gradient(values)), max(np.gradient(values))) for values in sigsValues ]
	
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
			
			x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ], self.sigsRanges) #Warning: Future calls to extractMany should take the signals in same order
			DATA.append(x)
		
		return DATA
		
	# -----------------------------------------
	''' Predict from the clustering done in the feature space '''
	def predict_fsp(self, d_start, d_end, D=gb.DURATION):
		dico = defaultdict(list)
		
		timedelta = datetime.timedelta(milliseconds=D)
		date = d_start
		while date < d_end:
			sys.stdout.write("\r%s" % "predict_fsp --- " + str(date)); sys.stdout.flush()
			sigsNames = [ sr.signal_name for sr in self.sigReaders ] # FIXME: Out if the loop
			
			if date + timedelta >= d_end: timedelta = d_end - date
			sigsTimeValues = [ sr.getSignal(start=date, end=date + timedelta, dated=gb.DATED) for sr in self.sigReaders ]
			date += timedelta
			
			if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]):
				continue
			
			x = SignalFeatures().extractMany([ values for times, values in sigsTimeValues ], self.sigsRanges)
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
	def predict_ssp(self, d_start, d_end, update=False):
		sigsTimeValues = [ sr.getSignal(start=d_start, end=d_end, dated=gb.DATED) for sr in self.sigReaders ]
		if any([ len(values)<gb.MIN_SUBSEQUENCE_LEN for times, values in sigsTimeValues ]):
			return [], [], []
		
		times, axes = SignalMerge.merge( sigsTimeValues, interpolate=False )
		
		X = zip(*axes)
		labels = []
		
		for t, x in enumerate(X):
			pred_mode = self.tracker.track(x, update=update)
			labels.append(pred_mode)
			sys.stdout.write("\r%s" % "predict_ssp \t pred_mode " + str(pred_mode) + "\t progress " + str(t*100./len(X)) + " " + str(times[t])); sys.stdout.flush()
		
		return times, axes, labels
		
	# -----------------------------------------
	def plot_colored_signals(self, times, axes, labels, path, figname):
		viz = Visualize()
		signame_labels = [ viz.colors[y%len(viz.colors)] for y in labels ]
		
		if len(axes) < len(self.sigReaders):
			return
			
		for isr, sr in enumerate(self.sigReaders):
			figurename = path+sr.signal_name+"_"+str(time.time())+figname
			viz.plot( [ times, axes[isr] ], axs_labels=['Time', sr.signal_name], color=signame_labels, fig=figurename )
			
		figurename = path+"_clustering_projection_AllSignals_"+str(time.time())+figname
		viz.plot( axes, color=signame_labels, fig=figurename )
	
	# -----------------------------------------
	def init_clust_tracker(self, clust, d_start=gb.D_START_INIT_TRACKER, d_end=gb.D_END_INIT_TRACKER):
		print "\n --------- init_clust_tracker ..."
		
		self.clust = clust
		self.tracker = ModeTracking(type=gb.PROBA_TYPE)
		
		# ------------- Initialize the Transition and Likelihoods based on the clustering result
		timedelta = datetime.timedelta(milliseconds=86400000 * 1) # read chunk by chunk of (each chunk is of 'step' milliseconds)
		date = d_start
		while date < d_end:
			if date + timedelta >= d_end: timedelta = d_end - date
			times, axes, labels = self.predict_fsp(d_start=date, d_end=date + timedelta)
			date += timedelta
			
			self.tracker.update_transition( labels )
			self.tracker.update_likelihoods( axes, labels )
		
	# -----------------------------------------
	def tracking(self, d_start=gb.D_START_TRACKING, d_end=gb.D_END_TRACKING, path=""):
		print "\n --------- tracking ..."
		
		times_fsp, axes_fsp, labels_fsp = [], [], []
		times_ssp, axes_ssp, labels_ssp = [], [], []
		
		timedelta = datetime.timedelta(milliseconds=60 * 60*1000) # read chunk by chunk (each chunk is of 'timedelta' milliseconds)
		date = d_start
		while date < d_end:
			if date + timedelta >= d_end: timedelta = d_end - date
			
			times, axes, labels = self.predict_fsp(d_start=date, d_end=date + timedelta)
			# self.plot_colored_signals(times, axes, labels, path, figname="_FSP.png")
			times_fsp += times; axes_fsp += axes; labels_fsp += labels
			
			times, axes, labels = self.predict_ssp(d_start=date, d_end=date + timedelta, update=True)
			# self.plot_colored_signals(times, axes, labels, path, figname="_SSP.png")
			times_ssp += times; axes_ssp += axes; labels_ssp += labels
			
			date += timedelta
		
		# ----------------------------
		if gb.ARTIFICIAL:
			times, values, true_labels = self.sigReaders[0].getSignal(start=d_start, end=d_end, dated=gb.DATED, get_modes=True)
			score_fps = adjusted_rand_score(true_labels, labels_fsp)
			score_sps = adjusted_rand_score(true_labels, labels_ssp)
			print "---------------------------------------------------"
			print "adjusted_rand_score FSP:", score_fps
			print "adjusted_rand_score SSP:", score_sps
			return score_fps, score_sps
		# ----------------------------
		return 0., 0.
		# return self.silhouette(axes_fsp, labels_fsp), self.silhouette(axes_ssp, labels_ssp)
		
	# -----------------------------------------
	def silhouette(self, axes, labels):
		limit = 10000 # FIXME: this is a quick hack to avoid memory errors (for big amount of data)
		X = zip(*axes)
		indexs = range(len(X))
		random.shuffle(indexs)
		X = np.array([ X[i] for i in indexs[:limit] ])
		Y = np.array([ labels[i] for i in indexs[:limit] ])
		
		return silhouette_score( X, Y, metric='euclidean' )
		
	# -----------------------------------------
	def logInformations(self, id_combin, clust, path="" ):
		print "\n id_combin", id_combin, "k", clust.k
		
		log = open( os.path.split(path)[0]+'/combins.txt', 'a' )
		log.write("COMB " + str(id_combin) + '\n')
		if clust.ids is not None:
			log.write(' - '.join(str(id) for id in clust.ids) + '\n')
			
		log.write(' - '.join( SignalFeatures().getFeaturesName(clust.ids) ) + '\n')
		log.write('\n')
		log.close()
		
		clust.plot( fig = path+'_clustering.png' )

# =================================================================
