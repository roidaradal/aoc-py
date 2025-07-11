# Advent of Code 2021 Day 16
# John Roy Daradal 

from aoc import *

class Packet:
    def __init__(self, version: int, kind: int, depth: int):
        self.depth = depth
        self.version = version 
        self.kind = kind
        self.isValue = kind == 4

        self.value: int = 0
        self.children: list[Packet] = []

    def __repr__(self) -> str:
        tail = ('x=%d' % self.value) if self.isValue else ('c=%d' % len(self.children))
        return '[d%d, v%d, k%d, %s]' % (self.depth, self.version, self.kind, tail)

    def computeValue(self):
        if self.isValue: return 

        match self.kind:
            case 0:
                total = 0
                for child in self.children:
                    total += child.value 
                self.value = total 
            case 1:
                product = 1 
                for child in self.children:
                    product *= child.value 
                self.value = product 
            case 2: 
                self.value = min([child.value for child in self.children])
            case 3:
                self.value = max([child.value for child in self.children])
            case 5:
                c1, c2 = self.children 
                self.value = 1 if c1.value > c2.value else 0
            case 6:
                c1, c2 = self.children 
                self.value = 1 if c1.value < c2.value else 0
            case 7:
                c1, c2 = self.children 
                self.value = 1 if c1.value == c2.value else 0

def data(full: bool) -> str:
    return readFirstLine(21, 16, full)

def solve() -> Solution:
    message = data(full=True)

    # Part 1
    bits = hexToBinary(message)
    packet, _ = processPacket(bits)
    
    total = 0
    stack: list[Packet] = [packet]
    visited: list[Packet] = []
    while len(stack) > 0:
        packet = stack.pop()
        visited.append(packet)
        total += packet.version 
        for child in packet.children:
            stack.append(child)

    # Part 2
    # Process leaf node values first, up to root
    for packet in sorted(visited, key=lambda p: p.depth, reverse=True):
        packet.computeValue()
    # Depth 0 is last packet processed
    topValue = packet.value 

    return newSolution(total, topValue)

def hexToBinary(message: str) -> str:
    out: list[str] = []
    for hex in message:
        x = int(hex, 16)
        out.append(binaryFilled(x, 4))
    return ''.join(out)

def processPacket(bits: str, depth: int=0) -> tuple[Packet, str]:
    version = int(bits[0:3], 2)
    kind = int(bits[3:6], 2)
    packet = Packet(version, kind, depth)
    extra = ''

    if kind == 4:
        value, extra = processValue(bits[6:])
        packet.value = value 
    elif bits[6] == '0':
        i = 7 
        length = int(bits[i:i+15], 2)
        start = i+15
        extra = bits[start:start+length]
        while len(extra) > 0:
            child, extra = processPacket(extra, depth+1)
            packet.children.append(child)
        extra = bits[start+length:]
    elif bits[6] == '1':
        i = 7 
        count = int(bits[i:i+11], 2)
        start = i+11
        extra = bits[start:]
        for _ in range(count):
            child, extra = processPacket(extra, depth+1)
            packet.children.append(child)

    return packet, extra

def processValue(bits: str) -> tuple[int, str]:
    result: list[str] = []
    i, limit = 0, len(bits)
    while i < limit:
        flag, number = bits[i], bits[i+1:i+5]
        result.append(number)
        i += 5
        if flag == '0': break
    value = int(''.join(result), 2)
    return value, bits[i:]


if __name__ == '__main__':
    do(solve, 21, 16)

'''
Part1:
- Convert each hex digit into its equivalent 4-digit binary code
- Process the binary digits of the packet, default depth = 0
- First 3 bits = version number, Next 3 bits = packet type
- Create the packet object with the version, kind, and depth 
- If type 4, packet contains a literal value:
    - Process the bits in 5s: 1st one is the flag that tells you if this is the 
      last group (0), and the next 4 bits are the value
    - Collect the 4 bits until we see a 0 flag
    - Return the decimal equivalent of the joined bits, and the extra unprocessed bits
- If next bit is 0, the next 15 bits tell you the number of bits to process for the subpackets
    - Recursively call processPacket on the extracted substring (depth+1), feeding back the extra to the next iteration
    - Add the result to the current packet's children
    - Make sure the extra string is from where you stopped processing the substring
- If next bit is 1, next 11 bits tell you the number of subpackets to process
    - Repeatedly call processPacket recursively and add to the current packet's children
- Return the packet and the extra string
- Starting from the top packet, visit the packets via DFS, so we can get the total version number of the packets

Part2:
- From the visited packets in Part 1, sort them according to descending depth order (leaf first)
- Compute the value of the leaf packets according to the packet type, then the inner nodes follow
- Since we ordered by depth, the children nodes' values will be computed before the parent's
- Return the value of the root node
'''