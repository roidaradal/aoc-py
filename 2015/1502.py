# Advent of Code 2015 Day 02
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> list[dims3]:
    fn = lambda line: toDims3(line, 'x')
    return [fn(line) for line in readLines(15, 2, full)]

def part1():
    def fn(dims: dims3) -> int:
        l,w,h = dims 
        lw, wh, lh = l*w, w*h, l*h 
        return (2*lw) + (2*wh) + (2*lh) + min(lw,wh,lh)
    
    items = data(full=True)
    total = getTotal(items, fn)
    print(total)

def part2():
    def fn(dims: dims3) -> int:
        d1, d2, d3 = sorted(dims) 
        return (2 * (d1+d2)) + (d1*d2*d3)
    
    items = data(full=True)
    total = getTotal(items, fn)
    print(total)


if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Sum up values computed with formula:
- 2*lw + 2*wh + 2*lh + min(lw,wh,lh)

Part2:
- Sort ascending the dimensions 
- Compute smallest face perimeter: 2 * (d1+d2)
- Add volume: d1*d2*d3
'''