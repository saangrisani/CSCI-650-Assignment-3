from collections import Counter
from itertools import product


def countSteps(delta, max_steps=100):
    tape = {}
    state = 'A'
    head = 0
    for steps in range(max_steps):
        if state == 'H':
            return steps
        state, symbol, direction = delta[(state, tape.get(head, '0'))]
        tape[head] = symbol
        head += 1 if direction == 'R' else -1
    if state == 'H':
        return max_steps
    return None


def busyBeaverCounts(max_steps=100):
    keys = list(product('AB', '01'))
    choices = list(product('ABH', '01', 'LR'))
    counts = Counter()
    for transitions in product(choices, repeat=4):
        delta = dict(zip(keys, transitions))
        steps = countSteps(delta, max_steps)
        bucket = max_steps if steps is None else steps
        counts[bucket] += 1
    return counts


if __name__ == '__main__':
    counts = busyBeaverCounts()
    total = sum(counts.values())
    print('Steps Number Fraction')
    for steps in range(7):
        print(steps, counts[steps], f'{counts[steps] / total:.6f}')
    print('7-99', sum(counts[i] for i in range(7, 100)))
    print('>=100', counts[100], f'{counts[100] / total:.6f}')
    print('Total', total)
