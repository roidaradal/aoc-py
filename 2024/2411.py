# Advent of Code 2024 Day 11
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    line = readFirstLine(24, 11, full)
    return toIntList(line, None)

def solve() -> Solution:
    stones = data(full=True)

    # Part 1 
    count1 = countStones(stones, 25)

    # Part 2
    count2 = countStones(stones, 75)

    return newSolution(count1, count2)

def countStones(stones: list[int], steps: int) -> int:
    freq: dict[int,int] = countFreq(stones)
    for _ in range(steps):
        freq2: dict[int,int] = defaultdict(int)
        for stone, count in freq.items():
            digits = str(stone)
            if stone == 0:
                freq2[1] += count 
            elif len(digits) % 2 == 0:
                mid = len(digits) // 2 
                half1 = int(digits[:mid])
                half2 = int(digits[mid:])
                freq2[half1] += count 
                freq2[half2] += count
            else:
                freq2[stone*2024] += count
        freq = freq2
    return sum(freq.values())

if __name__ == '__main__':
    do(solve, 24, 11)

'''
Solve:
- For Part 1, count the total stones after 25 steps
- For Part 2, count the total stones after 75 steps
- Count the initial frequency of each stone
- Repeat for the given number of steps:
    - For each (stone,count) perform the transformations
    - If stone is 0, transform it to a stone 1 
    - If stone has even number of digits, it is divided into 2 stones with 
      the left half and right half of the digits 
    - Otherwise, the stone is transformed into stone*2024
- Return the total number of stones = sum of frequency values
- Idea: Group the stones with their counts to make the computation faster
'''