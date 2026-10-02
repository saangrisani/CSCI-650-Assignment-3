import sys


def simulateTM(delta, A, w):
  tape = dict(enumerate(w))
  state = 'A'
  head = 0
  while state not in A:
    symbol = tape.get(head, 'b')
    if (state, symbol) not in delta:
      break
    state, symbol, direction = delta[(state, symbol)]
    tape[head] = symbol
    head += 1 if direction == 'R' else -1
  result = ''
  if tape:
    result = ''.join(tape.get(i, 'b')
                     for i in range(min(tape), max(tape) + 1))
    result = result.strip('b')
  if state in A:
    return True, result
  if result:
    return False, result
  return False, ''


def main(M):
  lines = M.split('\n')
  if not lines[int(lines[0]) + 2].strip():
    lines[int(lines[0]) + 2] = 'b'
    M = '\n'.join(lines)
  M = M.strip().split('\n')
  w = M[-1].strip()
  A = M[-2].strip().split(' ')
  delta = {}
  for line in M[1:-2]:
    line = line.strip().split(' ')
    delta[(line[0], line[1])] = line[2:]
  accepted, config = simulateTM(delta, A, w)
  return config+'\n'+str(accepted)


if __name__ == '__main__':
    print(main(sys.stdin.read()))
