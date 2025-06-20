# Advent of Code 2017 Day 01
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> str:
    return readFirstLine(17, 1, full)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    word = data(full=True)
    wordLen = len(word)
    def fn(i: int) -> int:
        j = (i+1) % wordLen 
        return int(word[i]) if word[i] == word[j] else 0
    numbers = list(range(wordLen))
    return getTotal(numbers, fn)

def part2() -> int:
    word = data(full=True)
    mid = len(word) // 2 
    def fn(i: int) -> int:
        j = mid+i 
        return 2 * int(word[i]) if word[i] == word[j] else 0 
    numbers = list(range(mid))
    return getTotal(numbers, fn)

if __name__ == '__main__':
    do(solve, 17, 1)

'''
Part1:
- Sum up digits that are same as next digit (with wraparound)

Part2:
- Check first half of digits (until mid) 
- Compare digit with corresponding digit in the second half 
- Sum up 2*digit if they match 
'''