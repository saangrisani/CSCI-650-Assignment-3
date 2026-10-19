# CSCI 650
# The CYK Algorithm Skeleton
# Author: Carter Tillquist
from itertools import product
#Run the CYK algorithm to determine whether or not w is in the language associated with the grammar G
#Return True if it is and False otherwise. In addition, return the table filled in during the course of the CYK algorithm.
#G - (V, T, S, P) - V - a set of variables (strings)
# T - a set of terminals (strings)
# S - the start symbol (string)
# P - a dictionary {string: {strings}} where keys are variables (production heads) and values are sets of strings
# (production bodies). This is assumed to be in CNF
#w - string- check whether or not w is in the language associated with G
#return - boolean, 2d matrix - true if w is in the language and false otherwise, a list of lists of sets of strings following the table
# format covered in class
def cyk(G, w):
    M = [[set() for _ in range(len(w)-i)] for i in range(len(w))]
    V, T, P, S = G
    if not w:
        return '' in P.get(S, set()), M
    for i, symbol in enumerate(w):
        for head, bodies in P.items():
            if symbol in bodies:
                M[0][i].add(head)
    for length in range(2, len(w) + 1):
        for start in range(len(w) - length + 1):
            for left_length in range(1, length):
                left = M[left_length - 1][start]
                right = M[length - left_length - 1][start + left_length]
                for head, bodies in P.items():
                    for body in bodies:
                        if (len(body) == 2
                                and body[0] in left and body[1] in right):
                            M[length - 1][start].add(head)
    if S in M[-1][0]:
        return True, M
    return False, M
##########################
### MAIN FOR INGINIOUS ###
##########################
def main(V, T, P, S, w):
    isElem, M = cyk((V, T, P, S), w)
    mat = ''
    for row in M: mat += ' | '.join(map(str, row))+'\n'
    return mat+str(isElem)
if __name__=='__main__':
    n = int(input("Enter a number of lines to read: "))
    V, T, P, S = set(), set(), {}, ''
    for i in range(n):
        line = input().strip()
        V |= set([c for c in line if c.isupper()])
        T |= set([c for c in line if not c.isupper() and c not in '->| '])
        line = line.split('->')
        head = line[0].strip()
        bodies = set([b.strip() for b in line[1].split('|')])
        if i == 0: S = head
        P[head] = P.get(head, set()) | bodies
    w = input("Enter a string to test: ")
    result = main(V, T, P, S, w)
    print(result)
