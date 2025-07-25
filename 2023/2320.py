# Advent of Code 2023 Day 20
# John Roy Daradal 

from aoc import *

BROAD, FLIP, CONJ = 0, 1, 2
label = {BROAD: 'BROAD', FLIP: 'FLIP', CONJ: 'CONJ'}

class Node:
    def __init__(self, kind: int, destination: list[str]):
        self.kind = kind 
        self.destination = destination
        # for flip-flop
        self.isOn: bool = False 
        # for conjunction 
        self.lastInput: dict[str,bool] = {}
    
    def addConnectedInput(self, name: str):
        self.lastInput[name] = False

    def processSignal(self, source: str, highPulse: bool) -> bool|None:
        if self.kind == FLIP:
            return self.processFlipSignal(highPulse)
        elif self.kind == CONJ:
            return self.processConjSignal(source, highPulse)
        return None

    def processFlipSignal(self, highPulse: bool) -> bool|None:
        if highPulse:
            return None
        else:
            self.isOn = not self.isOn # flip state 
            return self.isOn
        
    def processConjSignal(self, source: str, highPulse: bool) -> bool:
        self.lastInput[source] = highPulse
        return not all(self.lastInput.values())
        
def data(full: bool) -> dict[str, Node]:
    nodes: dict[str, Node] = {}
    for line in readLines(23, 20, full):
        head, tail = splitStr(line, '->')
        destination = splitStr(tail, ',')
        kind, name = BROAD, head
        if head.startswith('%'):
            kind, name = FLIP, name[1:]
        elif head.startswith('&'):
            kind, name = CONJ, name[1:]
        nodes[name] = Node(kind, destination)
    # Connect conj inputs 
    for name, node in nodes.items():
        for name2 in node.destination:
            if name2 not in nodes: continue
            if nodes[name2].kind == CONJ:
                nodes[name2].addConnectedInput(name)
    return nodes

def solve() -> Solution:
    # Part 1
    nodes = data(full=True)
    totalLow, totalHigh = 0, 0
    for _ in range(1000):
        low, high, _ = sendPulse(nodes, None)
        totalLow += low 
        totalHigh += high
    total1 = totalLow * totalHigh

    # Part 2
    counts = []
    for grandParent in findRxGrandParents(nodes):
        nodes = data(full=True)
        i = 0
        while True:
            i += 1 
            _, _, success = sendPulse(nodes, (grandParent, True))
            if success: break 
        counts.append(i)
    total2 = 1 
    for count in counts: total2 *= count

    return newSolution(total1, total2)

def sendPulse(nodes: dict[str,Node], goal: tuple[str,bool]|None) -> tuple[int, int, bool]:
    # Start with 1 low pulse from button -> broadcast
    counts = [1, 0] # low, high
    q: list[tuple[str,str,bool]] = []

    # Send low pulse from broadcaster -> destinations
    src = 'broadcaster'
    for dst in nodes[src].destination:
        q.append((src, dst, False))
    
    # Process the pulses in order 
    while len(q) > 0:
        src, dst, highPulse = q.pop(0)
        counts[int(highPulse)] += 1     # False indexes 0 (low), True indexes 1 (high)
        if goal != None and (src, highPulse) == goal:
            return 0, 0, True 
        
        if dst not in nodes: continue   # skip unknown node

        node = nodes[dst]
        result = node.processSignal(src, highPulse)
        if result is None: continue

        src = dst
        for dst in node.destination:
            q.append((src, dst, result))

    low, high = counts
    return low, high, False

def findRxGrandParents(nodes: dict[str,Node]) -> list[str]:
    grandParents: list[str] = []
    goal: str = 'rx'
    parent: str = ''
    # Find rx parent 
    for name, node in nodes.items():
        if goal in node.destination:
            parent = name 
            break 
    # Find grandparents 
    for name, node in nodes.items():
        if parent in node.destination:
            grandParents.append(name)
    return grandParents

if __name__ == '__main__':
    do(solve, 23, 20)

'''
Part1:
- Build the signal network by creating the broadcaster, flip-flop, and conjuction nodes and their destinations from the input
- Pass through the nodes again, so we can add the incoming inputs for conjunction nodes, and initialize their last input to False (low pulse)
- Send a pulse to the network 1000 times, getting the number of low and high pulse sent at each round 
    - Initialize the counts of low, high pulse to 1, 0 = 1 low pulse from button -> broadcast starts it 
    - We use a queue to process the sent pulses in order; start by adding the low pulse sent from broadcaster to each of its destination
    - The queue contains (src, dst, pulse) tuples
    - For each processed pulse, we increment the low/high count
    - Process the received signal from the src node to the dst node
    - If flip-flop node: ignore high pulse (return None); otherwise, flip the state (initial False) and return it 
    - If conjunction node: update the last input from the src, then return low pulse if all last inputs are high
    - If has output signal, use the dst as the new source and add its destinations to the queue, with the output signal
- Return the total low pulse count multiplied by the total high pulse count

Part2:
- Analyze the graph, starting with rx:
    - Only one node connects to it, a conjunction node (parent)
    - The parent node has 4 nodes that connect to it (grandParents)
    - The parent node needs to send a low pulse to rx
    - For the conjunction parent node to send a low pulse, all its inputs (grandParents) must send a high pulse
- Find the 4 grandParents of the rx node:  
    - Start by finding the parent: which node has rx in its destination
    - Then, identify grandParents by finding nodes with the parent in its destination
- For each grandParent, send a low pulse repeatedly until we see this grandParent node sending a high pulse
- Take note of the number of presses it took for each grandParent to send a high pulse 
- We can then take the LCM of these 4 counts, to see when they align the earliest - when all of them will send a high pulse
- Since the 4 counts are prime numbers, we can just take their product instead
'''