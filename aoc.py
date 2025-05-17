from collections.abc import Callable
import time 

dims3  = tuple[int,int,int]

def toDims3(line: str, sep: str|None) -> dims3:
    a,b,c = [int(x) for x in line.split(sep)]
    return (a,b,c)

#####################################################################################

def getTotal(items: list, fn: Callable) -> int:
    total = 0 
    for item in items:
        total += fn(item)
    return total

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
