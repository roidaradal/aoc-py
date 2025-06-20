# Advent of Code 2017 Day 07
# John Roy Daradal 

from aoc import *

class Tree:
    def __init__(self):
        self.nodes = []
        self.weight = {}
        self.parent = {}
        self.children = defaultdict(list)

def data(full: bool) -> Tree:
    t = Tree()
    for line in  readLines(17, 7, full):
        p = splitStr(line, '->')
        name, weight = splitStr(p[0], '(')
        t.nodes.append(name)
        t.weight[name] = int(weight.strip(')'))
        if len(p) == 1: continue
        for child in splitStr(p[1], ','):
            t.parent[child] = name
            t.children[name].append(child)
    return t

def solve() -> Solution:
    t = data(full=True)
    
    # Part 1
    root = [name for name in t.nodes if name not in t.parent][0]

    # Part 2
    weight = {}
    q = t.nodes
    targetWeight = 0
    while len(q) > 0:
        q2 = []
        stop = False
        for node in q:
            if node not in t.children:  # no children = leaf
                weight[node] = t.weight[node]   
            elif all(child in weight for child in t.children[node]): # all children have weights
                childWeights = set()
                totalChild = 0
                for child in t.children[node]:
                    w = weight[child]
                    childWeights.add(w)
                    totalChild += w 
                weight[node] = t.weight[node] + totalChild
                
                if len(childWeights) == 2: # one weight is not same as the rest
                    target, heavy = sorted(childWeights)
                    heavyChild = [child for child in t.children[node] if weight[child] == heavy][0]
                    targetWeight = t.weight[heavyChild] - (heavy-target)
                    stop = True 
                    break
            else: # has child without weight = defer
                q2.append(node)
        q = q2
        if stop: break
    
    return newSolution(root, targetWeight)

if __name__ == '__main__':
    do(solve, 17, 7)

'''
Solve:
- For part 1, find the root node by checking which node doesn't have a parent
- For part 2, find the node that has unbalanced weight
- For leaf nodes, node weight is simply its own weight
- For internal nodes, check if all children already have their weights computed
- If not complete, defer to q2 for next round
- If complete, can now compute node's weight = own weight + total weight of children
- Check the number of unique weights of children: if has 2 unique weights = found the imbalanced node
- Get the heavier weight and use that to find the heavier child
- Compute the target weight by subtracting the difference between heavy-target from the heavy child's weight
'''