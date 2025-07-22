# Advent of Code 2022 Day 20
# John Roy Daradal 

from aoc import *

class Node:
    def __init__(self, index: int, value: int):
        self.index = index 
        self.value = value 
        self.prev: Node = self 
        self.next: Node = self 

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(22, 20, full)]

def solve() -> Solution:
    numbers = data(full=True)
    limit = len(numbers)

    # Part 1 
    head = createDLL(numbers)
    zero1 = mixNumbers(head, limit, 1)
    total1 = getTotalCoords(zero1)

    # Part 2
    factor = 811589153
    numbers = [x * factor for x in numbers]
    head = createDLL(numbers)
    zero2 = mixNumbers(head, limit, 10)
    total2 = getTotalCoords(zero2)

    return newSolution(total1, total2)

def createDLL(numbers: list[int]) -> Node:
    head = Node(0, numbers[0])
    prev = head 
    for idx in range(1, len(numbers)):
        curr = Node(idx, numbers[idx])
        prev.next = curr 
        curr.prev = prev 
        prev = curr 
    prev.next = head 
    head.prev = prev 
    return head

def findNodeIndex(curr: Node, index: int) -> Node:
    if curr.index == index:
        return curr 
    prev, nxt = curr, curr 
    while True:
        prev = prev.prev 
        nxt  = nxt.next 
        if prev.index == index:
            return prev 
        if nxt.index == index:
            return nxt

def mixNumbers(head: Node, limit: int, rounds: int) -> Node:
    zeroNode = head 

    for _ in range(rounds):  
        curr = head
        for idx in range(limit):
            curr = findNodeIndex(curr, idx)
            numSteps = abs(curr.value) % (limit-1)

            if curr.value == 0:
                zeroNode = curr 
                continue 

            if numSteps == 0: 
                numSteps = limit-1
        
            # Detach old current from its neighbors
            oldCurr = curr 
            oldPrev = curr.prev
            oldNext = curr.next
            oldPrev.next = oldNext 
            oldNext.prev = oldPrev


            if curr.value < 0:
                for _ in range(numSteps):
                    curr = curr.prev 
                prev = curr.prev

                prev.next = oldCurr 
                oldCurr.prev = prev 
                oldCurr.next = curr 
                curr.prev = oldCurr

            elif curr.value > 0:
                for _ in range(numSteps):
                    curr = curr.next 
                nxt = curr.next

                curr.next = oldCurr 
                oldCurr.prev = curr 
                oldCurr.next = nxt 
                nxt.prev = oldCurr
    return zeroNode 

def getTotalCoords(zeroNode: Node) -> int:
    total = 0
    curr = zeroNode 
    for i in range(3000):
        curr = curr.next
        if (i+1) % 1000 == 0:
            total += curr.value
    return total

if __name__ == '__main__':
    do(solve, 22, 20)

'''
Solve:
- Use a DLLNode that contains the value and the original index (for ordering)
- Create the DLL from the given numbers, using the original order for the index
- Repeat the numbers mixing for the specified number of rounds 
    - For each round, we start at the head of the DLLNode
    - Go through the ranks in order (0, 1, 2, ..., limit-1)
    - Find the node with the given rank by starting from the current node and searching bi-directionally:
      one pointer goes backwards to the previous, one pointer goes forward to the next, to find the node faster
    - If the index node's value is 0, we store it as the zeroNode (to be returned later)
    - The number of steps we will take to move the index node is the abs(node.value)
    - However, since the node values will be magnified in Part 2, we will use modulo limit-1 to skip all the rounds 
      where we have to go through the full DLL (limit-1 because there are N nodes, there will only be N-1 hops in between)
    - But if we have numSteps == 0, that means that the number of steps is actually limit-1
    - Detach the old index node from its neighbors and connect the neighbors (prev/next) instead
    - If the node.value is negative, we go backwards (prev), otherwise we go forward (next)
    - Take numSteps steps forward/backward, and take note of the next/prev after where you landed 
    - Insert the old index node between where you landed and its previous neighbor
- After mixing all numbers for the specified number of rounds, return the found zeroNode
- From the zeroNode, find the values of the 1000, 2000, and 3000th node after it and return their sum
- For Part 1, mix the numbers 1 time
- For Part 2, multiply the numbers first by the factor (811589153) and mix the numbers 10 times
'''