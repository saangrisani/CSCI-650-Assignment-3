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

  # YOUR CODE HERE
  pass

#Implement a greedy algorithm for finding small dominating sets on a graph G
#G - a pair including a list of nodes and a list of edges
#return - a dominating set (as a list, order matters) created via a greedy algorithm
def greedyDominatingSet(G):
  #you may, but are not required to, convert G to a networkx graph
  H = nx.Graph()
  H.add_edges_from(G[1])
  H.add_nodes_from(G[0])

  # YOUR CODE HERE
  pass

#########################
### GENETIC ALGORITHM ###
#########################
#Generate a single random individual
#What should individuals in the population look like?
def randomIndividual(G):
  # YOUR CODE HERE
  pass

#Given two individuals from the population, use a standard technique to recombine them and produce new individual(s) for the next generation
def recombine(a, b):
  # YOUR CODE HERE
  pass

#Select two individuals from the population for recombination
#Use roulette wheel selection
def selection(pop, fitnesses):
  # YOUR CODE HERE
  pass

#Mutate a given individual
#It might make sense to include a probability here indicating how likely a single piece of an individual is to mutate
def mutate(ind, p=0.1):
  # YOUR CODE HERE
  pass

#How should we calculate the fitness of an individual?
def evalFitness(ind, G):
  # YOUR CODE HERE
  pass

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

  pop = [randomIndividual(H) for _ in range(popSize)]
  fitnessList = [] #each element is (min, avg, max) fitness for a generation

  for gen in range(generations):
    print('Generation', gen)
    fitnesses = [evalFitness(ind, H) for ind in pop]
    fitnessList.append((min(fitnesses), np.mean(fitnesses), max(fitnesses)))
    newPop = []
    # YOUR CODE HERE

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

