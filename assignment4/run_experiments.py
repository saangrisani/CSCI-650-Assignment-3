import os, sys, random, json, runpy
from pathlib import Path
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
os.environ["MPLBACKEND"] = "Agg"
os.environ["MPLCONFIGDIR"] = str(OUT / ".mplconfig")
import numpy as np
import matplotlib.pyplot as plt
from tsp import *
import tspTests

np.random.seed(65004)
random.seed(65004)
D = [[0, 2, 9], [7, 0, 3], [4, 8, 0]]
assert totalDistance(D, [0, 1, 2]) == 9
assert totalDistance(D, [0, 2, 1]) == 24
assert totalDistance([], []) == 0
assert totalDistance([[0]], [0]) == 0
assert nearestNeighbor(D, 0) == [0, 1, 2]
assert nearestNeighbor([], 0) == []
assert nearestNeighbor([[0]]) == [0]
assert nearestNeighbor([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0) == [0, 1, 2]
checks = 8
for n in (0, 1, 2, 7):
    original = list(range(n))
    for gen in (swapPairs, lambda p: swapPairs(p, 5), lambda p: swapPairs(p, adj=True),
                permuteRange, reverseRange):
        for _ in range(20):
            result = gen(original)
            assert original == list(range(n))
            assert sorted(result) == original and result is not original
            checks += 1
for _ in range(20):
    p = list(range(7))
    q = swapPairs(p, adj=True)
    changed = [j for j in range(7) if p[j] != q[j]]
    assert len(changed) == 2 and changed[1] == changed[0] + 1
    checks += 1
for gen in (swapPairs, permuteRange, reverseRange):
    best, dist, history = runSimulatedAnnealing(D, gen, 250, T=0)
    assert sorted(best) == [0, 1, 2]
    assert dist == totalDistance(D, best)
    assert len(history) == 250
    assert all(b <= a for a, b in zip(history, history[1:]))
    assert dist == min(history)
    checks += 1
best, dist, history = runSimulatedAnnealing(D, maxIterations=0)
assert history == [] and dist == totalDistance(D, best)
checks += 1
best, dist, history = runSimulatedAnnealing([], maxIterations=3)
assert best == [] and dist == 0 and history == [0, 0, 0]
checks += 1
# Deterministic test: high temperature accepts an uphill proposal, but best stays.
np.random.seed(1)
initial = np.random.permutation(3).tolist()
np.random.seed(1)
initial_dist = totalDistance(D, initial)
worse = max(([0, 1, 2], [0, 2, 1]), key=lambda p: totalDistance(D, p))
b, d, h = runSimulatedAnnealing(D, lambda p: worse[:], 1, T=1e100)
assert h[0] == totalDistance(D, worse) and d == initial_dist
checks += 1
print(f"Passed {checks} correctness/property checks.", flush=True)
# Run the supplied script unchanged; intercept plot display to save each figure.
np.random.seed(65004)
random.seed(65004)
names = ["nn_ba", "nn_ws", "nn_uniform", "sa_ba", "sa_ws", "sa_uniform"]
summaries = {}
count = 0
def save_show():
    global count
    name = names[count]
    plt.gcf().set_size_inches(7.2, 4.2)
    plt.tight_layout()
    plt.savefig(OUT / (name + ".png"), dpi=170)
    plt.savefig(OUT / (name + ".pdf"))
    plt.close()
    count += 1
plt.show = save_show
state = runpy.run_path(str(OUT / "tspTests.py"), run_name="__main__")
for label, values in state["data"].items():
    if values:
        v = np.array(values)
        summaries[label] = {"count": len(v), "mean": float(v.mean()),
                           "median": float(np.median(v)), "p95": float(np.percentile(v, 95)),
                           "max": float(v.max())}
# Capture complete histories from a separate reproducible replay of same experiment.
np.random.seed(65004)
random.seed(65004)
annealing = {}
for func in ["Barabasi-Albert", "Watts-Strogatz", "Uniform Random"]:
    # Reproduce RNG consumed by the script's nearest-neighbor phase.
    for rep in range(50):
        state["testTypes"][func](100)
for func in ["Barabasi-Albert", "Watts-Strogatz", "Uniform Random"]:
    matrix = state["testTypes"][func](100)
    results = {}
    for gen in (swapPairs, permuteRange, reverseRange):
        # Peek at the initial permutation without advancing the generator.
        rng_state = np.random.get_state()
        start = np.random.permutation(len(matrix)).tolist()
        np.random.set_state(rng_state)
        best, distance, hist = runSimulatedAnnealing(matrix, gen, 10000)
        results[gen.__name__] = {"initial": totalDistance(matrix, start), "best": distance,
                              "final": hist[-1], "uphill_steps": sum(b > a for a,b in zip(hist,hist[1:])),
                              "last_change": max([0]+[j+1 for j in range(1,len(hist)) if hist[j]!=hist[j-1]]),
                              "history": hist}
    annealing[func] = results
report = {"seed": 65004, "checks": checks, "nearest_neighbor": summaries,
          "annealing": annealing, "versions": {"numpy": np.__version__,
          "networkx": tspTests.nx.__version__, "matplotlib": plt.matplotlib.__version__}}
(OUT / "experiment_results.json").write_text(json.dumps(report, indent=2))
print(json.dumps({"nearest_neighbor": summaries, "annealing":
    {k:{g:{a:b for a,b in v.items() if a!="history"} for g,v in r.items()} for k,r in annealing.items()},
    "versions": report["versions"]}, indent=2), flush=True)



