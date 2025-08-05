# Advent of Code 2018 Day 23
# John Roy Daradal 

from aoc import *

Bot = tuple[int3, int] # position, radius

def data(full: bool) -> list[Bot]:
    def fn(line: str) -> Bot:
        for rep in ['pos=<', 'r=', '>']:
            line = line.replace(rep, '')
        x,y,z,r = toIntList(line, ',')
        return ((x,y,z), r)
    return [fn(line) for line in readLines(18, 23, full)]

def solve() -> Solution:
    bots = data(full=True)

    # Part 1
    pos, radius = max(bots, key=lambda b: b[1]) 
    inRange = lambda bot: manhattan3(pos, bot[0]) <= radius
    count = countValid(bots, inRange)

    # Part 2
    points: list[int2] = []
    for pos, r in bots:
        d = manhattan3(pos)
        start = max(0, d-r) # clip to 0, no negative distances
        end   = d+r
        points.append((start, 1))
        points.append((end, -1))
    
    currCount, maxCount = 0, 0 
    maxCountDistance = 0
    for dist, adj  in sorted(points):
        currCount += adj 
        if currCount > maxCount:
            maxCount = currCount 
            maxCountDistance = dist

    return newSolution(count, maxCountDistance)

if __name__ == '__main__':
    do(solve, 18, 23)

'''
Part1:
- Select the bot with the maximum radius
- Count the bots that are within range of the maxRadiusBot: 
  Manhattan distance of the MRB's position and bot's position <= MRB's radius

Part2:
- For each bot, compute the Manhattan distance of its position to (0,0,0)
- Minimum distance of bot = ManhattanDist - botRadius; clip value to 0 = no negative distances
- Maximum distance of bot = ManhattanDist + botRadius
- Add the min and max distance to a list, together with an indicator if it is a 
  starting point (+1) or ending point (-1)
- We are looking for the point with the maximum overlap among robots, and for the tie-breaker, 
  choose the point that is closest to (0,0,0) = shortest Manhattan distance
- Use the min/max distance range of bots to check this quickly:
    - Once we encounter a starting point, we immediately set the starting point of our current range
      to this starting point, and add 1 to our range count, since it adds 1 more robot reachable from current range
    - If we encounter an ending point, we close the current range, decrementing the range count by 1
    - We keep track of the maximum range count during iteration; if the current count exceeds max count, 
      update the max count, and update the max count distance that caused this change
- The final max count distance is the shortest distance with maximum overlap from the robots
- Reference for algorithm:
  https://stackoverflow.com/questions/15013800/find-the-maximally-intersecting-subset-of-ranges
'''