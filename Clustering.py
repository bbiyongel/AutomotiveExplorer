import numpy as np
from sklearn.cluster import KMeans
from Visualize import Visualize
from scipy.spatial import distance
import matplotlib.pyplot as plt

class Clustering:
	def __init__(self, X):
		self.random_seed = 12345 # set to None for random
		self.h = None
		self.labels = None
		self.X = X
    
	#---------------------------------------
	def dist_to_centers(self, X=None):
		if self.h is None:
			print "Clustering should be done before calling dist_to_centers."
			return
		
		if X is None:
			X = self.X
		
		centers = self.h.cluster_centers_ # FIXME: if the clustering has no centers, compute them based on clusters
		dists = []
		for center in centers:
			dists.append( [ distance.euclidean(x, center) for x in X ] )
			
		return dists
	
	#---------------------------------------
	def kmeans(self, k=2):
		self.h = KMeans(n_clusters = k, init = 'k-means++', n_init = 10, max_iter = 1000, tol = 0.00001, random_state = self.random_seed).fit( self.X )
		self.labels = self.h.labels_
		
		return self
		
	#---------------------------------------
	def plot(self):
		if self.labels is None:
			print "Clustering should be done before calling plot."
			return
		
		viz = Visualize()
		if len(self.X[0]) > 3:
			X = viz.PCA_Transform( zip(*self.X) )
		else:
			X = self.X
		
		unique_labels = np.unique(self.labels)
		clusters = { ul:[] for ul in unique_labels }
		
		for i in range( len(X) ):
			clusters[ self.labels[i] ].append( X[i] )
		
		centers_for_plot = [] # Not the real centers because dimension was reduced using PCA
		for label in clusters:
			centers_for_plot.append( [np.mean(col) for col in zip(* clusters[label] ) ] )
		
		viz.do_plot( zip(*centers_for_plot), marker='o', color='m' )
		viz.plot_groups(clusters)
	
	#---------------------------------------
	
	