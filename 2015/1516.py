# Advent of Code 2015 Day 16
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[dict[str,int]]:
    def fn(line: str) -> dict[str,int]:
        tail = line.split(':', 1)[1].strip()
        d: dict[str,int] = {}
        for pair in splitStr(tail, ','):
            k ,v = splitStr(pair, ':')
            d[k] = int(v)
        return d
    return [fn(line) for line in readLines(15, 16, full)]

def solve() -> Solution:
    aunts = data(full=True)
    aunt1, aunt2 = 0, 0

    for i, aunt in enumerate(aunts):
        # Part 1
        if aunt1 == 0 and isMatch(aunt):
            aunt1 = i+1 

        # Part 2 
        if aunt2 == 0 and isMatch2(aunt):
            aunt2 = i+1 
        
        if aunt1 != 0 and aunt2 != 0:
            break 
    
    return newSolution(aunt1, aunt2)
        
goal: dict[str,int] = {
    'children'      : 3, 
    'cats'          : 7,
    'samoyeds'      : 2,
    'pomeranians'   : 3, 
    'akitas'        : 0,
    'vizslas'       : 0, 
    'goldfish'      : 5, 
    'trees'         : 3, 
    'cars'          : 2, 
    'perfumes'      : 1,
}

def isMatch(aunt: dict[str,int]) -> bool:
    for k,v in aunt.items():
        if goal[k] != v: return False 
    return True 

def isMatch2(aunt: dict[str,int]) -> bool:
    for k,v in aunt.items():
        if k in ('cats','trees'):
            if v <= goal[k]: return False 
        elif k in ('pomeranians', 'goldfish'):
            if v >= goal[k]: return False 
        else:
            if goal[k] != v: return False
    return True 

if __name__ == '__main__':
    do(solve, 15, 16)

'''
Solve:
- For Part 1 and 2, use the isMatch and isMatch2 functions to find the aunt who 
  gave the gift; once the 2 aunts are found, exit out of the loop 
- isMatch: check if all known key, value of aunt matches the goal; if any mismatch, it's not this aunt 
- isMatch2: check all key, value of aunt:
    - if key = cats|trees and value <= goal, fail
    - if key = pomeranians|goldifsh and value >= goal, fail
    - otherwise, check if value matches goal, if not: fail
'''