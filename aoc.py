from collections.abc import Callable, Iterator
from collections import defaultdict
import time, hashlib

coords = tuple[int,int]
dims3  = tuple[int,int,int]
delta  = tuple[int,int]

def toDims3(line: str, sep: str|None) -> dims3:
    a,b,c = [int(x) for x in line.split(sep)]
    return (a,b,c)

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

def charFreq(word: str, skip: list|None = None) -> defaultdict[str,int]:
    freq: defaultdict[str,int] = defaultdict(int)
    for char in word:
        if skip != None and char in skip:
            continue
        freq[char] += 1
    return freq

def hasTwins(word: str, gap: int = 0) -> bool:
    back = gap+1
    for i in range(back, len(word)):
        if word[i] == word[i-back]:
            return True 
    return False

def substringPositions(word: str, length: int) -> defaultdict[str,list[int]]:
    at = defaultdict(list)
    for i in range(len(word)-(length-1)):
        sub = word[i:i+length]
        at[sub].append(i)
    return at

#####################################################################################

U: delta = (-1,0)
D: delta = (1,0)
L: delta = (0,-1)
R: delta = (0,1)

def move(c: coords, d: delta) -> coords:
    (row,col),(dy,dx) = c, d
    return (row+dy, col+dx)

# Returns ending position and set of visited coords (with frequency of visit)
def walk(moves: list[delta], start: coords = (0,0),  visitStart: bool = True) -> tuple[coords,dict[coords,int]]:
    visited = defaultdict(int)
    if visitStart: visited[start] = 1 
    curr = start
    for d in moves:
        curr = move(curr, d)
        visited[curr] += 1 
    return (curr, visited)

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
