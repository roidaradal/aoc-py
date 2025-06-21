# Advent of Code 2020 Day 14
# John Roy Daradal 

import itertools
from aoc import *

Command = tuple[str, str]

def data(full: bool) -> list[Command]:
    def fn(line: str) -> Command:
        key, value = splitStr(line, '=')
        if key != 'mask':
            key = key.split('[')[1].strip(']')
        return (key, value)
    return [fn(line) for line in readLines(20, 14, full)]

def solve() -> Solution:
    commands = data(full=True)
    
    # Part 1
    total1 = processCommands(commands, False)

    # Part 2
    total2 = processCommands(commands, True)

    return newSolution(total1, total2)

def processCommands(commands: list[Command], maskAddress: bool) -> int:
    mask = ''
    mem: dict[int,int] = {}
    for key, value in commands:
        if key == 'mask':
            mask = value 
        else:
            if maskAddress:
                addrs = maskedAddress(binary(key), mask)
                v = int(value)
                for addr in addrs:
                    mem[addr] = v
            else:
                addr = int(key)
                mem[addr] = maskedValue(binary(value), mask)

    return sum(mem.values())

def binary(x: str) -> str:
    b = bin(int(x))[2:]
    return b.zfill(36)

def maskedValue(value: str, mask: str) -> int:
    r: list[str] = []
    for v,m in zip(value, mask):
        x = v if m == 'X' else m 
        r.append(x)
    b = ''.join(r)
    return int(b, 2)

def maskedAddress(address: str, mask: str) -> list[int]:
    r: list[str] = []
    for a,m in zip(address, mask):
        x = a if m == '0' else m 
        r.append(x)
    indexes = [i for i in range(len(r)) if r[i] == 'X']
    count = len(indexes)
    addrs: list[int] = []
    for bits in itertools.product('01', repeat=count):
        addr = r[:]
        for i,b in zip(indexes, bits):
            addr[i] = b 
        a = ''.join(addr)
        addrs.append(int(a, 2))
    return addrs

if __name__ == '__main__':
    do(solve, 20, 14)

'''
Solve: 
- Process each command and return the sum of memory values after 
- If mask command, update the mask 
- Otherwise, update the memory address with value
- For Part 1, mask the value before updating the memory address
    - Get the 36-bit binary representation of the value 
    - Apply the mask to the binary value:
        - If mask bit is X, copy the binary digit 
        - Otherwise, copy the mask bit
    - Convert the masked binary back to integer
- For Part 2, the masked address produces several memory addresses to update value
    - Get the 36-bit binary representation of the address 
    - Apply the mask to the binary address:
        - If mask bit is 0, copy the binary digit (unchanged)
        - Otherwise, copy the mask bit (X or 1)
    - Find the indexes in the result where the mask bit is X: these are replaceable with 0 or 1 
    - Find all combinations of 0,1 that can fill in the indexes 
    - Combining the existing address and the X replaced with 0-1 values produces multiple addresses 
    - The list of binary addresses produced are converted back to integer
'''