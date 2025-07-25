# Advent of Code 2023 Day 19
# John Roy Daradal 

import operator
from aoc import *

Item = dict[str, int]
Condition = tuple[str, str, int] # property, >/<, limit
Rule = tuple[Condition, str] # Condition, nextKeyIfOk
opp = {
    '<' : '>=',
    '>' : '<=',
}
opFn = {
    '<' : operator.lt, 
    '>' : operator.gt, 
    '<=': operator.le, 
    '>=': operator.ge,
}
trueCondition: Condition = ('x', '>', 0)

class Node: 
    def __init__(self, condition: Condition):
        self.condition = condition 
        self.leftChild:  Node|None = None 
        self.rightChild: Node|None = None
        self.isLeaf: bool = False 
        self.accept: bool = False

def data(full: bool) -> tuple[dict[str, list[Rule]], list[Item]]:
    ruleBook : dict[str, list[Rule]] = {}
    items: list[Item] = []
    itemMode = False
    for line in readLines(23, 19, full):
        if line == '':
            itemMode = True 
        elif itemMode:
            line = line.strip('{}')
            item: Item = {}
            for entry in splitStr(line, ','):
                k,v = splitStr(entry, '=')
                item[k] = int(v)
            items.append(item) 
        else:
            key, tail = splitStr(line, '{')
            parts = splitStr(tail.strip('}'), ',')
            rules: list[Rule] = []
            for part in parts[:-1]:
                head, nextKey = splitStr(part, ':')
                if '<' in head:
                    field, limit = splitStr(head, '<')
                    condition = (field, '<', int(limit))
                    rules.append((condition, nextKey))
                elif '>' in head:
                    field, limit = splitStr(head, '>')
                    condition = (field, '>', int(limit))
                    rules.append((condition, nextKey))
            fallback = parts[-1]
            rules.append((trueCondition, fallback))
            ruleBook[key] = rules
    return ruleBook, items

def solve() -> Solution:
    ruleBook, items = data(full=True)

    # Part 1
    total1 = 0
    for item in items:
        if isItemAccepted(item, ruleBook):
            total1 += sum(item.values())

    # Part 2
    root = createSubtree(trueCondition, ruleBook['in'], ruleBook)
    q: list[tuple[Node, list[Condition]]] = [(root, [])]
    accepted: set[tuple[Condition,...]] = set()
    while len(q) > 0:
        node, path = q.pop(0)
        if node.isLeaf:
            if node.accept:
                combo = tuple(sorted(path + [node.condition]))
                accepted.add(combo)
        else:
            if node.leftChild != None:
                q.append((node.leftChild, path + [node.condition]))
            if node.rightChild != None:
                q.append((node.rightChild, path + [node.condition]))

    total2 = 0
    for conditions in accepted:
        total2 += countCombos(list(conditions))

    return newSolution(total1, total2)

def isItemAccepted(item: Item, ruleBook: dict[str, list[Rule]]) -> bool:
    key = 'in'
    while True:
        key = getNextKey(ruleBook[key], item)
        if key == 'A':
            return True 
        elif key == 'R':
            return False

def getNextKey(rules: list[Rule], item: Item) -> str:
    nextKey = ''
    for condition, nextKey in rules:
        if isConditionSatisfied(condition, item):
            break
    return nextKey

def isConditionSatisfied(condition: Condition, item: Item) -> bool:
    (field, op, limit) = condition
    if op == '<':
        return item[field] < limit 
    elif op == '>':
        return item[field] > limit 
    return False

def oppositeCondition(condition: Condition) -> Condition:
    field, op, limit = condition
    return (field, opp[op], limit)

def createSubtree(rootCondition: Condition, rules: list[Rule], ruleBook: dict[str, list[Rule]]) -> Node:
    root = Node(rootCondition)
    rule1 = rules[0]
    condition, nextKey = rule1 

    # Left subtree 
    leftCondition = condition
    if nextKey == 'A' or nextKey == 'R':
        root.leftChild = createLeafNode(nextKey, leftCondition)
    else:
        root.leftChild = createSubtree(leftCondition, ruleBook[nextKey], ruleBook)

    # Right subtree
    rightCondition = oppositeCondition(condition)
    rules2 = rules[1:]
    if len(rules2) == 1: # last rule = fallback 
        _, nextKey = rules2[0]
        if nextKey == 'A' or nextKey == 'R':
            root.rightChild = createLeafNode(nextKey, rightCondition)
        else:
            root.rightChild = createSubtree(rightCondition, ruleBook[nextKey], ruleBook)
    else: # 2 or more rules left 
        root.rightChild = createSubtree(rightCondition, rules2, ruleBook)

    return root

def createLeafNode(key: str, condition: Condition) -> Node:
    leaf = Node(condition)
    leaf.isLeaf = True 
    leaf.accept = key == 'A'
    return leaf

def countCombos(conditions: list[Condition]) -> int:
    domain = {prop: list(range(1,4001)) for prop in 'xmas'}
    for field, op, limit in conditions:
        domain[field] = [x for x in domain[field] if opFn[op](x, limit)]
    x, m, a, s = [len(domain[prop]) for prop in 'xmas']
    return x*m*a*s

if __name__ == '__main__':
    do(solve, 23, 19)

'''
Part1:
- Go through the items and check if they are accepted by the rule book
- Start with the rules for 'in'; repeat until we reach A (accept) or R (reject)
- Go through the current rules: check the rule condition if the item satisfies it
- The condition is satisfied if the item[field] (< or >) limit 
- If the condition is satisfied, we return the nextKey of this rule, otherwise we continue
  to the next rule; eventually, we reach the fallback rule, which tells you which key to go next
- If the next key return is not yet A or R, we continue with the same process
- Return the sum of the total of item values for accepted items

Part2:
- Build a decision tree with root at 'in'; its condition is a true condition (no effect)
- A node has a condition, leftChild and rightChild (if not leaf); if it is a leaf node, it has an accept flag
- To create a subtree, create the subtree root with the given root condition
- Its left child will process the satisfied first rule:
    - If the first rule's nextKey is A or R, we create a leaf node holding the first rule's condition, with the proper accept flag
    - Otherwise, we recursively call createSubtree to form the left subtree, with the leftCondition at the root
- Its right child will process the failed first rule, and continue with the rest of the remaining rules
    - Create the rightCondition by forming the opposite of leftCondition
    - If there is only 1 more rule left, do a similar processing to left child
        - If the nextKey of the last rule is A or R, create a left node holding the rightCondition, with the proper accept flag
        - Otherwise, we recursively call createSubtree to from the right subtree, with the rightCondition at the root
    - If there are 2 or more rules left, recursively call createSubtree with the rightCondition, 
      but only using the remaining rules (not resetting to a new set of rules for the nextKey)
- After forming the decision tree, we use BFS traversal to find the leaf accept nodes, exploring the leftChild and rightChild of nodes
- While traversing the decision tree, we collect the conditions at each node we encounter
- On accepting leaf nodes, we collect the combination of conditions that lead to an acceptance
- We transform the combo to tuple(sorted(combo)) to normalize the combos, and add them to a set to avoid duplications
- For each of the unique condition combinatinos that lead to an acceptance, we count the number of number combinations 
  for x,m,a,s = [1,4000] that satisfies the conditions
    - Start with the domain of x,m,a,s = [1,4000]
    - Go through each condition and apply the condition to the domain of interest to filter out invalid values
    - Number of combinations for that condition set is the product of the domain sizes of x,m,a,s after processing all conditions
- Return the total count for all accepted combinations
'''