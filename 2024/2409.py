# Advent of Code 2024 Day 09
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    line = readFirstLine(24, 9, full)
    return toIntLine(line)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    numbers = data(full=True)
    head, tail = buildLinkedList(numbers)
    a, b = head, tail 
    while True:
        while a.value != None: # look for free space
            a = a.next
        while b.value == None: # look for file
            b = b.prev
        if a.rank > b.rank: break # passed by each other in the middle

        if a.size == b.size: # same size = swap values 
            a.value, b.value = b.value, a.value 
        elif a.size < b.size: # not enough free space
            a.value = b.value 
            b.size = b.size - a.size 
        elif a.size > b.size: # has room for more 
            a.value, b.value = b.value, a.value 
            free = a.size - b.size 
            a.size = b.size 
            node = Node(None, free, a.rank)
            node.prev = a 
            node.next = a.next 
            a.next.prev = node 
            a.next = node

    return getChecksum(head)
     
def part2() -> int:
    numbers = data(full=True)
    head,tail = buildLinkedList(numbers)
    curr = tail 
    while True:
        fid = curr.value 
        # look for leftmost free space that can fit current size 
        free: Node|None = head 
        while True:
            if free != None and free.value is None and free.size >= curr.size:
                break
            if free != None and free.isTail: 
                free = None 
                break
            else:
                free = free.next 
        
        # ensure free is a node and it is to left of current node 
        if free != None and free.rank < curr.rank:
            if free.size == curr.size: # same size = swap values 
                free.value, curr.value = curr.value, free.value 
            else: # has room for more 
                free.value, curr.value = curr.value, free.value 
                left = free.size - curr.size 
                free.size = curr.size 
                node = Node(None, left, free.rank)
                node.prev = free 
                node.next = free.next 
                free.next.prev = node 
                free.next = node
        
        # find next file to move (value-1)
        goal = fid-1 if fid != None else 0
        if goal > 0:
            while curr.value != goal:
                curr = curr.prev
        else:
            break # dont look for 0 anymore, no left free space anyway

    return getChecksum(head)

class Node:
    def __init__(self, value: int|None, size: int, rank: int):
        self.value = value 
        self.size = size 
        self.rank = rank 
        self.isHead = False 
        self.isTail = False
        self.next: Node = self
        self.prev: Node = self

def buildLinkedList(numbers: list[int]) -> tuple[Node, Node]:
    N = len(numbers)
    head: Node = Node(0, 0, 0) 
    tail: Node = Node(0, 0, 0)
    curr: Node | None = None 
    rank = 0
    for i in range(0, N, 2):
        fid = i // 2 
        node1 = Node(fid, numbers[i], rank)
        rank += 1
        if curr is None:
            head = node1 
            head.isHead = True
        else:
            curr.next = node1 
            node1.prev = curr 
        
        if i < N-1:
            if numbers[i+1] > 0:
                node2 = Node(None, numbers[i+1], rank)
                rank += 1
                node1.next = node2 
                node2.prev = node1 
                curr = node2
            else:
                curr = node1
        else:
            tail = node1 
            tail.isTail = True
    return head, tail

def getChecksum(head: Node) -> int:
    checksum = 0
    i = 0 
    node = head 
    while True:
        for _ in range(node.size):
            if node.value != None:
                checksum += (i * node.value)
            i += 1
        if node.isTail:
            break 
        else:
            node = node.next 
    return checksum
    
if __name__ == '__main__':
    do(solve, 24, 9)

'''
Part1:
- Build the linked list from the number list 
- Start a pointer from the head, b pointer from the tail
- Look for a free space from the left 
- Look for files from the right 
- Stop if the a and b pointers have already passed by each other in the middle 
- If a and b have same size, swap values 
- If a.size < b.size, there is not enough free space, so transfer b's value to a,
  and adjust b's size by subtracting a's size (now b still has files left to transfer)
- If a.size > b.size, a has room for more, so we swap a and b's value and compute the 
  free space left after; create a new blank node with this free space and insert after a
- After exiting, compute the checksum and output it

Part2:
- Build the linked list from the number list 
- Start by getting files from the tail (right)
- Look for the leftmost free space that can fit the current size 
- If free node is found, transfer similar to Part 1:
    - If same size, just swap values
    - If has room for more, swap the values, create a new node with the leftover space and insert after 
- Find the next file to move (value-1)
- Important that we use value-based finding, because files could have been transfered to a space before it (redoing the transfer to front)
- After exiting, compute the checksum and output it

BuildLinkedList:
- Process the number list 2 at a time: a file size, and an empty block size
- Increment the rank of the file items as they are added 
- Build a DLL for easy insertion / deletion of nodes in between
- Add free space nodes (value=None) if it has non-zero size 
- Identify the head and tail of the DLL

GetChecksum:
- Traverse the DLL from head to tail 
- The i variable keeps track of the current index position
- Repeat node.size times to expand 1 node to its component files
- If not free space (value != None), add to the checksum the product of the value and the index
'''