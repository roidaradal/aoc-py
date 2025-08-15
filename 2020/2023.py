# Advent of Code 2020 Day 23
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    line = readFirstLine(20, 23, full)
    return toIntLine(line)

def solve() -> Solution:
    numbers = data(full=True)

    # Part 1
    minDigit, maxDigit = min(numbers), max(numbers)
    nextOf = moveCups(numbers, 100, (minDigit, maxDigit))
    output: list[str] = []
    curr = nextOf[1]
    while curr != 1:
        output.append(str(curr))
        curr = nextOf[curr] 
    order = ''.join(output)

    # Part 2
    newMaxDigit = 1_000_000
    numbers += list(range(maxDigit+1, newMaxDigit+1))
    nextOf = moveCups(numbers, 10_000_000, (minDigit, newMaxDigit))
    a = nextOf[1]
    b = nextOf[a]
    product = a * b

    return newSolution(order, product)

def moveCups(numbers: list[int], moves: int, digitRange: int2) -> dict[int,int]:
    nextOf: dict[int, int] = {}
    prev = numbers[0]
    for i in range(1, len(numbers)):
        nextOf[prev] = numbers[i]
        prev = numbers[i]
    nextOf[prev] = numbers[0]
    minDigit, maxDigit = digitRange 

    curr = numbers[0]
    for _ in range(moves):
        # Pick up 3 cups next to curr 
        c1 = nextOf[curr]
        c2 = nextOf[c1]
        c3 = nextOf[c2]
        pickedUp = [c1, c2, c3]

        # Remove c1-c3 from loop
        nxt = nextOf[c3]
        nextOf[curr] = nxt 

        # Select destination 
        dest = maxDigit if curr == minDigit else curr-1 
        while dest in pickedUp:
            dest = maxDigit if dest == minDigit else dest-1
        
        # Add c1-c3 next to destination 
        nxt = nextOf[dest]
        nextOf[dest] = c1 
        nextOf[c3] = nxt 

        # Select next current 
        curr = nextOf[curr]

    return nextOf

if __name__ == '__main__':
    do(solve, 20, 23)

'''
Solve:
- Use a dictionary to map the next item of a number; choose dictionary for fast updating 
  and fast lookup of numbers (if array/DLL, need to search for numbers)
- For the specified number of moves, repeat the ff:
    - Pick up the 3 cups next to curr (note their values)
    - Remove c1-c3 from the loop, so we connect nextOf[curr] = nextOf[c3]
    - Select destination cup: subtract 1 from the current number, wrapping around to the 
      maximum digit if the minimum digit is reached
    - If that value is one of the picked up numbers, repeat until we find a non-picked up value
    - Add c1-c3 next to the destination cup by linking nextOf[dest] = c1 and nextOf[c3] = old nextOf[dest]
    - Update the next current number, by going to nextOf[curr]
- For Part 1, the crab moves the cups 100 times, then starting from 1's next number, 
  output the final order of numbers (repeatedly use nextOf until we loop back to 1)
- For Part 2, the numbers are extended up to 1,000,000, and the crab moves the cup 10 million times
- Get the two next numbers from 1 and output their product
'''