# CSCI 650
# Simulated Annealing and Nearest Neighbor Heuristics for the Traveling Salesman Problem
# Author: Carter Tillquist

import numpy as np

#Determine the total distance traveled by a salesman using the given path
#Remember that the salesman must end at the start location
#D - a distance matrix
#path - a list of indices in D representing a route
#return - the total distance traveled
def totalDistance(D, path):
  pass

#Generate a path for a traveling salesman to follow using the nearest neighbor heuristic
#D - a distance matrix
#start - the starting location, if set to -1 (the default), select a random start
#return - a sequence of nodes to visit, the length should equal the number of rows in D
def nearestNeighbor(D, start=-1):
  pass

#Swap pairs of elements in the given path to produce a new candidate solution
#path - a path to modify to produce a new candidate solution
#numSwaps - the number of pairs of elements to swap
#adj - if true, only swap adjacent values
#return - a new path
def swapPairs(path, numSwaps=1, adj=False):
  candidate = path[:] #we do not want to change the given path
  pass

#Modify the given path by randomly permuting a randomly selected slice
#path - the path to modify to produce a new candidate
#return - a new path
def permuteRange(path):
  candidate = path[:] #we do not want to change the given path
  pass

#Modify the given path by reversing a randomly selected slice
#path - the path to modify to produce a new candidate
#return - a new path
def reverseRange(path):
  candidate = path[:] #we do not want to change the given path
  pass

#Use simulated annealing to find a solution to the traveling salesman problem
#D - a distance matrix
#gencandidate - a function taking a path as input and producing a new candidate path
#maxIterations - the maximum number of iterations to perform
#alpha - a multiplicative update factor for the temperature
#return - the best path discovered, the total distance associated with the best path, and a list of distances for the current path on each iteration
def runSimulatedAnnealing(D, genCandidate=swapPairs, maxIterations=1000, T=-1, alpha=0.9):
  if T==-1: T = np.sqrt(len(D)) #default starting temperature
  curPath = np.random.permutation(len(D)).tolist() #a random initial path
  pass
  return bestPath, bestDist, distList

