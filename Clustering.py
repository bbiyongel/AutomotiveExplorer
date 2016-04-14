import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.feature_selection import VarianceThreshold
from Visualize import Visualize
from scipy.spatial import distance
import matplotlib.pyplot as plt

class Clustering:
	# def __init__(self, X, scale=False, n_features=None, feature_ids=None):
	def __init__(self, X, scale=False, features=None):
		self.random_seed = 12345 # set to None for random
		self.X = X
		
		self.h = None
		self.Y = None
		
		self.scaler = None
		self.ids = None
		
		# Visualize().plot( zip(*self.X) ) # FOR DEBUG
		
		# Reduce the number of features
		if features is not None:
			if isinstance( features, (int, long, float) ):
				variances = VarianceThreshold().fit(self.X).variances_
				self.ids = sorted(range(len(variances)), key=lambda i: variances[i])[-int(features):] # indexes of the top n_features values in variances
			elif type(features) in [list,tuple]:
				self.ids = features #TODO validate that features is a list of ints and len(features) <= len(self.X[0])
				
			self.X = self.reduceFeatures(self.X)
			# print "Selected features", self.ids, "on a total of", len(X[0])  # FOR DEBUG
			
		# Reduce the number of features by using only the specified features
		# if feature_ids is not None:
			# self.ids = feature_ids
			# self.X = self.reduceFeatures(self.X)
			
		# Reduce the number of features to n_features by eliminating low variance features
		# if n_features is not None:
			# variances = VarianceThreshold().fit(self.X).variances_
			# self.ids = sorted(range(len(variances)), key=lambda i: variances[i])[-n_features:] # indexes of the top n_features values in variances
			# self.X = self.reduceFeatures(self.X)
			
			
		if scale:
			self.scaler = MinMaxScaler() # StandardScaler() can also be used instead of MinMaxScaler()
			self.X = self.scaler.fit_transform(self.X)
		
		# Visualize().plot( zip(*self.X) ) # FOR DEBUG
    
	#---------------------------------------
	def reduceFeatures(self, X):
		if self.ids is None:
			return X
		else:
			return [ [v for iv,v in enumerate(x) if iv in self.ids] for x in X ]
	
	#---------------------------------------
	def kmeans(self, k=2):
		self.h = KMeans(n_clusters = k, init = 'k-means++', n_init = 10, max_iter = 1000, tol = 0.00001, random_state = self.random_seed).fit( self.X )
		self.Y = self.h.labels_
		
		return self
		
	#---------------------------------------
	def done(self):
		if self.h is None:
			print "Clustering is not yet done !"
			return False
		else:
			return True
			
	#---------------------------------------
	def getCenters(self):
		if not self.done(): return
		
		try:
			return self.h.cluster_centers_
		
		# If the clustering has no centers, compute them based on clusters
		except AttributeError: 
			unique_labels = np.unique(self.Y)
			clusters = { ul:[] for ul in unique_labels }
			
			for i in range( len(X) ):
				clusters[ self.Y[i] ].append( X[i] )
			
			centers = []
			for label in clusters:
				centers.append( [np.mean(col) for col in zip(* clusters[label] ) ] )

			return centers
		
	#---------------------------------------
	def predict(self, x):
		if not self.done(): return
		x_processed = x
		x_processed = self.reduceFeatures([x_processed])[0]
		x_processed = x_processed if self.scaler is None else self.scaler.transform(x_processed)
		return self.h.predict(x_processed)[0]
	
	#---------------------------------------
	def predictAll(self, X):
		if not self.done(): return
		X_processed = X
		X_processed = self.reduceFeatures(X_processed)
		X_processed = X_processed if self.scaler is None else self.scaler.transform(X_processed)
		return self.h.predict(X_processed)
	
	#---------------------------------------
	def quality(self, X=None):
		if not self.done(): return
		
		if X is None: # if X not provided then use the training data and resulting labels
			X = self.X
			Y = self.Y
		else: # if X is provided then use it with the predicted labels (clusters)
			Y = self.predictAll(X)
		
		return silhouette_score(X, Y, metric='euclidean')
		
	#---------------------------------------
	def plot(self):
		if not self.done(): return
		
		viz = Visualize()
		if len(self.X[0]) > 3:
			X = viz.PCA_Transform( zip(*self.X) )
		else:
			X = self.X
		
		unique_labels = np.unique(self.Y)
		clusters = { ul:[] for ul in unique_labels }
		
		for i in range( len(X) ):
			clusters[ self.Y[i] ].append( X[i] )
		
		centers_for_plot = [] # Not the real centers because dimension was reduced using PCA
		for label in clusters:
			centers_for_plot.append( [np.mean(col) for col in zip(* clusters[label] ) ] )
		
		viz.do_plot( zip(*centers_for_plot), marker='o', color='m' )
		viz.plot_groups(clusters)
	
	#---------------------------------------
	
	