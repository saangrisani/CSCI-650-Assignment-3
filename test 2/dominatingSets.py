# CSCI 650
# Dominating Sets
# Author: Carter Tillquist

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Given a graph G, a set of nodes D, and an integer k, determine whether or not D is
#a dominating set of size at most k on G
#G - a pair including a list of nodes and a list of edges
#D - a set of nodes in G
#k - an integer
#return - True if D is a dominating set of size at most k and False otherwise
def checkDominatingSet(G, D, k):
  #you may, but are not required to, convert G to a networkx graph
  H = nx.Graph()
  H.add_edges_from(G[1])
  H.add_nodes_from(G[0])

  chosen = set(D)
  if len(chosen) > k or not chosen <= set(H.nodes()):
    return False
  covered = set(chosen)
  for u in chosen:
    covered.update(H.neighbors(u))
  return len(covered) == len(H)

#Implement a greedy algorithm for finding small dominating sets on a graph G
#G - a pair including a list of nodes and a list of edges
#return - a dominating set (as a list, order matters) created via a greedy algorithm
def greedyDominatingSet(G):
  #you may, but are not required to, convert G to a networkx graph
  H = nx.Graph()
  H.add_edges_from(G[1])
  H.add_nodes_from(G[0])

  uncovered = set(H.nodes())
  closed = {v: set(H.neighbors(v)) | {v} for v in H}
  result = []
  while uncovered:
    # max keeps the first vertex in insertion order on a tie.
    v = max(H.nodes(), key=lambda u: len(closed[u] & uncovered))
    result.append(v)
    uncovered.difference_update(closed[v])
  return result

#########################
### GENETIC ALGORITHM ###
#########################
#Generate a single random individual
#What should individuals in the population look like?
def randomIndividual(G):
  # Position i represents the ith vertex in G.nodes() order.
  n = len(G.nodes()) if isinstance(G, nx.Graph) else len(G[0])
  return np.random.randint(0, 2, size=n).tolist()

#Given two individuals from the population, use a standard technique to recombine them and produce new individual(s) for the next generation
def recombine(a, b):
  if len(a) != len(b):
    raise ValueError("Parents must have equal lengths")
  if len(a) < 2:
    return list(a), list(b)
  cut = np.random.randint(1, len(a))
  return list(a[:cut]) + list(b[cut:]), list(b[:cut]) + list(a[cut:])

#Select two individuals from the population for recombination
#Use roulette wheel selection
def selection(pop, fitnesses):
  weights = np.asarray(fitnesses, dtype=float)
  if len(pop) == 0 or len(weights) != len(pop):
    raise ValueError("Population and fitnesses must be nonempty and aligned")
  if not np.all(np.isfinite(weights)) or np.any(weights < 0):
    raise ValueError("Fitness weights must be finite and nonnegative")
  total = weights.sum()
  probabilities = weights / total if total > 0 else None
  i, j = np.random.choice(len(pop), size=2, replace=True, p=probabilities)
  return list(pop[i]), list(pop[j])

#Mutate a given individual
#It might make sense to include a probability here indicating how likely a single piece of an individual is to mutate
def mutate(ind, p=0.1):
  if not 0 <= p <= 1:
    raise ValueError("Mutation probability must be between 0 and 1")
  for i in range(len(ind)):
    if np.random.random() < p:
      ind[i] = 1 - ind[i]
  return ind

#How should we calculate the fitness of an individual?
def evalFitness(ind, G):
  H = G if isinstance(G, nx.Graph) else nx.Graph()
  if not isinstance(G, nx.Graph):
    H.add_nodes_from(G[0])
    H.add_edges_from(G[1])
  nodes = list(H.nodes())
  if len(ind) != len(nodes) or any(bit not in (0, 1) for bit in ind):
    raise ValueError("Individual must have one binary gene per vertex")
  chosen = {v for v, bit in zip(nodes, ind) if bit}
  covered = set(chosen)
  for v in chosen:
    covered.update(H.neighbors(v))
  missing = len(nodes) - len(covered)
  return 1.0 / (1 + len(chosen) + (len(nodes) + 1) * missing)

#Run a genetic algorithm to find a small dominating set of G
#G - the graph of interest, this is a pair including a list of nodes and a list of edges
#popSize - the number of individuals to include in the population
#generations - the number of generations to consider before stopping
#return - the best solution in the final generation, its fitness, and a list of the minimum, average, and maximum fitness values for each generation
def runGA(G, popSize=10, generations=100):
  #you may, but are not required to, convert G to a networkx graph
  H = nx.Graph()
  H.add_edges_from(G[1])
  H.add_nodes_from(G[0])

  if popSize < 1 or generations < 0:
    raise ValueError("Population must be positive and generations nonnegative")
  pop = [randomIndividual(H) for _ in range(popSize)]
  fitnessList = [] #each element is (min, avg, max) fitness for a generation

  for gen in range(generations):
    print('Generation', gen)
    fitnesses = [evalFitness(ind, H) for ind in pop]
    fitnessList.append((min(fitnesses), np.mean(fitnesses), max(fitnesses)))
    newPop = []
    # Preserve the best individual and create the remaining population.
    elite = max(range(len(pop)), key=lambda i: fitnesses[i])
    newPop.append(list(pop[elite]))
    while len(newPop) < popSize:
      a, b = selection(pop, fitnesses)
      for child in recombine(a, b):
        mutate(child, p=1.0 / max(1, len(H)))
        newPop.append(child)
        if len(newPop) == popSize:
          break
    pop = newPop

  bestSol, bestFitness = max([(ind, evalFitness(ind, H)) for ind in pop], key=lambda x: x[1])
  return bestSol, bestFitness, fitnessList

#A simple main to run a genetic algorithm on a path
if __name__=='__main__':
  G = nx.path_graph(100)
  G = (list(G.nodes()), list(G.edges()))

  bestSol, bestFitness, fitnessList = runGA(G, popSize=50, generations=1000)
  minList, avgList, maxList = zip(*fitnessList)
  plt.plot(range(len(fitnessList)), minList, label='Min')
  plt.plot(range(len(fitnessList)), avgList, label='Avg')
  plt.plot(range(len(fitnessList)), maxList, label='Max')
  plt.title(r'Fitness Over time on a Path, $n=100$')
  plt.xlabel('Generation')
  plt.ylabel('Fitness')
  plt.legend(loc='lower left')
  plt.show()

