# Advent of Code 2022 Day 03
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    return readLines(22, 3, full)

def part1():
    words = data(full=True)
    total = getTotal(words, commonScore) 
    print(total)

def part2():
    words = data(full=True)
    groups = [words[i:i+3] for i in range(0, len(words), 3)]
    total = getTotal(groups, badgeScore)
    print(total) 

def score(char: str) -> int:
    v = ord(char)
    if 97 <= v <= 122: # a-z: 1-26
        return v - 96
    elif 65 <= v <= 90: # A-Z: 27-52
        return v - 38
    return 0

def commonScore(word: str) -> int:
    mid = len(word) // 2 
    chars = set()
    for i, char in enumerate(word):
        if i < mid:
            chars.add(char)
        elif char in chars:
            return score(char)
    return 0
        
def badgeScore(words: list[str]) -> int:
    common = set(words[0])
    for word in words[1:]:
        uncommon = set(common)
        for char in word:
            if char in uncommon: uncommon.remove(char)
        for char in uncommon:
            common.remove(char)
    badge = tuple(common)[0]
    return score(badge)
    

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Find the common char in first half and second half of the word
- In first half (i < mid), add encountered chars to a set 
- In second half, if char encountered in first half, return its score
- To compute char score, map a-z to 1-26 and A-Z to 27-52 by using ord and adjusting the value

Part2:
- Group words by 3s 
- Start with the word1's chars as the common set 
- Go through other words in order, each time finding the uncommon chars from the current common set
- Remove the uncommon chars from the common set, reducing it each round
- In the end you are left with one item in the common set, return its score
'''