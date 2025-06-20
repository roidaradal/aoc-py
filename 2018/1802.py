# Advent of Code 2018 Day 02
# John Roy Daradal 

import itertools
from aoc import *

def data(full: bool) -> list[str]:
    return readLines(18, 2, full)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    words = data(full=True)
    count2, count3 = 0, 0 
    for word in words:
        freq = charFreq(word).values()
        if 2 in freq: count2 += 1 
        if 3 in freq: count3 += 1
    return count2 * count3

def part2() -> str:
    words = data(full=True)
    word = ''
    for word1, word2 in itertools.combinations(words, 2):
        diff = strDiff(word1, word2)
        if len(diff) != 1: continue 

        idx = diff[0]
        word = word1[:idx] + word1[idx+1:]
        break
    return word

# Return list of index where word1 and word2 differs
# Assumes word1 and word2 have same length
def strDiff(word1: str, word2: str) -> list[int]:
    diff = []
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            diff.append(i)
    return diff

if __name__ == '__main__':
    do(solve, 18, 2)

'''
Part1:
- Get character frequency values of each word
- Increase count2 if has freq of 2
- Increase count3 if has freq of 3 

Part2:
- Loop through pair combinations of words 
- If strDiff is only 1, remove char at that index 
'''