# Advent of Code 2015 Day 19
# John Roy Daradal 

import re
from aoc import *

Converter = dict[str,list[str]]

def data(full: bool) -> tuple[str, Converter]:
    readWord = False 
    word = ''
    T: Converter = defaultdict(list)
    for line in readLines(15, 19, full):
        if line == '':
            readWord = True 
        elif readWord:
            word = line 
        else: 
            k,v = splitStr(line, '=>')
            T[k].append(v)
    return word, T

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    word, T = data(full=True)
    results: set[str] = set()
    for substring, replacements in T.items():
        for match in re.finditer(substring, word):
            start, end = match.start(), match.end() 
            results = results.union(replaceAll(word, start, end, replacements))
    return len(results) 

def part2() -> int:
    word, T = data(full=True)
    # analyzeGrammar(T)

    rep = createReverse(T)
    # analyzeReverse(rep)

    return greedyReplace(word, rep)
    
def replaceAll(word: str, start: int, end: int, replacements: list[str]) -> set[str]:
    head, tail = word[:start], word[end:]
    results: set[str] = set()
    for mid in replacements:
        results.add(f"{head}{mid}{tail}")
    return results

def analyzeGrammar(T: Converter):
    elements: set[str] = set(T.keys())
    for k, replacements in T.items():
        print(k.ljust(5), ' | '.join(replacements))
        for chemical in replacements:
            elements = elements.union(breakdown(chemical))
            
    print('\nElements:', len(elements))
    nothing = 0
    for e in sorted(elements): 
        if e not in T: 
            print(e)
            nothing += 1
    print('Produces nothing:', nothing)

def breakdown(chemical: str) -> set[str]:
    elements: set[str] = set()
    curr = [chemical[0]]
    for nxt in chemical[1:]:
        if nxt.isupper():
            elements.add(''.join(curr))
            curr = [nxt]
        else:
            curr.append(nxt)
    elements.add(''.join(curr))
    return elements

def createReverse(T: Converter) -> Converter:
    rep: Converter = defaultdict(list)
    for element, replacements in T.items():
        for substring in replacements:
            rep[substring].append(element)
    return rep

def analyzeReverse(rep: Converter):
    for k in sorted(rep.keys(), key=countElements):
        print(k.ljust(10), rep[k])
    
    substrings = list(rep.keys())
    overlap = 0
    for sub1 in substrings:
        for sub2 in substrings:
            if sub1 == sub2: continue 
            if sub1 in sub2: # substring 
                print('Overlap: %s in %s' % (sub1, sub2))
                overlap += 1
    print('Total:', overlap)

def greedyReplace(word: str, rep: Converter):
    steps = 0
    while True:
        replaced = False 
        keyFn = lambda sub: lookaheadReplace(sub, word, rep)
        for sub in sorted(rep.keys(), key=keyFn, reverse=True):
            if sub in word:
                word = word.replace(sub, rep[sub][0], 1)
                replaced = True 
                break
        if replaced:
            steps += 1
        else: 
            break
    return steps if word == 'e' else 0

def countElements(chemical: str) -> int:
    return sum(1 for x in chemical if x.isupper())

def countReplaceable(word: str, rep: Converter) -> int:
    return sum(1 for sub in rep if sub in word)

def lookaheadReplace(sub: str, word: str, rep: Converter) -> int:
    if sub not in word: return 0 
    word2 = word.replace(sub, rep[sub][0], 1)
    return countReplaceable(word2, rep)


if __name__ == '__main__':
    do(solve, 15, 19)

'''
Part1:
- Go through all (substring, list of replacements) from the converter table 
- Find all instances of the substring in the word
- Replace all instances of the substring with all possible replacements 
- Count the total unique resulting words

Part2 (Initial Solution - Grammar Based):
- Analyzing the grammar, there are 4 elements that don't produce anything: C, Y, Ar, Rn
- However, C can be spared because there is a Ca element
- Further checking of the grammar reveals that productions are of the form:
    - X => YZ , X => XY, X => XX, X => YX, X => YY
    - except for when Ar, Rn are involved: X => Y(Z), where Ar and Rn looks like parentheses 
    - except for when Y is involved: X => Y(Z,Z), where X looks like a comma
- Elements in the molecule are either capital letters (A) or capital letter with a lowercase (Ab)
- There is a solution that counts the steps directly from the grammar properties:
    number of elements = count of upper case letters ()
    elements - countRn - countAr - 2*countY - 1
- Used this initially to get the correct solution for 2 test cases, and check that the greedy
   solution below produces the correct results for both cases

Part 2:
- Create the reverse converter: from the replacement to the element
- Analyzing the reverse converter, we see that each replacement maps to exactly one element 
- There are also no overlaps in the replacement substrings, so we can be confident that there 
  is a definite replacement order that doesn't involve checking many possibilities
- Greedy approach: go through the replacements in descending order of the sorting function:
    - Find the first replacement that is a substring of the current word 
    - Replace the first instance of that substring with its element (there is only one)
    - Count the steps until we can no longer find a replacement in the current word 
- Double check that the final word is 'e'
- Greedy heuristic for substring replacements: lookahead count replaceable 
    - If the substring is not in the word, return 0 (no priority)
    - Lookahead by performing the replacement of the first instance of this substring by its equivalent element 
    - Count the replaceable substrings in the resulting word
    - Idea: we are looking for the substring that will maximize the number of replaceable substrings in the next round 
    - By doing so, we avoid the substrings that lead to dead-end or fewer replacements
'''