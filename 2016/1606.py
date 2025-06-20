# Advent of Code 2016 Day 06
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    return readLines(16, 6, full)

def solve() -> Solution:
    words = data(full=True)
    freq = columnFrequency(words)
    maxMsg, minMsg = [], []
    for col in range(len(freq)):
        colFreq = [(count,letter) for letter,count in freq[col].items()]
        # Part 1
        maxMsg.append(max(colFreq)[1])
        # Part 2
        minMsg.append(min(colFreq)[1])
    maxMsg = ''.join(maxMsg)
    minMsg = ''.join(minMsg)

    return newSolution(maxMsg, minMsg)

def columnFrequency(words: list[str]) -> dict[int,dict[str,int]]:
    _, numCols = getBounds(words)
    freq: dict[int,dict[str,int]] = {i: defaultdict(int) for i in range(numCols)}
    for word in words:
        for col,char in enumerate(word):
            freq[col][char] += 1
    return freq

if __name__ == '__main__':
    do(solve, 16, 6)

'''
Solve:
- Get the frequency of characters per column 
- For Part 1, form the message by getting the max frequency characters per column
- For Part 2, form the message by getting the min frequency characters per column
'''