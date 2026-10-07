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
  if not path:
    return 0.0
  return float(sum(D[path[j]][path[(j + 1) % len(path)]]
          for j in range(len(path))))


#Generate a path for a traveling salesman to follow using the nearest neighbor heuristic
#D - a distance matrix
#start - the starting location, if set to -1 (the default), select a random start
#return - a sequence of nodes to visit, the length should equal the number of rows in D
def nearestNeighbor(D, start=-1):
  n = len(D)
  if n == 0:
    return []
  if start == -1:
    start = int(np.random.randint(n))
  path = [start]
  remaining = set(range(n))
  remaining.remove(start)
  while remaining:
    city = min(remaining, key=lambda v: (D[path[-1]][v], v))
    path.append(city)
    remaining.remove(city)
  return path


#Swap pairs of elements in the given path to produce a new candidate solution
#path - a path to modify to produce a new candidate solution
#numSwaps - the number of pairs of elements to swap
#adj - if true, only swap adjacent values
#return - a new path
def swapPairs(path, numSwaps=1, adj=False):
  candidate = path[:] #we do not want to change the given path
  n = len(candidate)
  if n < 2:
    return candidate
  for _ in range(numSwaps):
    if adj:
      a = int(np.random.randint(n - 1))
      b = a + 1
    else:
      a, b = np.random.choice(n, size=2, replace=False)
    candidate[a], candidate[b] = candidate[b], candidate[a]
  return candidate


#Modify the given path by randomly permuting a randomly selected slice
#path - the path to modify to produce a new candidate
#return - a new path
def permuteRange(path):
  candidate = path[:] #we do not want to change the given path
  if len(candidate) < 2:
    return candidate
  a, b = sorted(np.random.choice(len(candidate), size=2, replace=False))
  candidate[a:b + 1] = np.random.permutation(candidate[a:b + 1]).tolist()
  return candidate


#Modify the given path by reversing a randomly selected slice
#path - the path to modify to produce a new candidate
#return - a new path
def reverseRange(path):
  candidate = path[:] #we do not want to change the given path
  if len(candidate) < 2:
    return candidate
  a, b = sorted(np.random.choice(len(candidate), size=2, replace=False))
  candidate[a:b + 1] = candidate[a:b + 1][::-1]
  return candidate


#Use simulated annealing to find a solution to the traveling salesman problem
#D - a distance matrix
#gencandidate - a function taking a path as input and producing a new candidate path
#maxIterations - the maximum number of iterations to perform
#alpha - a multiplicative update factor for the temperature
#return - the best path discovered, the total distance associated with the best path, and a list of distances for the current path on each iteration
def runSimulatedAnnealing(D, genCandidate=swapPairs, maxIterations=1000, T=-1, alpha=0.9):
  if T==-1: T = np.sqrt(len(D)) #default starting temperature
  T = float(T)
  curPath = np.random.permutation(len(D)).tolist() #a random initial path
  curDist = totalDistance(D, curPath)
  bestPath, bestDist = curPath[:], curDist
  distList = []
  for _ in range(maxIterations):
    candidate = genCandidate(curPath[:])
    candidateDist = totalDistance(D, candidate)
    delta = candidateDist - curDist
    if delta <= 0 or (T > 0 and np.random.random() < np.exp(-delta / T)):
      curPath, curDist = list(candidate), candidateDist
      if curDist < bestDist:
        bestPath, bestDist = curPath[:], curDist
    distList.append(curDist)
    T *= alpha
  return bestPath, bestDist, distList

