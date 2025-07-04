# Advent of Code 2019 Day 19
# John Roy Daradal 

from aoc import *
from intcode import *

Grid = dict[coords,int]

def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 19, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    # Part 1
    grid: Grid = {}
    rows, cols = 50, 50
    for y in range(rows):
        for x in range(cols):
            grid[(y,x)] = getTileAt(y, x)
    count = len([x for x in grid.values() if x == 1])

    # displayGrid(grid)

    # Part 2 
    score = findSquare(grid, (rows,cols), 30, 100)

    return newSolution(count, score)

def getTileAt(y: int, x: int) -> int:
    numbers = data(full=True)
    return runProgram(numbers, [x,y])

def runProgram(numbers: dict[int, int], inputs: list[int]) -> int:
    i, rbase = 0, 0 
    output = 0
    while True:
        word = str(numbers[i])
        head, tail = word[:-2], word[-2:]
        cmd = int(tail)
        if cmd == 99: break 

        if cmd in (1,2,7,8): # Add, Multiply, LessThan, Equals
            in1, in2, out = numbers[i+1], numbers[i+2], numbers[i+3]
            m1, m2, m3 = modes(head, 3)
            a = param2(in1, m1, rbase, numbers)
            b = param2(in2, m2, rbase, numbers)
            c = index(out, m3, rbase)
            if cmd == 1:
                numbers[c] = a + b
            elif cmd == 2:
                numbers[c] = a * b
            elif cmd == 7: 
                numbers[c] = 1 if a < b else 0
            elif cmd == 8:
                numbers[c] = 1 if a == b else 0
            i += 4
        elif cmd == 3: # Input
            m = modes(head, 1)[0]
            idx = index(numbers[i+1], m, rbase)
            numbers[idx] = inputs.pop(0)
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            output = param2(numbers[i+1], m, rbase, numbers)
            i += 2 
        elif cmd == 9: # relative base 
            m = modes(head, 1)[0]
            jmp = param2(numbers[i+1], m, rbase, numbers)
            rbase += jmp 
            i += 2
        elif cmd == 5 or cmd == 6: #Jump-if-True/False
            p1, p2 = numbers[i+1], numbers[i+2]
            m1, m2 = modes(head, 2)
            isZero = param2(p1, m1, rbase, numbers) == 0
            doJump = isZero if cmd == 6 else (not isZero)
            if doJump:
                i = param2(p2, m2, rbase, numbers)
            else:
                i += 3
    return output

def displayGrid(grid: Grid):
    maxRow = max(c[0] for c in grid.keys())
    maxCol = max(c[1] for c in grid.keys())
    for row in range(maxRow+1):
        line: list[str] = []
        for col in range(maxCol+1):
            pt = (row,col)
            tile = '?'
            if pt in grid: 
                tile = '#' if grid[pt] == 1 else '.'
            line.append(tile)
        print(''.join(line) + ' ' + str(row))

def findSquare(grid: Grid, bounds: dims2, startRow: int, squareSide: int) -> int:
    rows, cols = bounds
    rowStart: dict[int, int] = {}
    rowEnd: dict[int, int] = {}

    # Compute the first row range 
    row = startRow
    for col in range(1,cols):
        diff = abs(grid[(row,col-1)] - grid[(row,col)])
        if row not in rowStart and diff == 1:
            rowStart[row] = col
        elif row not in rowEnd and diff == 1:
            rowEnd[row] = col

    continueRow = rows
    # Compute the full row ranges from existing grid
    for row in range(startRow+1, rows):
        # Skip all blank
        if all(grid[row,x] == 0 for x in range(cols)):
            continueRow = row
            break

        prevRow = row-1 
        # Find row start 
        col = rowStart[prevRow]
        while grid[(row,col)] != 1:
            col += 1
        rowStart[row] = col 

        # Find row end 
        incomplete = False
        col = rowEnd[prevRow]
        if col >= cols:
            incomplete = True 
        else:
            while grid[(row,col)] != 0:
                if col + 1 == cols: 
                    incomplete = True
                    break 
                else:
                    col += 1
        
        # If incomplete, explore to the right until we find end
        if incomplete:
            # start at the column boundary until we find 0
            col = exploreUntil(row, cols, 0)

        rowEnd[row] = col 

    # Explore the rows outside the grid
    row = continueRow 
    while True:
        prevRow = row-1 

        # Find row start 
        rowStart[row] = exploreUntil(row, rowStart[prevRow], 1)
        # Find row end 
        rowEnd[row] = exploreUntil(row, rowEnd[prevRow], 0)

        start, end = rowStart[row], rowEnd[row]
        width = end - start
        height = row - startRow

        # process if can have valid width and height 
        if width >= squareSide and height >= squareSide:
            wiggle = (width - squareSide) + 1
            for w in range(wiggle):
                colStart = start + w
                score = checkSquare(rowStart, rowEnd, row, colStart, squareSide)
                if score > 0: return score 
        # Go to next row
        row += 1

def exploreUntil(row: int, col: int, goal: int) -> int:
    while True:
        tile = getTileAt(row, col)
        if tile == goal:
            return col 
        else:
            col += 1

def checkSquare(rowStart: dict[int,int], rowEnd: dict[int,int], row: int, col: int, squareSide: int) -> int:
    colStart, colEnd = col, col+squareSide
    for d in range(squareSide-1):
        y = row - d - 1 
        start, end = rowStart[y], rowEnd[y]
        inRange = start <= colStart < end and start < colEnd <= end
        if not inRange: return 0
    # all rows passed 
    y = row - (squareSide-1) 
    x = colStart * 10000 
    return x + y

if __name__ == '__main__':
    do(solve, 19, 19)

'''
Part1:
- RunProgram is similar to 1909, but two inputs are fed: (x, y) and the output is the tile type (1 or 0) in the grid
- Run the program multiple times to get the tiles for the 50x50 grid (0-49 for rows, cols)
- Output the count of 1 tiles in the grid

Part2:
- Find the nearest 100x100 square that fits in the beam
- Start at row 30 (skip the earlier rows that are not big enough)
- Compute the row range (start,end) at row 30, by finding where successive 0 and 1 tiles are
- Compute the row ranges from row 31 to 50 from the existing grid
- If row is already all 0, break loop and let the exploratory phase start at this row 
- To compute the range of the existing grid rows, we need to find the starting # (start) and the column after the last # (end)
- To find the row start of existing row:
    - Start at the column where the previous row started
    - Move forward until we find a 1 tile; this is the starting column for this row
- To find the row end of existing row:
    - Start at the column where the previous row ended 
    - If column is out of bounds, mark as incomplete (for further exploration)
    - Move forward until we find a 0 tile or we go out of bounds (incomplete)
    - If incomplete, start at the grid column boundary and move forward until we find a 0 tile
    - This involves running the program again as this was previously unexplored by Part 1
    - The found 0 tile on this row becomes the ending column
- After processing the ranges of the 50x50 grid, we will now explore the next rows
- We will not do a full row scan: we will only limit our search to the range of the previous row and expand from there 
- To find the row start of unexplored row:
    - Start at the column where previous row started 
    - Run the program to find the tile type and move forward until we find a tile 1
- To find the row end of unexplored row:
    - Start at the column where previous row ended 
    - Run the program to find the tile type and move forward until we find a tile 0
- After computing the row's range, check if it can house the 100x100 square:
    - Check that the width of the row range >= 100 
    - Check that the height of current row is also sufficient (has at least 100 rows before it)
    - Compute the wiggle room for sliding the square horizontally: (width - 100) + 1
    - For each valid starting column position, check if it can house the 100x100 square
    - Return immediately once square is found
- Go to next row if square is not yet found
- To check if current window has 100x100 square:
    - Compute the column bounds: current column (start), start + 100 (end)
    - Check the previous 100 rows if the column range is a subset of that row's range
    - Once one row fails, stop immediately 
    - If all rows passed, return the top-left corner's (x*10,000) + y
'''