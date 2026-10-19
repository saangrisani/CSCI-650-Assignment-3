"""Independent correctness checks, including exhaustive small graphs."""
import contextlib
import io
import itertools
import json
from pathlib import Path
import networkx as nx
import numpy as np
import dominatingSets as ds

def reference(H, D, k):
    D = set(D)
    return len(D) <= k and D <= set(H) and all(v in D or any(u in D for u in H[v]) for v in H)

def main():
    checked = 0
    counterexample = None
    for H in nx.graph_atlas_g():
        if len(H) > 6:
            continue
        G = (list(H), list(H.edges()))
        for bits in itertools.product((0, 1), repeat=len(H)):
            D = {v for v, bit in zip(H, bits) if bit}
            for k in (len(D)-1, len(D), len(H)):
                assert ds.checkDominatingSet(G, D, k) == reference(H, D, k)
                checked += 1
        greedy = ds.greedyDominatingSet(G)
        uncovered = set(H)
        for v in greedy:
            scores = {u: len((set(H[u]) | {u}) & uncovered) for u in H}
            assert scores[v] == max(scores.values())
            uncovered -= set(H[v]) | {v}
        assert not uncovered
        assert len(greedy) == len(set(greedy))
        if counterexample is None and any(reference(H, set(greedy)-{v}, len(H)) for v in greedy):
            optimum = next(list(D) for size in range(len(H)+1)
                           for D in itertools.combinations(H, size) if reference(H, D, size))
            counterexample = dict(nodes=list(H), edges=list(H.edges()), greedy=greedy, optimum=optimum)
    assert not ds.checkDominatingSet(([1], []), {2}, 1)
    assert ds.greedyDominatingSet((['a','b'], [])) == ['a','b']
    np.random.seed(650)
    for H in (nx.Graph(), nx.path_graph(1), nx.empty_graph(5), nx.path_graph(15)):
        G = (list(H), list(H.edges()))
        with contextlib.redirect_stdout(io.StringIO()):
            best, fit, hist = ds.runGA(G, popSize=7, generations=20)
        assert len(best) == len(H) and fit == ds.evalFitness(best, H)
        assert len(hist) == 20 and all(lo <= avg <= hi for lo, avg, hi in hist)
        assert all(hist[i][2] <= hist[i+1][2] for i in range(19))
    a,b = [0,1,0],[1,0,1]
    old_a,old_b = list(a),list(b)
    ds.recombine(a,b)
    assert a == old_a and b == old_b
    assert ds.mutate(list(a), p=1) == [1,0,1]
    assert ds.mutate(list(a), p=0) == a
    result = dict(verifier_comparisons=checked, graph_atlas_max_vertices=6,
                  additional_GA_and_operator_checks='passed', counterexample=counterexample)
    Path(__file__).with_name('verification_results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
