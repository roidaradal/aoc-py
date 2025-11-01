# Advent of Code 2024 Day 24
# John Roy Daradal 

from aoc import *

str4 = tuple[str,str,str,str] # out, p1, p2, op

XOR, OR, AND = 'XOR', 'OR', 'AND'

def data(full: bool) -> tuple[dict[str,bool], list[str4]]:
    values: dict[str, bool] = {}
    gates: list[str4] = []
    gateMode = False
    for line in readLines(24, 24, full):
        if line == '':
            gateMode = True 
        elif gateMode:
            head, out = splitStr(line , '->') 
            p1, op, p2 = splitStr(head, None)
            p1, p2 = sorted([p1, p2])
            gates.append((out, p1, p2, op))
        else:
            key, value = splitStr(line, ':')
            values[key] = value == '1'
    return values, gates

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    values, gates = data(full=True)
    zkeys: list[str] = [g[0] for g in gates if g[0].startswith('z')]
    
    defer: list[str4] = gates 
    while True:
        defer2: list[str4] = []
        for gate in defer:
            out,p1,p2,op = gate
            if p1 in values and p2 in values:
                v1, v2, v3 = values[p1], values[p2], False
                if op == 'AND':
                    v3 = v1 & v2
                elif op == 'OR':
                    v3 = v1 | v2 
                elif op == 'XOR':
                    v3 = v1 ^ v2 
                values[out] = v3
            else:
                defer2.append(gate)

        defer = defer2
        if all(zkey in values for zkey in zkeys): break 
    
    bits: list[str] = []
    for zkey in sorted(zkeys, reverse=True):
        bit = '1' if values[zkey] else '0'
        bits.append(bit)
    output = int(''.join(bits), 2)
    return output

def part2() -> str:
    _, gates = data(full=True)
    conn = createConnections(gates, [])
    swapped: list[str2] = []

    while True:
        swap = findSwappable(conn)
        if swap is None: break 
        swapped.append(swap)
        conn = createConnections(gates, swapped)

    output: list[str] = []
    for out1, out2 in swapped:
        output.append(out1)
        output.append(out2)

    return ','.join(sorted(output))

def findSwappable(conn: dict[str2, str2]) -> str2|None:
    p2,out = conn[('x00', AND)]
    carry = out 

    for d in range(1,45):
        xkey = 'x%.2d' % d 
        ykey = 'y%.2d' % d 
        zkey = 'z%.2d' % d

        # x ^ y = res
        p2, res = conn[(xkey, XOR)]
        if p2 != ykey:
            print('Error in x^y: %s, exp: %s, got: %s' % (xkey, ykey, p2))
        
        # x & y = extra1
        p2, extra1 = conn[(xkey,AND)]
        if p2 != ykey:
            print('Error in x&y: %s, exp: %s, got: %s' % (xkey, ykey, p2))

        # carry ^ res = z 
        p2, out = conn[(carry, XOR)]
        if p2 != res:
            return (res, p2)
        if out != zkey:
            return (out, zkey)

        # carry & res = extra2
        p2, extra2 = conn[(carry, AND)]
        if p2 != res:
            return (res, p2)

        # extra1 | extra2 = ncarry
        p2, ncarry = conn[(extra1, OR)]
        if p2 != extra2:
            print('Error in extra1|extra2: %s, exp: %s, got: %s' % (extra1, extra2, p2))

        carry = ncarry
    return None

def createConnections(gates: list[str4], swapped: list[str2]) -> dict[str2, str2]:
    swap: dict[str, str] = {}
    for out1, out2 in swapped:
        swap[out1] = out2 
        swap[out2] = out1 

    conn: dict[str2,str2] = {}
    for out,p1,p2,op in gates:
        if out in swap: out = swap[out]
        for pair in [(p1,p2),(p2,p1)]:
            n1, n2 = pair 
            conn[(n1,op)] = (n2,out)

    return conn

if __name__ == '__main__':
    do(solve, 24, 24)

'''
Part1:
- Read the initial gate values and the gate configurations from the input
- The z-gates are the gates whose output names start with z 
- Repeat until we find the values of all z-gates:
    - Initially all gates are in the defer list
    - Go through the defer list gates
    - If param1 or param2 of the gate still doesn't have a value, defer again to the next round
    - If both params have values, compute the value of the output gate by doing the AND/OR/XOR operation
- If all the z-gates have values, compute the output by going through them in reverse order
    - Go from z45 down to z00, use bit 1 if True, else 0
    - The collected bits form the binary number, output the decimal equivalent

Part2:
- These gates represent x + y = z:
    - Bits for x are represented by x00 to x44 
    - Bits for y are represented by y00 to y44 
    - Bits for z are represented by z00 to z45
    - All other gates are part of the addition process
- Figure out the 8 gates that have their outputs switched by going through the gates 
  and checking their expected output vs the actual output gate
- From the list of gates with (out, p1, p2, op) format, create the connection lookup 
  (p1, op) => (p2, out) and (p2, op) => (p1, out)
- This is for easy lookup of the expected pair parameter and output gate for the given 
  parameter and operation; we use this for comparing the expected vs actual
- Additionally, we can send in a list of swapped connections so that we can correct this 
  in the connection lookup we will output
- For the last bit, adding x00 and y00 follows this process:
    - z00 = x00 ^ y00 (if different = 1, if same = 0)
    - carry = x00 & y00 (carry 1 if both 1, else 0)
- For the general form, adding xN and yN follows this process:
    - res = x ^ y                   (main result of adding the 2 bits)
    - extra1 = x & y                (main carry of adding the 2 bits)
    - zN = carry ^ res              (final result = main result ^ previous carry)
    - extra2 = carry & res          (extra carry = previous carry & main result)
    - ncarry = extra1 | extra2      (next carry = either main/carry extra is 1)
- Based on the equations above, we can check whether the connected param2 and the declared 
  output gate are the expected values; if not, return the expected and actual pair as swappable
- Once we find a swappable pair, we swap them, recompute the connections and try again
- We stop the loop if no swaps were found
- Output the list of sorted swapped outputs, separated by comma
'''