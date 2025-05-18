# Advent of Code 2018 Day 05
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readLines(18, 5, full)[0]

def part1():
    word = data(full=True)
    word = fullyCompress(word)
    print(len(word)) 

def part2():
    word = data(full=True)
    chars = set(char.lower() for char in word) 
    numChars = len(chars)
    minLength = float('inf')
    for i,char in enumerate(chars):
        word2 = ''.join(x for x in word if x.lower() != char)
        word2 = fullyCompress(word2)
        wordLen = len(word2)
        print('%.2d / %.2d - %s - %d' % (i+1, numChars, char, wordLen))
        minLength = min(minLength, wordLen)
    print(minLength)

def fullyCompress(word: str) -> str:
    ok = True 
    while ok:
        word, ok = compress(word)
    return word 

def compress(word: str) -> tuple[str,bool]:
    for i in range(len(word)-1):
        x, y = word[i], word[i+1]
        if x != y and x.lower() == y.lower():
            word = word[:i] + word[i+2:]
            return (word, True)
    return (word, False)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Foreach character pair in word, check if it has form Aa or aA 
- Compress by removing that pair from the word
- Repeatedly compress until no more changes made

Part2:
- Get the unique lowercase letters in the word 
- For each letter: form a new word by removing all instances of that letter (upper/lowercase)
- Find the minimum compressed word length resulting from the words produced by removing each letter
- Note: This solution takes around 5 minutes to finish (checks 26 letters)
'''