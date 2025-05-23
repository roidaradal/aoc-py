# Advent of Code 2018 Day 08
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    line = readLines(18, 8, full)[0]
    return toIntList(line, None)

def part1():
    numbers = data(full=True)
    limit = len(numbers)
    child, meta = numbers[:2]
    stack = [(child,meta)]
    total = 0 
    i = 2
    while i < limit:
        if stack[-1][0] == 0:
            _, meta = stack.pop()
            for m in range(meta):
                total += numbers[i+m]
            i += meta
            if len(stack) == 0: continue 
            child, meta = stack[-1]
            stack[-1] = (child-1, meta)
        else: 
            child, meta = numbers[i], numbers[i+1]
            stack.append((child, meta))
            i += 2
    print(total)

def part2():
    numbers = data(full=True)
    limit = len(numbers)
    child, meta = numbers[:2]
    stack = [(child, meta, [])]
    i = 2 
    value = 0
    while i < limit:
        top = stack[-1]
        if top[0] == len(top[2]):
            child, meta, values = stack.pop()
            hasChild = child > 0
            value = 0
            for m in range(meta):
                if hasChild:
                    idx = numbers[i+m]-1    # adjust for 1-based index
                    if idx < len(values):
                        value += values[idx]
                else:
                    value += numbers[i+m]
            i += meta 
            if len(stack) == 0: break 
            child, meta, values = stack[-1]
            values.append(value)
            stack[-1] = (child, meta, values)
        else:
            child, meta = numbers[i], numbers[i+1]
            stack.append((child, meta, []))
            i += 2
    print(value)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- If node has children (else part), the next 2 numbers are the numChildren and metadata count
- Add this pair to the stack and move the index by 2
- If the top of the stack doesn't have children anymore (0), we can process the metadata part
- Remove the pair from the stack top, and add the next m numbers of the metadata to the total
- Move the index by the metadata count 
- If there is still a stack top, we decrement its children since it has already been processed

Part2:
- Similar to Part 1, but the stack now contains triple: numChildren, metaCount, and children values
- Else part is same as Part 1: next 2 numbers indicate numChildren and metadata count
- If the stack top's children already have computed values, we can compute the node's value too
- Remove the triple from the stack top; processing depends on whether node has children or not
- If no children, value is just the raw metadata values summed up (similar to Part 1)
- If has children, metadata values refer to children index (adjust -1 because 1-based)
- Only add to the total value if the child index is valid
- After computing the value of the node, add it to the new stack top's children values (the node's parent)
- Stop if stack is empty; print out the last value computed (root's value)
'''