# CSCI 650
# An Implementation of a Simple Turing Machine Skeleton
# Author: Carter Tillquist

from collections import Counter
from itertools import product

#Given a transition function delta and a set of accepting states A, determine whether or not w is recognized by the associated Turing machine.
#Recall that we are making several assumptions here including that state A is the start state.
#delta - {(state, symbol): (state, symbol, direction)} - a dictionary mapping (state, symbol) pairs to triples indicating the new state to
#        transition to, the symbol to write to the tape, and the direction to move the tape head ('L' or 'R')
#A - [state] - a list (or set) of accepting states
#w - string - the input string to provide to the Turing machine
#Return True if w is recognized and False otherwise in addition to the final tape for the Turing machine.
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

##########################
### MAIN FOR INGINIOUS ###
##########################
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

if __name__=='__main__':
  n = input("Enter the number of transitions: ")
  M = n+'\n'
  print("Enter one transition per line with the initial state, symbol being read on the tape, destination state, symbol written to the tape, and tape head direction (L or R) separated by spaces:")
  delta = {}
  for _ in range(int(n)):
    M += input()+'\n'
  M += input("Enter accepting states separated by spaces: ")+'\n'
  M += input("Enter a string to check: ")
  result = main(M)
  print(result)


