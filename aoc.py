from collections.abc import Callable, Iterator
from collections import defaultdict
from typing import Any
import time, hashlib

coords = tuple[int,int]
int2   = tuple[int,int]
int3   = tuple[int,int,int]
dims2  = tuple[int,int]
dims3  = tuple[int,int,int]
delta  = tuple[int,int]
strInt = tuple[str,int]

def toDims2(line: str, sep: str|None) -> dims2:
    a,b = [int(x) for x in line.split(sep)]
    return (a,b)

def toDims3(line: str, sep: str|None) -> dims3:
    a,b,c = [int(x) for x in line.split(sep)]
    return (a,b,c)

def toInt2(line: str, sep: str|None) -> int2:
    a,b = [int(x) for x in line.split(sep)]
    return (a,b)


def toStrInt(line: str, strLen: int) -> strInt:
    line = line.strip() 
    return (line[:strLen], int(line[strLen:]))

def toIntList(line: str, sep: str|None) -> list[int]:
    return [int(x) for x in line.split(sep)]

#####################################################################################

def getTotal(items: list, fn: Callable) -> int:
    total = 0 
    for item in items:
        total += fn(item)
    return total

def countValid(items: list, fn: Callable) -> int:
    count = 0 
    for item in items:
        if fn(item):
            count += 1 
    return count

#####################################################################################

def md5Hash(word: str) -> str:
    return hashlib.md5(word.encode('utf-8')).hexdigest()

def md5HashGenerator(key: str, goal: str, start: int) -> Iterator:
    i = start
    while True:
        word = '%s%d' % (key, i)
        hash = md5Hash(word)
        if hash.startswith(goal):
            yield (i, hash)
        i += 1

#####################################################################################

def sortedStr(word: str) -> str: 
    return ''.join(sorted(word))

def charFreq(word: str, skip: list|None = None) -> defaultdict[str,int]:
    freq: defaultdict[str,int] = defaultdict(int)
    for char in word:
        if skip != None and char in skip:
            continue
        freq[char] += 1
    return freq

def countFreq(items: list) -> dict:
    freq = defaultdict(int)
    for item in items:
        freq[item] += 1
    return freq

def hasTwins(word: str, gap: int = 0) -> bool:
    back = gap+1
    for i in range(back, len(word)):
        if word[i] == word[i-back]:
            return True 
    return False

def splitStr(word: str, sep: str|None) -> list[str]:
    return [x.strip() for x in word.split(sep)]

def groupChunks(word: str) -> list[str]:
    chunks = []
    curr, count = word[0], 1
    for i in range(1, len(word)):
        char = word[i]
        if char == curr: 
            count += 1
        else: 
            chunks.append(curr * count) # repeat string 
            curr, count = char, 1 
    chunks.append(curr * count)
    return chunks

#####################################################################################

U: delta = (-1,0)
D: delta = (1,0)
L: delta = (0,-1)
R: delta = (0,1)

leftOf:  dict[delta,delta] = {U: L, L: D, D: R, R: U}
rightOf: dict[delta,delta] = {U: R, R: D, D: L, L: U}

def createGrid(initial: Any, numRows: int, numCols: int) -> list[list]:
    return [[initial for _ in range(numCols)] for _ in range(numRows)]

def getBounds(grid: list) -> dims2:
    return (len(grid), len(grid[0]))

def move(c: coords, d: delta) -> coords:
    (row,col),(dy,dx) = c, d
    return (row+dy, col+dx)

def manhattan(c: coords) -> int:
    return sum(abs(x) for x in c)

def insideBounds(c: coords, maxBounds: dims2, minBounds: dims2 = (0,0)) -> bool:
    row, col = c 
    minRows, minCols = minBounds
    numRows, numCols = maxBounds 
    return minRows <= row < numRows and minCols <= col < numCols

def surround8(c: coords) -> list[coords]:
    row,col = c 
    return [
        (row-1,col-1), (row-1,col-0), (row-1,col+1),
        (row-0,col-1),                (row-0,col+1),
        (row+1,col-1), (row+1,col-0), (row+1,col+1),
    ]

#####################################################################################

def do(fn: Callable):
    start = time.time()
    fn()
    duration = time.time() - start 
    print('\nTime: %.2fs' % duration)
    print('-----' * 5)

def readLines(year: int, day: int, full: bool, strip: bool = True) -> list[str]:
    folder = 'data' if full else 'test'
    path = '%s/%d%.2d.txt' % (folder, year, day)
    f = open(path, 'r')
    lines = [x.strip() if strip else x for x in f.readlines()]
    f.close()
    return lines 
