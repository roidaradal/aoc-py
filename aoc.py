from collections.abc import Callable, Iterator
from collections import defaultdict
from typing import Any
from dotenv import load_dotenv
import time, hashlib, os, sys

load_dotenv()

coords = tuple[int,int]
int2   = tuple[int,int]
int3   = tuple[int,int,int]
int4   = tuple[int,int,int,int]
dims2  = tuple[int,int]
dims3  = tuple[int,int,int]
delta  = tuple[int,int]
strInt = tuple[str,int]
str2   = tuple[str,str]
str3   = tuple[str,str,str]
vector = tuple[coords,delta]
IntGrid = list[list[int]]
Solution = tuple[str,str]

def toDims2(line: str, sep: str|None) -> dims2:
    a,b = [int(x.strip()) for x in line.split(sep)]
    return (a,b)

def toDims3(line: str, sep: str|None) -> dims3:
    a,b,c = [int(x.strip()) for x in line.split(sep)]
    return (a,b,c)

def toInt2(line: str, sep: str|None) -> int2:
    a,b = [int(x.strip()) for x in line.split(sep)]
    return (a,b)

def toStr2(line: str, sep: str|None) -> str2:
    a, b = splitStr(line, sep)
    return (a, b)

def toStrInt(line: str, strLen: int) -> strInt:
    line = line.strip() 
    return (line[:strLen], int(line[strLen:]))

def lineStrInt(line: str, sep: str|None) -> strInt:
    a,b = [x.strip() for x in line.split(sep)]
    return (a, int(b))

def toIntList(line: str, sep: str|None) -> list[int]:
    return [int(x.strip()) for x in line.split(sep)]

def toIntLine(line: str) -> list[int]:
    return [int(x) for x in line]

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

def argmax(items: list[int]) -> int:
    # -index for tie-breaker: choose earlier index first 
    return max((x,-i) for i,x in enumerate(items))[1] * -1

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

def binaryFilled(x: int, fill: int) -> str:
    return bin(x)[2:].zfill(fill)

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

def tryParseInt(x: str) -> int|str:
    try: 
        y = int(x)
        return y
    except ValueError:
        return x
    
def cmp(a: int, b: int) -> int:
    if a < b:
        return -1
    elif a > b:
        return 1 
    else:
        return 0
    
def mergeRanges(ranges: list[int2]) -> list[int2]:
    ranges.sort()
    result: list[int2] = []
    currStart, currEnd = ranges[0]
    for nextStart, nextEnd in ranges[1:]:
        if currStart <= nextStart and nextEnd <= currEnd: continue # subset 

        if nextStart <= currEnd: # overlap
            currEnd = nextEnd 
        else:
            result.append((currStart, currEnd))
            currStart, currEnd = nextStart, nextEnd
    result.append((currStart, currEnd))
    return result

def findCloser(pattern: str, start: int) -> int:
    # Start = index of ( so start at next char to avoid incrementing the opener
    i, limit = start+1, len(pattern)
    depth = 0
    while i < limit:
        char = pattern[i]
        if char == '(':
            depth += 1
        if char == ')':
            if depth == 0:
                break
            else:
                depth -= 1
        i += 1
    return i

#####################################################################################

U: delta = (-1,0)
D: delta = (1,0)
L: delta = (0,-1)
R: delta = (0,1)
X: delta = (0,0)
NW: delta = (-1,-1)
NE: delta = (-1,1)
SW: delta = (1,-1)
SE: delta = (1,1)

leftOf:  dict[delta,delta] = {
    U: L, L: D, D: R, R: U, X: X,
    NE: NW, NW: SW, SW: SE, SE: NE,
}
rightOf: dict[delta,delta] = {
    U: R, R: D, D: L, L: U, X: X,
    NE: SE, SE: SW, SW: NW, NW: NE,
}

def createGrid(initial: Any, numRows: int, numCols: int) -> list[list]:
    return [[initial for _ in range(numCols)] for _ in range(numRows)]

def getBounds(grid: list) -> dims2:
    return (len(grid), len(grid[0]))

def move(c: coords, d: delta) -> coords:
    (row,col),(dy,dx) = c, d
    return (row+dy, col+dx)

def repeatMove(c: coords, d: delta, r: int) -> coords:
    for _ in range(r): c = move(c, d)
    return c

def getDelta(c1: coords, c2: coords) -> delta:
    (y1,x1), (y2,x2) = c1, c2 
    return (y2-y1, x2-x1)

def manhattan(c1: coords, c2: coords=(0,0)) -> int:
    (y1,x1),(y2,x2) = c1, c2
    return abs(y2-y1) + abs(x2-x1)

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

def surround4(c: coords) -> list[coords]:
    row,col = c
    return [
                       (row-1,col-0), 
        (row-0,col-1),                (row-0,col+1),
                       (row+1,col-0),
    ]
#####################################################################################

def do(fn: Callable, year: int, day: int):
    args = sys.argv[1:]
    testMode = len(args) > 0 and args[0] == 'test'
    
    start = time.time()
    ans1, ans2 = fn()

    if testMode:
        sol1, sol2  = getSolution(year, day)
        if ans1 == sol1:
            print('OK1:', ans1)
        else:
            print('Part1: Exp vs Got:\n%s\n%s' % (sol1, ans1))
        if ans2 == sol2:
            print('OK2:', ans2)
        else:
            print('Part2: Exp vs Got:\n%s\n%s' % (sol2, ans2))
    else:
        print(ans1)
        print(ans2)

    duration = time.time() - start 
    print('\nTime: %.2fs' % duration)


def rootDir():
    root = os.getenv('AOC_DATA_DIR')
    if root is None:
        root = '../aoc-data'
    return root

def readLines(year: int, day: int, full: bool, strip: bool = True) -> list[str]:
    folder = '20%d' % year if full else 'test'
    path = '%s/%s/%d%.2d.txt' % (rootDir(), folder, year, day)
    f = open(path, 'r')
    lines = [x.strip() if strip else x for x in f.readlines()]
    f.close()
    return lines 

def readFirstLine(year: int, day: int, full: bool, strip: bool = True) -> str:
    return readLines(year, day, full, strip)[0]

def getSolution(year: int, day: int) -> Solution:
    path = '%s/solutions/all.csv' % rootDir()
    f = open(path, 'r')
    lines = [x.strip() for x in f.readlines()]
    f.close()
    solution: dict[str,Solution] = {}
    for line in lines:
        p = line.split('|')
        k = p[0] + p[1]
        v = (p[2], p[3])
        solution[k] = v
    key = '%d%.2d' % (year, day)
    return solution[key]

def newSolution(part1: Any, part2: Any) -> Solution:
    sol1 = str(part1)
    sol2 = str(part2)
    return (sol1, sol2)