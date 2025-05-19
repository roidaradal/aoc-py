# Advent of Code 2015 Day 10
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readLines(15, 10, full)[0]

def solve():
    text = data(full = True)

    length = repeatExpand(text, 40)
    print(length)

    length = repeatExpand(text, 50)
    print(length)

def repeatExpand(text: str, count: int) -> int:
    curr = text
    for _ in range(count):
        nxt = []
        d, r = curr[0], 1 
        for x in curr[1:]:
            if x == d:
                r += 1
            else:
                nxt.append(str(r))
                nxt.append(d)
                d, r = x, 1
        nxt.append(str(r))
        nxt.append(d)
        curr = ''.join(nxt)
    return len(curr)

if __name__ == '__main__':
    do(solve)

'''
Solve: 
- For Part 1, repeat 40 times; for Part 2, repeat 50 times
- Repeatedly expand the text multiple times by going through the text digits 
- A chunk of digits is formed if the contiguous digits are all same digit 
- Once we segment the text digits into chunks, form the next text by concatenating the chunk size and chunk digits
'''