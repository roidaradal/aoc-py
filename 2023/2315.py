# Advent of Code 2023 Day 15
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str]:
    line = readFirstLine(23, 15, full)
    return splitStr(line, ',')

def solve() -> Solution:
    words = data(full=True)

    # Part 1 
    total1 = getTotal(words, hash256)

    # Part 2
    box: dict[int, list[strInt]] = defaultdict(list)
    hashOf: dict[str, int] = {}
    for word in words:
        if word.endswith('-'):
            label = word[:-1]
            if label not in hashOf:
                hashOf[label] = hash256(label)
            idx = hashOf[label]
            results = [i for i,(name,_) in enumerate(box[idx]) if name == label]
            if len(results) == 1:
                i = results[0]
                del box[idx][i]
        elif '=' in word:
            label,size = splitStr(word, '=')
            size = int(size)
            if label not in hashOf:
                hashOf[label] = hash256(label)
            idx = hashOf[label]
            results = [i for i,(name,_) in enumerate(box[idx]) if name == label]
            if len(results) == 1:
                i = results[0]
                box[idx][i] = (label, size)
            else:
                box[idx].append((label, size))
    total2 = 0
    for b in box:
        for i,(_, size) in enumerate(box[b]):
            total2 += (b+1) * (i+1) * size
 
    return newSolution(total1, total2)

def hash256(word: str) -> int:
    curr = 0 
    for letter in word:
        curr += ord(letter)
        curr *= 17 
        curr %= 256
    return curr

if __name__ == '__main__':
    do(solve, 23, 15)

'''
Solve:
- Hash256 of a word goes through each letter:
    - Add to the current total the letter's ASCII code 
    - Multiply by 17 and modulo by 256
- For Part 1, get the total when applying hash256 to the input words
- For Part 2, process the words as commands
- Idea: implementation of a HashMap 
- Cache the results of hashing the label, to avoid recomputation
- If subtract command (cmd-), get the hash of the cmd label => box index
    - In the box of the computed key, find the cmd if it exists 
    - Remove the item from the box if found
- If equals command (cmd=x), get the hash of the cmd label => box index 
    - In the box of the computed key, check if the cmd exists 
    - If already existing, replace the item with the new value x 
    - If not yet in the box, add to the end of the box
- To compute the focusing power, go through each box:
    - Go through each (label, size) in the box
    - Add up the box index (1-based) x item index (1-based) x size
'''