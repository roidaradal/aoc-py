# Advent of Code 2022 Day 15
# John Roy Daradal 

from aoc import *

def data(full: bool) -> dict[coords, coords]: 
    sensors: dict[coords, coords] = {}
    remove = (',', ':', 'x=', 'y=')
    for line in readLines(22, 15, full):
        for r in remove:
            line = line.replace(r, '')
        p = line.split()
        sx, sy = int(p[2]), int(p[3])
        bx, by = int(p[-2]), int(p[-1])
        sensors[(sy,sx)] = (by,bx)
    return sensors

def solve() -> Solution:
    sensors = data(full=True)
    numSensors = len(sensors)

    # Part 1
    noBeacon: dict[int,list[int2]] = defaultdict(list)  # row => list of ranges
    goalRow = 2_000_000 
    i = 0
    for sensor, beacon in sensors.items():
        cfg = Config()
        cfg.sensor = sensor 
        cfg.beacon = beacon
        cfg.targetRow = goalRow
        computeNoBeacon(noBeacon, cfg)
        i += 1
        print('%d / %d' % (i, numSensors))
    items: set[int] = set()
    for x1,x2 in noBeacon[goalRow]:
        items = items.union(set(range(x1,x2)))
    for y,x in sensors.values(): # beacons 
        if y != goalRow: continue 
        if x in items: items.remove(x)
    count = len(items)

    # Part 2
    noBeacon: dict[int, list[int2]] = defaultdict(list)
    limit = 4_000_000
    i = 0
    for sensor, beacon in sensors.items():
        cfg = Config()
        cfg.sensor = sensor 
        cfg.beacon = beacon 
        cfg.minBounds = (0,0)
        cfg.maxBounds = (limit+1,limit+1)
        computeNoBeacon(noBeacon, cfg)
        i += 1
        print('%d / %d' % (i, numSensors))

    tuning = 0
    i, factor = 0, 100_000
    for y in noBeacon:
        i += 1 
        if i % factor == 0: print(i // factor)

        result = mergeRanges(noBeacon[y])
        if len(result) == 2:
            x = result[0][1]
            tuning = (x * 4_000_000) + y
            break

    return newSolution(count, tuning) 

class Config:
    def __init__(self):
        self.sensor: coords = (0,0)
        self.beacon: coords = (0,0)
        self.minBounds: dims2|None = None 
        self.maxBounds: dims2|None = None
        self.targetRow: int|None = None

def computeNoBeacon(noBeacon: dict[int,list[int2]], cfg: Config):
    radius = manhattan(cfg.sensor, cfg.beacon)
    sy,sx = cfg.sensor
    for dy in range(0, radius+1):
        options = [sy-dy, sy+dy] if dy > 0 else [sy]
        for ny in options:
            if cfg.targetRow != None and ny != cfg.targetRow: continue
            if cfg.minBounds != None and ny < cfg.minBounds[0]: continue
            if cfg.maxBounds != None and ny > cfg.maxBounds[0]: continue
            dx = radius - dy 
            nx1 = sx-dx 
            nx2 = sx+dx+1
            if cfg.minBounds != None: 
                nx1 = max(nx1, cfg.minBounds[1])
                nx2 = max(nx2, cfg.minBounds[1])
            if cfg.maxBounds != None:
                nx1 = min(nx1, cfg.maxBounds[1])
                nx2 = min(nx2, cfg.maxBounds[1])
            if nx1 >= nx2: continue # skip invalid range 
            noBeacon[ny].append((nx1, nx2))

if __name__ == '__main__':
    do(solve, 22, 15)

'''
Part1:
- For each sensor and its closest beacon, compute the noBeacon areas 
- Limit the computation to the target row = 2_000_000
- Count the unique columns with noBeacons in the target row 
- Make sure to remove the beacons in this row

Part2:
- For each sensor and its closest beacon, compute the noBeacon areas
- Clip the values for (x,y) from (0,0) to (4M, 4M)
- Check each row and merge the ranges of noBeacon areas:
    - Sort the ranges and process them by pairs 
    - If next range is a subset of the current range, skip 
    - If two ranges overlap, merge into one bigger range 
    - Otherwise, there is a gap in the range: close it and start a new one
- Almost all results end up with 1 resulting range (all noBeacon)
- If the result of the merge is 2 ranges = we have found the distress beacon:
  its position is the current row and the column for which the range was split
- Compute the tuning frequency: (x * 4M) + y

ComputeNoBeacon:
- The radius for the noBeacon area is the Manhattan distance of the sensor and its nearest beacon 
- The change in y (dy) ranges from 0 (for own row) up to radius
- Process both upward (sy-dy) and downward (sy+dy) areas
- If targetRow is set, skip the non-targetRow rows 
- If min/maxBounds are set, skip if the row is out-of-bounds 
- The radius width (horizontal) for this row is dx = radius - dy 
- Range from sx-dx (left) to sx+dx (right)
- If min/maxBounds are set, clip the range to fall within bounds 
- Skip invalid ranges 
- Add to the noBeacon area for this row the resulting column range
'''