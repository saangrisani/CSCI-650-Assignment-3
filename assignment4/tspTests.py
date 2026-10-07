# CSCI 650
# Generate Tests of Different Types for the Traveling Salesman Problem
# Author: Carter Tillquist

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from tsp import nearestNeighbor, totalDistance, runSimulatedAnnealing, swapPairs, permuteRange, reverseRange

#Generate a distance matrix given a networkx graph
def genDistanceMatrix(G):
  D = dict(nx.all_pairs_shortest_path_length(G))
  nodes = sorted(D.keys())
  return [[D[u][v] for v in nodes] for u in nodes]

#Generate a Barabasi-Albert random graph with n nodes and m neighbors for newly added nodes and return the distance matrix
def baDistances(n, m=1):
  G = nx.barabasi_albert_graph(n, m)
  return genDistanceMatrix(G)

#Generate a Watts-Strogatz random graph with n nodes, k neighbors on the ring, and a rewire probability of p and return the distance matrix
def wattsStrogatzDistances(n, k=2, p=0.1):
  G = nx.watts_strogatz_graph(n, k, p)
  return genDistanceMatrix(G)

#Generate a distance matrix for points place uniformly at random in a d-dimensional unit square
def unitSquareDistances(n, d=2):
  points = np.random.uniform(0, 1, size=[n for _ in range(d)])
  return [[np.linalg.norm(a-b) for b in points] for a in points]

#Generate a distance matrix similar to the one described in Optimization by Simulated Annealing by Kirkpatrick et al. (see Figure 9)
#Note that Manhattan distance is used instead of Euclidean distance
def randomSquareRegionDistances(n):
  points = []
  for i in range(3):
    for j in range(3):
      points.extend(list(np.random.uniform(0, 1, size=(n//9, 2))+np.array([i*1.2, j*1.2])))
  D = [[sum(np.abs(a-b)) for b in points] for a in points]
  return D

#Generate distances uniformly at random, may not be symmetric
def randomDistances(n, low=1, high=100):
  D = np.random.uniform(0, 1, size=(n,n))
  for i in range(len(D)): D[i][i] = 0
  return D

#Generate distances from a normal distribution, may not be symmetric
def randomNormalDistances(n, mu=5, sigma=2):
  D = np.absolute(np.random.normal(mu, sigma, size=(n,n)))
  for i in range(len(D)): D[i][i] = 0
  return D

#main
if __name__=='__main__':
  testTypes = {'Barabasi-Albert': lambda n: baDistances(n, m=4),
               'Watts-Strogatz': lambda n: wattsStrogatzDistances(n, k=4, p=0.1),
               'Unit Square': lambda n: unitSquareDistances(n),
               'Square Regions': lambda n: randomSquareRegionDistances(3*n),
               'Uniform Random': lambda n: randomDistances(n, low=1, high=20),
               'Normal Random': lambda n: randomNormalDistances(n)}

  #run tests using the nearest neighbor heuristic
  #this may take several seconds
  if True:
    n = 100
    repeats = 50

    data = {key:[] for key in testTypes}
    for func in ['Barabasi-Albert', 'Watts-Strogatz', 'Uniform Random']:
      for rep in range(repeats):
        D = testTypes[func](n)
        dists = [totalDistance(D, nearestNeighbor(D, start)) for start in range(len(D))]
        m = min(dists)
        ratios = [d/m for d in dists]
        data[func].extend(ratios)
      bins = 25
      plt.hist(data[func], bins=bins, alpha=0.5, density=True)
      plt.title(func+' Distances')
      plt.ylabel('Fraction of Observations')
      plt.xlabel('Ratios with Respect to Minimum')
      plt.show()

  #run tests using simulated annealing
  if True:
    n = 100
    candidateMap = {0:'Swap Pairs', 1:'Permute Range', 2:'Reverse Range'}
    for func in ['Barabasi-Albert', 'Watts-Strogatz', 'Uniform Random']:
      D = testTypes[func](n)
      best = np.inf
      for i,candidateFunc in enumerate([swapPairs, permuteRange, reverseRange]):
        a,b,c = runSimulatedAnnealing(D, maxIterations=10000, T=-1, genCandidate=candidateFunc)
        best = min([best, b])
        plt.plot(c, label=candidateMap[i])
      plt.title(func)
      plt.xlabel('Iteration')
      plt.ylabel('Current Path Distance')
      plt.legend()
      plt.show()


