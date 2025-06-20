# Advent of Code 2023 Day 05
# John Roy Daradal 

from aoc import * 

class Config: 
    def __init__(self):
        self.seeds = []
        self.maps  = {}
    
    @property 
    def seedRanges(self) -> list[int2]:
        s = self.seeds 
        return [(s[i], s[i]+s[i+1]-1) for i in range(0,len(s), 2)]

    @property
    def mapRanges(self) -> dict[str, list[int3]]:
        m = {}
        for key, items in self.maps.items():
            m[key] = []
            for src, dst, count in items:
                m[key].append((src, src+count-1, dst-src))
        return m

def data(full: bool) -> Config:
    cfg = Config()
    key = ''
    for line in readLines(23, 5, full):
        if line == '': continue 
        elif line.startswith('seeds:'):
            _, tail = splitStr(line, ':')
            cfg.seeds = toIntList(tail, None)
        elif line.endswith('map:'):
            key, _ = splitStr(line, None)
            cfg.maps[key] = []
        else:
            dst,src,count = toIntList(line, None)
            cfg.maps[key].append((src,dst,count))
    return cfg

def solve() -> Solution:
    cfg = data(full=True)

    # Part 1
    locations = applyMapChain(cfg)
    minLoc1 = min(locations)

    # Part 2 
    locations = applyMapRangeChain(cfg)
    minLoc2 = min(locations)

    return newSolution(minLoc1, minLoc2)

chain = ['seed','soil','fertilizer','water','light','temperature','humidity','location']

def applyMapChain(cfg: Config) -> list[int]:
    current = cfg.seeds 
    for i in range(len(chain)-1):
        key = '-to-'.join((chain[i],chain[i+1]))
        current = translate(current, cfg.maps[key])
    return current 

def translate(numbers: list[int], t: list[int3]) -> list[int]:
    result = []
    for x in numbers:
        y = x 
        for src,dst,count in t:
            if src <= x < src+count:
                y = dst + (x-src)
                break
        result.append(y)
    return result

def applyMapRangeChain(cfg: Config) -> list[int]:
    currRanges = cfg.seedRanges 
    rangeMap = cfg.mapRanges 
    for i in range(len(chain)-1):
        key = '-to-'.join((chain[i], chain[i+1]))
        nextRanges = []
        while len(currRanges) > 0:
            currRange = currRanges.pop(0)
            for start,end,diff in rangeMap[key]:
                ruleRange = (start,end)
                if isInside(ruleRange, currRange):
                    first, last = currRange
                    nextRanges.append((first+diff, last+diff))
                    break 
                match, extra = findIntersection(ruleRange, currRange)
                if match != None and extra != None:
                    first, last = match 
                    nextRanges.append((first+diff, last+diff))
                    currRanges.append(extra)
                    break
            else:
                nextRanges.append(currRange)
        currRanges = nextRanges
    return [x[0] for x in currRanges]

def isInside(ruleRange: int2, currRange: int2) -> bool:
    minValue, maxValue = ruleRange 
    start, end = currRange 
    return minValue <= start <= end <= maxValue 

def findIntersection(ruleRange: int2, currRange: int2) -> tuple[int2|None, int2|None]:
    minValue, maxValue = ruleRange 
    start, end = currRange 
    if minValue <= start <= maxValue:
        match, extra = (start, maxValue), (maxValue+1, end)
    elif minValue <= end <= maxValue:
        extra, match = (start, minValue-1), (minValue, end)
    else:
        match, extra = None, None
    return match, extra


if __name__ == '__main__':
    do(solve, 23, 5)

'''
Part1:
- Apply map chain by using the translation tables in order 
- Check the ranges in the translation table; if number falls in range, apply conversion
- If not found in ranges, number is not translated 
- In last set of numbers (location), return the start of ranges and get the minimum

Part2:
- Convert the seed list into seed ranges 
- Convert the maps into map ranges 
- Go through the translation tables in order, similar to Part 1
- Start with seed ranges as the first set of ranges 
- Go through the ranges and translate those that are inside a rule range or has intersection
- If part of a range doesn't fall inside a rule's range, add the extra range back to the queue
- Repeat until all ranges have been processed and proceed with the translated ranges for the next round
'''