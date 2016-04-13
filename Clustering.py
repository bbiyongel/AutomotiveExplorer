import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from Visualize import Visualize
from scipy.spatial import distance
import matplotlib.pyplot as plt

class Clustering:
	def __init__(self, X, scale=False):
		self.random_seed = 12345 # set to None for random
		self.h = None
		self.Y = None
		self.scaler = None
		
		if scale:
			self.scaler = MinMaxScaler() # StandardScaler() can also be used instead of MinMaxScaler()
			self.X = self.scaler.fit_transform(X)
		else:
			self.X = X
    
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
		
		x_scaled = x if self.scaler is None else self.scaler.transform(x)
		return self.h.predict(x_scaled)[0]
	
	#---------------------------------------
	def predictAll(self, X):
		if not self.done(): return
		
		X_scaled = X if self.scaler is None else self.scaler.transform(X)
		return self.h.predict(X_scaled)
	
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
	
	