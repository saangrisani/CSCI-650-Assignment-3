# CSCI 650
# Generate Random Tests for Dominating Sets
# Author: Carter Tillquist

import numpy as np
import networkx as nx
import dominatingSets as ds

#Tests for this problem on INGInious are generated randomly following an approach similar, though not identical,
#to what is included here. Feel free to modify this code to help with testing on your local machine.

if __name__=='__main__':
  n = np.random.randint(5, 20)
  i = np.random.randint(1, n//2) if np.random.uniform(0,1) < 0.2 else 0

  G = nx.Graph()
  opt = np.random.randint(5)
  
  if opt==0: G = nx.random_unlabeled_tree(n)
  elif opt==1: G = nx.barabasi_albert_graph(n, np.random.randint(2, min(n, 5)))
  elif opt==2: G = nx.path_graph(n)
  elif opt==3: G = nx.complete_graph(n)
  elif opt==4: G = nx.watts_strogatz_graph(n, np.random.randint(2, 4), p=0.1)
  if i>0: G.add_nodes_from(range(max(G.nodes()), max(G.nodes())+i))

  D = nx.dominating_set(G)
  k = 0
  if np.random.uniform(0, 1) < 0.5: #check a dominating set
    k = np.random.randint(len(D), len(G)+1)
  else:
    if len(D) > 2: D = np.random.choice(list(D), size=np.random.randint(1, len(D)-1), replace=False)
    k = np.random.randint(max(1, len(D)-3), len(D)+3)

  G = (list(G.nodes()), list(G.edges()))

  print('Nodes', G[0])
  print('Edges', G[1])

  print('Check dominating set')
  print('D', D)
  print('k', k)
  print('Result', ds.checkDominatingSet(G, D, k)) 

  print('Greedy dominating set')
  S = ds.greedyDominatingSet(G)
  print('Result', S, ds.checkDominatingSet(G, S, len(G[0])))

