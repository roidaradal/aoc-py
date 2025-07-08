# Advent of Code 2020 Day 19
# John Roy Daradal 

import re
from functools import reduce
from aoc import *

Grammar = dict[str, list[list[str]]]

def data(full: bool) -> tuple[Grammar, str2, list[str]]:
    wordMode = False 
    grammar: Grammar = {}
    a, b = '', ''
    words: list[str] = []
    for line in readLines(20, 19, full):
        if line == '':
            wordMode = True 
        elif wordMode:
            words.append(line)
        else:
            key, tail = splitStr(line, ':')
            if tail == '"a"':
                a = key
            elif tail == '"b"':
                b = key
            else:
                rules = splitStr(tail, '|')
                grammar[key] = [r.split() for r in rules]
    return grammar, (a,b), words

def solve() -> Solution:
    grammar, (a,b), words = data(full=True)
    counts: list[int] = []
    for override in [False, True]:
        T = createTranslator(grammar, a, b, override)

        pattern = f'^{T["0"]}$'
        def isMatch(x: str) -> bool:
            result = re.match(pattern, x)
            return result != None and result.group(0) == x
        
        counts.append(countValid(words, isMatch))
    
    count1, count2 = counts
    return newSolution(count1, count2)

def createTranslator(grammar: Grammar, a: str, b: str, override: bool) -> dict[str,str]:
    T: dict[str,str] = {a: 'a', b: 'b'}
    incomplete = list(grammar.keys())
    while len(incomplete) > 0:
        ready: list[str] = []
        for key in incomplete:
            deps = set(reduce(lambda x,y: x + y, grammar[key]))
            if all(dep in T for dep in deps):
                ready.append(key)
        for key in ready:
            updateGrammar(T, key, grammar[key])
            incomplete.remove(key)

    if override: # For Part 2 
        re42 = T['42']
        re31 = T['31']
        re8  = f'({re42}+)' # one or more of re42
        options = [re42+re31]
        for r in range(2, 6): # repeat 2-5x 
            option = '((%s){%d}(%s){%d})' % (re42, r, re31, r) # 42n31n
            options.append(option)
        re11 = '(' + '|'.join(options) + ')'
        T['8'] = re8
        T['11'] = re11
        T['0'] = re8 + re11

    return T

def updateGrammar(T: dict[str,str], key: str, rules: list[list[str]]):
    options: list[str] = []
    for rule in rules:
        option: list[str] = []
        for k in rule:
            rep = T[k]
            option.append(rep)
        fullOption = ''.join(option)
        options.append(fullOption)
    T[key] = '(' + '|'.join(options) + ')'

if __name__ == '__main__':
    do(solve, 20, 19)

'''
Solve:
- Read the grammar from the input data, identify which rules produce the literals "a" and "b"
- Replace the rules with regular expressions by creating the translator
    - Start with rules for a and b in the translator 
    - Check which rules are ready for translation, by checking that all its parts / dependencies are already in the translator 
    - Update the translator by replacing the ready rules with their translated values
    - If multiple options, separate by | for the regex; wrap with () to indicate grouping
- For Part 2, override the grammar with the changes:
    - 8 -> 42 becomes 8 -> 42 8 => 42+
        - Just replace rule 8 by (re42+) - one or more of re42
    - 11 -> 42 31 becomes 11 -> 42 11 31 => 42n31n 
        - Expand the pattern manually by adding 42 31, 42{2}31{2}, 42{3}31{3}, etc
        - Do this for repeat=1 to 5, then join the options by |
- The final regexp pattern is T[0] wrapped in ^ and $ (start, end)
- Count which among the words is a full match on the final pattern
'''