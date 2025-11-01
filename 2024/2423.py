# Advent of Code 2024 Day 23
# John Roy Daradal 

from aoc import *

Clique = tuple[str,...]

def data(full: bool) -> dict[str, set[str]]:
    neighbors: dict[str, set[str]] = defaultdict(set)
    for line in readLines(24, 23, full):
        e1, e2 = splitStr(line, '-')
        neighbors[e1].add(e2)
        neighbors[e2].add(e1)
    return neighbors

def solve() -> Solution:
    neighbors = data(full=True)
    cliques: dict[int, set[Clique]] = defaultdict(set)

    # Create clique-2
    for v1 in neighbors:
        for v2 in neighbors[v1]:
            cliques[2].add(newClique(v1, v2)) 

    # Find maximum clique
    size = 3
    while True:
        cliques[size] = createCliques(cliques[size-1], neighbors)
        if len(cliques[size]) == 1:
            break 
        else:
            size += 1

    # Part 1 
    count = 0
    for clique in cliques[3]:
        if any(node.startswith('t') for node in clique):
            count += 1

    # Part 2
    clique = tuple(cliques[size])[0]
    password = ','.join(clique)

    return newSolution(count, password)

def newClique(*nodes: str) -> Clique:
    return tuple(sorted(nodes))

def createCliques(smallCliques: set[Clique], neighbors: dict[str, set[str]]) -> set[Clique]:
    cliques: set[Clique] = set()
    for oldClique in smallCliques:
        candidates: set[str] = set()
        for node in oldClique:
            candidates = candidates.union(neighbors[node])
        candidates = candidates - set(oldClique)
        for node2 in candidates:
            if all(node2 in neighbors[node] for node in oldClique):
                cliques.add(newClique(node2, *oldClique))
    return cliques

if __name__ == '__main__':
    do(solve, 24, 23)

'''
Solve:
- Create the undirected adjacency list from the given pairs of computers
- Create cliques of size 2: these are just the graph edges (n1,n2 are connected to each other)
- When we create the cliques of size N, we use the cliques of size N-1 and build on it:
    - The canonical form of a clique is the sorted tuple of the computer names
    - From the cliques of size N-1, we can add 1 node that is also connected to all other nodes 
      to make a clique of size N
    - The candidate nodes to be added are all the neighbors of the nodes currently in the clique, 
      which are not already in the clique
    - For each candidate node, if this node is also connected to all the other nodes in the smaller clique,
      then we can form a clique of size N by adding it to the smaller clique
- Starting from size 3, create cliques of bigger sizes until we find a clique size that has only 1 clique
- For Part 1, count the number of size-3 cliques where at least one computer starts with 't'
- For Part 2, form the password by sorting the computer names in the biggest clique and joining by comma
'''