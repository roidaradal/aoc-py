# Advent of Code 2017 Day 01
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> str:
    return readLines(17, 1, full)[0]

def part1():
    word = data(full=True)
    wordLen = len(word)
    def fn(i: int) -> int:
        j = (i+1) % wordLen 
        return int(word[i]) if word[i] == word[j] else 0
    numbers = list(range(wordLen))
    total = getTotal(numbers, fn)
    print(total) 

def part2():
    word = data(full=True)
    mid = len(word) // 2 
    def fn(i: int) -> int:
        j = mid+i 
        return 2 * int(word[i]) if word[i] == word[j] else 0 
    numbers = list(range(mid))
    total = getTotal(numbers, fn)
    print(total)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Sum up digits that are same as next digit (with wraparound)

Part2:
- Check first half of digits (until mid) 
- Compare digit with corresponding digit in the second half 
- Sum up 2*digit if they match 
'''