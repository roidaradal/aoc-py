# Advent of Code 2016 Day 14
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readFirstLine(16, 14, full)

def solve() -> Solution:
    word = data(full=True)
    limit = 64 
    values = []
    # Part 1 and 2
    for hashFn in [hashFn1, hashFn2]:
        keys = []
        hashOf = {}
        i = -1
        while len(keys) != limit:
            i += 1
            if i not in hashOf:
                hashOf[i] = hashFn(word, i)
            letter = findTriple(hashOf[i])
            if letter == '': continue 
            goal = letter * 5 
            for j in range(1000):
                k = i + j + 1
                if k not in hashOf:
                    hashOf[k] = hashFn(word, k)
                if goal in hashOf[k]:
                    keys.append(i)
                    break 
        values.append(keys[-1])
    return newSolution(values[0], values[1])

def findTriple(h: str) -> str:
    curr, count = '', 0 
    for x in h:
        if x != curr:
            curr = x 
            count = 1 
        else:
            count += 1
            if count == 3: return curr 
    return ''          

def hashFn1(word: str, i: int) -> str:
    return md5Hash('%s%d' % (word, i))

def hashFn2(word: str, i: int) -> str:
    word = hashFn1(word, i)
    for _ in range(2016):
        word = md5Hash(word)
    return word

if __name__ == '__main__':
    do(solve, 16, 14)

'''
Solve: 
- Find the 64th valid key
- Memoize the hashOf[index] so we dont need to recompute when looking at the next 1000 hashes
- For the current hash, find a triple consecutive letter; skip that hash if no such triple exists
- If a triple exists, check if there is a hash in the next 1000 hashes that contains as substring
  that letter repeated 5x consecutively
- If this is satisfied, the current index is added to the keys
- Output the 64th key index
- For Part 1, the hashFn simply gets the MD5 Hash of the concatenated word and the index 
- For Part 2, it computes the hash produced by hashFn1 and repeatedly applies md5Hash 2016 times
'''