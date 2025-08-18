# Advent of Code 2022 Day 21
# John Roy Daradal 

from aoc import *

HUMAN = 'humn'
str4 = tuple[str,str|int,str|int,str]

def data(full: bool) -> tuple[dict[str,int], dict[str, str3]]:
    values: dict[str,int] = {}
    rules: dict[str,str3] = {}
    for line in readLines(22, 21, full):
        name, tail = splitStr(line, ':')
        p = splitStr(tail, None)
        if len(p) == 1:
            values[name] = int(p[0])
        else:
            p1, op, p2 = p[0], p[1], p[2]
            rules[name] = (op, p1, p2)
    return values, rules

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    values, rules = data(full=True)

    levels, _ = createSubTree('root', rules)
    rootValue = computeRootValue(values, rules, levels, 'root')        
    return rootValue

def part2() -> int:
    values, rules = data(full=True)
    del values[HUMAN]

    _, leftRoot, rightRoot  = rules['root']
    levels1, hasHuman1 = createSubTree(leftRoot, rules)
    levels2, hasHuman2 = createSubTree(rightRoot, rules)
    humanValue = 0

    if hasHuman1:
        goalValue = computeRootValue(values, rules, levels2, rightRoot)
        humanValue = computeHumanValue(values, rules, levels1, leftRoot, goalValue)
    elif hasHuman2:
        goalValue = computeRootValue(values, rules, levels1, leftRoot)
        humanValue = computeHumanValue(values, rules, levels2, rightRoot, goalValue)

    return humanValue

def createSubTree(root: str, rules: dict[str, str3]) -> tuple[dict[int, set[str]], bool]:
    levels: dict[int, set[str]] = defaultdict(set)
    q: list[strInt] = [(root, 0)]
    hasHuman = False
    while len(q) > 0:
        node, level = q.pop(0)
        levels[level].add(node)
        if node == HUMAN: hasHuman = True

        if node not in rules: continue
        p1 = rules[node][1]
        p2 = rules[node][2]
        q.append((p1, level+1))
        q.append((p2, level+1))
        
    return levels, hasHuman

def computeRootValue(values: dict[str,int], rules: dict[str, str3], levels: dict[int, set[str]], root: str) -> int:
    for level in sorted(levels, reverse=True):
        for node in levels[level]:
            if node in values: continue 
            addValue(values, rules[node], node)
    return values[root]

def addValue(values: dict[str, int], rule: str3, node: str):
    op, p1, p2 = rule 
    v1, v2 = values[p1], values[p2]
    values[node] = computeValue(op, v1, v2)

def computeValue(op: str, v1: int, v2: int) -> int:
    if op == '+':
        return v1 + v2 
    elif op == '-':
        return v1 - v2
    elif op == '*':
        return v1 * v2 
    elif op == '/':
        return v1 // v2
    else:
        return 0

def computeHumanValue(values: dict[str, int], rules: dict[str, str3], levels: dict[int, set[str]], root: str, rootValue: int) -> int:
    stack: list[str4] = []
    for level in sorted(levels, reverse=True):
        for node in levels[level]:
            if node in values or node == HUMAN: continue
            op, p1, p2 = rules[node]
            val1, val2 = p1 in values, p2 in values 
            if val1 and val2:
                addValue(values, rules[node], node)
            else:
                if op == '+':
                    if val2:    # p1 is variable
                        stack.append(('-', node, values[p2], p1))
                    elif val1:  # p2 is variable
                        stack.append(('-', node, values[p1], p2))
                elif op == '*':
                    if val2:    # p1 is variable
                        stack.append(('/', node, values[p2], p1))
                    elif val1:  # p2 is variable
                        stack.append(('/', node, values[p1], p2))
                elif op == '-':
                    if val2:    # p1 is variable 
                        stack.append(('+', node, values[p2], p1))
                    elif val1:  # p2 is variable 
                        stack.append(('-', values[p1], node, p2))
                elif op == '/':
                    if val2:    # p1 is variable 
                        stack.append(('*', node, values[p2], p1))
                    elif val1:  # p2 is variable 
                        stack.append(('/', values[p1], node, p2))
    
    values[root] = rootValue 
    while len(stack) > 0:
        op, p1, p2, node = stack.pop()
        v1, v2 = 0, 0
        if type(p1) == int: 
            v1 = p1 
        elif type(p1) == str and p1 in values:
            v1 = values[p1]
        if type(p2) == int:
            v2 = p2 
        elif type(p2) == str and p2 in values:
            v2 = values[p2]
        values[node] = computeValue(op, v1, v2)

    return values[HUMAN]

if __name__ == '__main__':
    do(solve, 22, 21)

'''
Part1:
- Create the subtree rooted at 'root':
    - Use BFS starting with the root node at level 0
    - Add node to set of nodes at the current level 
    - For rule-based nodes, add their param1 and param2 nodes in the queue, with level+1
- The returned subtree is a dictionary of levels and the nodes we need to compute at this level
- Using the levels above, compute the root value:
    - Start at the deepest level going up to 0 (need to take care of the children prerequisites, before the parent)
    - For each node in that level (except those that already have values), compute their value:
    - Update values[node] to the result of p1 op p2, where op can be +, -, * or /
- Output the root value

Part2:
- The operation at the root node is checking for equality
- Delete the initial value of 'humn' node, as we'll try to figure out the value for this node 
  that balances the left subtree and the right subtree, to pass the equality test at root
- Create the left subtree and the right subtree, using the createSubTree similar to Part 1
- Additionally, createSubTree returns a boolean flag to indicate whether that subtree has the 'humn' node
- If the human node is in the left subtree:
    - We can safely compute the root value of the right subtree, and this will be our goal value
    - Compute the human value for the left subtree, using the goal value of right subtree
- If the human node is in the right subtree:
    - We can safely compute the root value of the left subtree, and this will be our goal value
    - Compute the human value for the right subtree, using the goal value of left subtree
- To compute the human value for a subtree:
    - Start at the deepest level going up to 0 (take care of prerequisites, before parent)
    - Process each node at that level, except the human node and nodes which already have values
    - If the value of param1 and param2 are already set, then compute the values[node] similar to Part 1
    - Otherwise, we add the inverse equation to a stack (we are reversing the process):
        - node = p1 + v2    =>  p1 = node - v2 
        - node = v1 + p2    =>  p2 = node - v1
        - node = p1 * v2    =>  p1 = node / v2 
        - node = v1 * p2    =>  p2 = node / v1
        - node = p1 - v2    =>  p1 = node + v2 
        - node = v1 - p2    =>  p2 = v1 - node 
        - node = p1 / v2    =>  p1 = node * p1 
        - node = v1 / p2    =>  p2 = v1 / node
    - After processing all levels, we process the equations in the stack:
        - Set the value of this subtree's root to the value of the opposite subtree's root 
        - Then, go down and compute the values of the lower nodes 
        - The directions is now from root -> humn node, since we reversed the equations 
- Ouput the value of the humn node
'''