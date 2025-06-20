# Advent of Code 2017 Day 04
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[list[str]]:
    return [line.split() for line in readLines(17, 4, full)]

def solve() -> Solution:
    phrases = data(full=True)

    # Part 1
    fn1 = lambda phrase: isValid(phrase, False)
    count1 = countValid(phrases, fn1)

    # Part 2
    fn2 = lambda phrase: isValid(phrase, True)
    count2 = countValid(phrases, fn2)

    return newSolution(count1, count2)

def isValid(phrase: list[str], sortWord: bool) -> bool:
    freq = defaultdict(int) 
    for word in phrase:
        if sortWord: word = sortedStr(word)
        freq[word] += 1
    return all(count == 1 for count in freq.values())

if __name__ == '__main__':
    do(solve, 17, 4)

'''
Solve:
- For Part1, dont sort word; for Part2, sort word 
- Count valid phrases
- Phrase is valid if no word repeats: compute freq and check if all counts == 1
'''