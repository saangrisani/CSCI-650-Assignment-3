def cyk(G, w):
    V, T, P, S = G
    n = len(w)
    table = [[set() for _ in range(n)] for _ in range(n)]
    if n == 0:
        return '' in P.get(S, set()), table
    for i in range(n):
        for head, bodies in P.items():
            if w[i] in bodies:
                table[i][i].add(head)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for head, bodies in P.items():
                    for body in bodies:
                        if (len(body) == 2
                                and body[0] in table[i][k]
                                and body[1] in table[k + 1][j]):
                            table[i][j].add(head)
    return S in table[0][n - 1], table


def main(M):
    lines = M.splitlines()
    n = int(lines[0])
    P = {}
    S = None
    for line in lines[1:n + 1]:
        head, bodies = line.split('->')
        head = head.strip()
        if S is None:
            S = head
        P.setdefault(head, set()).update(
            body.strip() for body in bodies.split('|') if body.strip())
    V = set(P)
    T = {body for bodies in P.values()
         for body in bodies if len(body) == 1}
    w = lines[n + 1].strip() if len(lines) > n + 1 else ''
    accepted, table = cyk((V, T, P, S), w)
    output = [' '.join('{' + ','.join(sorted(cell)) + '}'
                       for cell in row) for row in table]
    output.append(str(accepted))
    return '\n'.join(output)


if __name__ == '__main__':
    n = int(input())
    P = {}
    S = None
    for _ in range(n):
        head, bodies = input().split('->')
        head = head.strip()
        if S is None:
            S = head
        P.setdefault(head, set()).update(
            body.strip() for body in bodies.split('|') if body.strip())
    V = set(P)
    T = {body for bodies in P.values()
         for body in bodies if len(body) == 1}
    accepted, table = cyk((V, T, P, S), input().strip())
    for row in table:
        print(' '.join('{' + ','.join(sorted(cell)) + '}' for cell in row))
    print(accepted)
