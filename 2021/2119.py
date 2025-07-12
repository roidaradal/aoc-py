# Advent of Code 2021 Day 19
# John Roy Daradal 

from aoc import *

def data(full: bool) -> dict[int, list[int3]]:
    scanners: dict[int, list[int3]] = {}
    key = 0
    for line in readLines(21, 19, full):
        if line == '': 
            continue 
        elif line.startswith('---'):
            line = line.strip('-').strip()
            key = int(line.split()[1])
            scanners[key] = []
        else:
            x,y,z = toIntList(line, ',')
            scanners[key].append((x,y,z))
    for key in scanners:
        scanners[key] = sorted(scanners[key])
    return scanners

def solve() -> Solution:
    scans = data(full=True)

    # Part 1
    pending = [k for k in scans.keys() if k != 0]

    # Generate 24 versions of each scanner 
    orientations = generateOrientations()
    versions: dict[int, dict[int, list[int3]]] = {}
    for k in pending: 
        versions[k] = generateVersions(scans[k], orientations)

    # Generate 3D cube, initialized by scan0 points
    cube: list[int3] = []
    for t in scans[0]:
        cube.append(t)

    # List of scanner positions
    scanners: list[int3] = [(0,0,0)]

    while len(pending) > 0:
        remove = []
        for k in pending:
            for scan in versions[k].values():
                diffs: dict[int3, int] = defaultdict(int)
                for t in cube:
                    for s in scan:
                        diffs[getDiff(t, s)] += 1
                diffCounts = [(x, t) for t,x in diffs.items() if x >= 12]
                if len(diffCounts) == 0: continue
                _, diff = max(diffCounts)
                dx, dy, dz = diff
                for x,y,z in scan:
                    t = (x-dx, y-dy, z-dz)
                    if t not in cube: cube.append(t)
                remove.append(k)
                scanners.append((-dx, -dy, -dz))
                break
        for r in remove:
            pending.remove(r)
    count = len(cube)

    # Part 2
    limit = len(scanners)
    distances: list[int] = []
    for i in range(limit):
        for j in range(i+1, limit):
            distances.append(manhattan3(scanners[i], scanners[j]))
    maxDistance = max(distances)

    return newSolution(count, maxDistance)

def generateOrientations() -> list[int3]:
    faces: list[int3] = [
        (1,2,3),    # front 
        (-1,2,-3),  # back 
        (1,3,-2),   # top 
        (1,-3,2),  # bottom 
        (-3,2,1),   # left 
        (3,2,-1),   # right
    ]
    orientations: list[int3] = []
    for face in faces:
        f1, f2, f3 = face 
        orientations.append((f1,f2,f3))
        orientations.append((f2,-f1,f3))
        orientations.append((-f1,-f2,f3))
        orientations.append((-f2,f1,f3))
    return orientations

def generateVersions(scans: list[int3], orientations: list[int3]) -> dict[int, list[int3]]:
    versions: dict[int, list[int3]] = {}
    for i, orientation in enumerate(orientations):
        (x,y,z), (xf, yf, zf) = getIndexFactors(orientation)
        version: list[int3] = []
        for scan in scans:
            a = scan[x] * xf 
            b = scan[y] * yf 
            c = scan[z] * zf 
            version.append((a,b,c))
        versions[i] = version
    return versions

def getIndexFactors(orientation) -> tuple[int3, int3]:
    x, y, z = orientation
    xf = 1 if x > 0 else -1 
    yf = 1 if y > 0 else -1 
    zf = 1 if z > 0 else -1
    x, y, z = abs(x)-1, abs(y)-1, abs(z)-1
    return (x,y,z), (xf, yf, zf)

def getDiff(s1: int3, s2: int3) -> int3:
    x1,y1,z1 = s1
    x2,y2,z2 = s2  
    return (x2-x1, y2-y1, z2-z1)

if __name__ == '__main__':
    do(solve, 21, 19)

'''
Part1:
- Generate the 24 orientations of the scanners:
    - Start with the 6 faces of the cube: front, back, top, bot, left, right
    - Then for each face, use the original version, and the 3 rotate lefts 
- For each scanner, except scanner 0, generate the 24 versions of the points 
  using the 24 orientations above:
    - Transform the point by rearranging the coordinates and applying the negations 
      based on the given orientation
- Generate the 3D cube, initialized by scanner 0 points (this is our reference)
- Repeat until there are no more pending scanners to be processed:
    - Go through each pending scanner; for each scanner, go through each version 
    - For all the triples in the current cube, and the triples in the current scanner version:
        - Compute their diffs and group the diff triples, to find a diff triple that appears at least 12 times 
        - If we find a diff triple that appears >= 12 times, this is a valid overlap with the cube
        - The diff triple with all the values negated will give you the location of that scanner 
          (because by adjusting it this way, the diff with the cube would be 0 = perfectly aligned)
        - Add this scanner versions points to the cube, but adjusted (-dx, -dy, -dz)
        - This scanner is removed from the pending list
- Return the number of cubes found after processing all scanners 

Part2:
- From Part 1, we have determined the locations of the scanners
- For each pair of scanner, compute their Manhattan distance 
- Output the maximum distance found among all pairs
'''