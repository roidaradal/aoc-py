# Advent of Code 2015 Day 05
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> list[str]:
    return readLines(15, 5, full)

def solve() -> Solution:
    words = data(full=True)

    # Part 1
    count1 = countValid(words, isNice)

    # Part 2 
    count2 = countValid(words, isNice2)
    
    return newSolution(count1, count2)

invalid = ('ab','cd','pq','xy')
vowels = 'aeiou'

def isNice(word: str) -> bool:
    # Check if contains any of the invalid substrings
    if any(x in word for x in invalid): 
        return False 
    
    # Check if has letter that appears twice in a row (aa)
    if not hasTwins(word):
        return False 

    # Check if has at least 3 vowels
    freq = charFreq(word)
    numVowels = sum(freq[v] for v in vowels)
    return numVowels >= 3

def isNice2(word: str) -> bool:
    # Check if contains letter which repeats with one letter between them (e.g. axa)
    if not hasTwins(word, gap=1):
        return False
    
    # Check if has pair of two letters that appears >= 2 with no overlap
    pairs = substringGroups(word, 2)
    for idxs in pairs.values():
        if len(idxs) >= 3:
            return True 
        elif len(idxs) ==2 and abs(idxs[0]-idxs[1]) >= 2:
            # if only two indexes, make sure has gap of at least 2
            return True    
    return False

def substringGroups(word: str, length: int) -> dict[str,list[int]]:
    at: dict[str,list[int]] = defaultdict(list)
    for i in range(len(word)-(length-1)):
        sub = word[i:i+length]
        at[sub].append(i)
    return at

if __name__ == '__main__':
    do(solve, 15, 5)

'''
Part1:
- Check if word contains any of invalid substrings (ab, cd, pq, xy)
- Check if word has letter that appears twice in a row (e.g. aa, bb)
- Check if word has at least 3 vowels 

Part2:
- Check if contains letter which repeats with one letter between them
- Check if has pair of two letters that appears >= 2 with no overlap
    - Group the pairs' indexes 
    - If pair has at least 3 indexes, valid 
    - If pair only has 2 indexes, check that index difference is at least 2 (no overlap)
'''