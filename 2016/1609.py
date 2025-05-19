# Advent of Code 2016 Day 09
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readLines(16, 9, full)[0]

def solve():
    word = data(full=True)
    size1 = decompressLength(word, True)
    print(size1) 
    size2 = decompressLength(word, False)
    print(size2)

def decompressLength(word: str, skip: bool) -> int:
    i, wordLen = 0, len(word)
    count = [1 for _ in range(wordLen)]
    while i < wordLen:
        if word[i] != '(':
            i += 1
            continue
        # Found (
        end = word.find(')', i)
        size, repeat = toIntList(word[i+1:end], 'x')
        start = end+1
        for j in range(i, start):
            count[j] = 0
        for j in range(start, start+size):
            count[j] *= repeat
        if skip: 
            i = start+size  # go to char after repeated substring
        else:
            i = end+1       # go to char after marker ()
    return sum(count)
        

if __name__ == '__main__':
    do(solve)

'''
Solve:
- For Part 1, skip over the whole repeated substring; continue to char after it 
- For Part 2, continue after the marker (), possibly processing other markers that were part of a repeated substring
- Start with count of each word position initialized to 1
- Go through the characters of the word; if not ( skip over it
- If opening for marker ( is found, find it's corresponding closing )
- Get the size of the substring to process and no. of times to repeat 
- Remove the markers count by settings its region to 0
- Starting from after ) up to the size indicated for the substring, multiply the characters by the repeat factor
- For Part 1, since we are skipping the whole repeated substring, go to the char after it 
- For Part 2, since we are processing all markers, go to the char after )
'''