# Advent of Code 2021 Day 14
# John Roy Daradal 

import math
from aoc import *

def data(full: bool) -> tuple[str, dict[str, str2]]:
    lines = readLines(21, 14, full)
    word = lines[0]
    T: dict[str, str2] = {}
    for line in lines[2:]:
        k, m = splitStr(line, '->')
        T[k] = (k[0]+m, m+k[1])
    return word, T

def solve() -> Solution:
    word, T = data(full=True)

    # Part 1
    diff1 = freqDiff(word, T, 10) 

    # Part 2
    diff2 = freqDiff(word, T, 40)

    return newSolution(diff1, diff2)

def freqDiff(word: str, T: dict[str, str2], steps: int) -> int:
    curr: dict[str,int] = defaultdict(int)
    for i in range(len(word)-1):
        pair = word[i:i+2]
        curr[pair] += 1
    
    for _ in range(steps):
        nxt: dict[str,int] = defaultdict(int)
        for pair, count in curr.items():
            for pair2 in T[pair]:
                nxt[pair2] += count
        curr = nxt 

    freq: dict[str,int] = defaultdict(int)
    for pair, count in curr.items():
        for letter in pair:
            freq[letter] += count 
    
    freqs = [math.ceil(v/2) for v in freq.values()]
    maxFreq, minFreq = max(freqs), min(freqs)
    return maxFreq - minFreq

if __name__ == '__main__':
    do(solve, 21, 14)

'''
Solve:
- From the input data, create a translation table that transforms the line:
    KS -> O into a dictionary entry: KS => (KO, OS)
    since the O will be inserted between the two, KS will be replaced by the KO, OS
- For Part 1, repeat the conversion 10 times 
- For Part 2, repeat the conversion 40 times
- Go through each 2-window in the input word; increment the pair's count 
- Repeat based on number of steps:
    - For each (pair, count) in the current pair frequency table,
      go through the replacements of pair from the translation table 
    - Increment the replacement pair's count in the next frequency table by the current count 
      since having 6 ABs, replaced by XY will have 6 XYs in the next round 
- Then, get the overall frequency of each letter 
- Correct the counts by dividing by 2 and taking the ceiling (for odd counts)
- We divide by 2 because we double counted by taking overlapping windows (middle counted twice)
- Take the minimum and maximum frequency count and return their difference
'''