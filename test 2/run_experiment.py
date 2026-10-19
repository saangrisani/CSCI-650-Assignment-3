"""Reproduce the required population-50, 1000-generation experiment."""
from pathlib import Path
import contextlib
import csv
import io
import json
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import dominatingSets as ds

def main():
    np.random.seed(650)
    H = nx.path_graph(100)
    G = (list(H), list(H.edges()))
    with contextlib.redirect_stdout(io.StringIO()):
        best, fitness, history = ds.runGA(G, popSize=50, generations=1000)
    root = Path(__file__).parent
    with (root/'fitness_history.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['generation', 'minimum', 'average', 'maximum'])
        w.writerows((i, *row) for i, row in enumerate(history))
    selected = [v for v, bit in zip(H, best) if bit]
    result = dict(seed=650, vertices=100, edges=99, population=50,
                  generations=1000, best_individual=best, selected_vertices=selected,
                  selected_count=len(selected), fitness=fitness,
                  dominating=ds.checkDominatingSet(G, selected, 100),
                  first_statistics=history[0], last_statistics=history[-1])
    (root/'experiment_results.json').write_text(json.dumps(result, indent=2))
    a = np.asarray(history)
    fig, ax = plt.subplots(figsize=(8, 4.1), constrained_layout=True)
    for col, label, color in [(2,'Maximum','#176b45'),(1,'Average','#205ca8'),(0,'Minimum','#b24a31')]:
        ax.plot(range(1000), a[:, col], label=label, color=color, linewidth=1.2)
    ax.set(title='Genetic algorithm on a 100-vertex path', xlabel='Generation (0-999)',
           ylabel='Fitness (higher is better)')
    ax.grid(alpha=.2)
    ax.legend()
    fig.savefig(root/'fitness.png', dpi=180)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
