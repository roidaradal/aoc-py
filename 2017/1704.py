# Advent of Code 2017 Day 04
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[list[str]]:
    return [line.split() for line in readLines(17, 4, full)]

def part1():
    phrases = data(full=True)
    fn = lambda phrase: isValid(phrase, False)
    count = countValid(phrases, fn)
    print(count) 

def part2():
    phrases = data(full=True)
    fn = lambda phrase: isValid(phrase, True)
    count = countValid(phrases, fn)
    print(count)

def isValid(phrase: list[str], sortWord: bool) -> bool:
    freq = defaultdict(int) 
    for word in phrase:
        if sortWord: word = sortedStr(word)
        freq[word] += 1
    return all(count == 1 for count in freq.values())

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Solve:
- For Part1, dont sort word; for Part2, sort word 
- Count valid phrases
- Phrase is valid if no word repeats: compute freq and check if all counts == 1
'''