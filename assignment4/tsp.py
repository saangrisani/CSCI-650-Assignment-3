# CSCI 650
# Simulated Annealing and Nearest Neighbor Heuristics for the Traveling Salesman Problem
# Starter interface by Carter Tillquist; implementation completed with AI assistance.

import numpy as np


def totalDistance(D, path):
    """Return the closed-tour distance, including the last-to-first edge."""
    if not path:
        return 0.0
    return float(sum(D[path[j]][path[(j + 1) % len(path)]]
                     for j in range(len(path))))


def nearestNeighbor(D, start=-1):
    """Visit each city once, greedily choosing the closest unvisited city."""
    n = len(D)
    if n == 0:
        return []
    if start == -1:
        start = int(np.random.randint(n))
    if not 0 <= start < n:
        raise ValueError("start must identify a city")
    path = [start]
    remaining = set(range(n))
    remaining.remove(start)
    while remaining:
        city = min(remaining, key=lambda v: (D[path[-1]][v], v))
        path.append(city)
        remaining.remove(city)
    return path


def swapPairs(path, numSwaps=1, adj=False):
    """Return a copy with random swaps; adjacent means consecutive indices."""
    candidate = list(path)
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


def permuteRange(path):
    """Shuffle an inclusive slice between two distinct random indices."""
    candidate = list(path)
    if len(candidate) < 2:
        return candidate
    a, b = sorted(np.random.choice(len(candidate), size=2, replace=False))
    candidate[a:b + 1] = np.random.permutation(candidate[a:b + 1]).tolist()
    return candidate


def reverseRange(path):
    """Reverse an inclusive slice between two distinct random indices."""
    candidate = list(path)
    if len(candidate) < 2:
        return candidate
    a, b = sorted(np.random.choice(len(candidate), size=2, replace=False))
    candidate[a:b + 1] = candidate[a:b + 1][::-1]
    return candidate


def runSimulatedAnnealing(D, genCandidate=swapPairs,
                         maxIterations=1000, T=-1, alpha=0.9):
    """Return best tour, its distance, and current distance after each step."""
    if T == -1:
        T = float(np.sqrt(len(D)))
    T = float(T)
    if T < 0 or not np.isfinite(T):
        raise ValueError("T must be finite and nonnegative, or -1")
    if not 0 < alpha <= 1:
        raise ValueError("alpha must lie in (0, 1]")
    if maxIterations < 0:
        raise ValueError("maxIterations must be nonnegative")
    curPath = np.random.permutation(len(D)).tolist()
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
