# Advent of Code 2015 Day 08
# John Roy Daradal 

import re
from aoc import *

def data(full: bool) -> list[str]:
    return readLines(15, 8, full)

def part1():
    words = data(full=True)
    fn = lambda text: len(text) - len(parseString(text))
    total = getTotal(words, fn)
    print(total)

def part2():
    words = data(full=True)
    fn = lambda text: len(expandString(text)) - len(text)
    total = getTotal(words, fn)
    print(total) 

hex = r'\\x[0-9a-f]{2}'
def parseString(text: str) -> str:
    text = text[1:-1]
    text = re.sub(hex, '.', text)
    text = text.replace('\\"', '"')
    text = text.replace('\\\\', '.')
    return text

def expandString(text: str) -> str:
    chars = []
    for x in text:
        if x == '"':
            chars.append('\\"')
        elif x == '\\':
            chars.append('\\\\')
        else:
            chars.append(x)
    return '"%s"' % ''.join(chars)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Sum up the differences between the length of original text and length of parsed text (compressed)
- To parse the string, remove the surrounding quotes and replace any hexadecimal chars with one char
- Also replace the escaped quote and backslash with one char

Part2:
- Sum up the differences between the length of the expanded text and length of original text
- To expand the string, add quotes around it; add other chars as-is
- If char is a quote or a backslash, add the escaped version
'''