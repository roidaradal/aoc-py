# Advent of Code 2015 Day 12
# John Roy Daradal 

import re, json
from aoc import *

def data(full: bool) -> str:
    return readFirstLine(15, 12, full)

def solve() -> Solution:
    text = data(full=True)

    # Part 1 
    total1 = sumNumbers(text)

    # Part 2
    items = json.loads(text)
    total2 = sumItems(items)

    return newSolution(total1, total2)

def sumNumbers(text: str) -> int:
    pattern = r'\-?[0-9]+'
    matches = re.findall(pattern, text)
    total = getTotal(matches, int)
    return total

def sumItems(items: list|dict) -> int:
    total = 0 
    if type(items) == list:
        for x in items:
            t = type(x)
            if t == int:
                total += x 
            elif t == dict or t == list:
                total += sumItems(x)
    elif type(items) == dict:
        for v in items.values():
            t = type(v)
            if t == str and v == 'red':
                return 0
            elif t == int:
                total += v 
            elif t == dict or t == list:
                total += sumItems(v)
    return total

if __name__ == '__main__':
    do(solve, 15, 12)

'''
Part1:
- Use regexp to find number patterns in the text 
- Convert these to ints and output the total

Part2:
- Load the text as a JSON object and get the total of the object 
- If items is a list, go through each item in the list:
    - If item is integer, add to total
    - If item is list or dict, recursively call sumItems on it 
- If items is a dictionary, go through the values:
    - If value is 'red', the value for the whole object is 0 
    - If value is integer, add to total 
    - If value is list or dict, recursively call sumItems on it
'''