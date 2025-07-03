# Advent of Code 2019 Day 17
# John Roy Daradal 

from aoc import *
from intcode import *

def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 17, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    # Part 1
    numbers = data(full=True)
    grid = runProgram(numbers, [])
    total = totalAlignment(grid)

    # Part 2 
    numbers = data(full=True)
    numbers[0] = 2
    inputs = generateInputs(traverseGrid(grid))
    dust = runProgram(numbers, inputs)[0]

    return newSolution(total, dust)

def runProgram(numbers: dict[int, int], inputs: list[int]) -> list[str]:
    i, rbase = 0, 0 
    grid: list[str] = []
    line: list[str] = []
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
            if output >= 128: # not an ASCII code
                return [str(output)] # For Part 2
            
            tile = chr(output) # at this point, we know it's a valid ASCII code
            if output == 10: # newline 
                if len(line) > 0: grid.append(''.join(line))
                line = []
            else:
                line.append(tile)
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
    return grid

def totalAlignment(grid: list[str]) -> int:
    bounds = getBounds(grid) 
    total = 0
    for row,line in enumerate(grid):
        for col,tile in enumerate(line):
            if tile != '#': continue 
            near = [c for c in surround4((row,col)) if insideBounds(c, bounds)]
            scaffold = sum(1 for ny,nx in near if grid[ny][nx] == '#')
            if scaffold == 4: # all 4 neighbors are scaffold = intersection
                total += row * col 
    return total

def traverseGrid(grid: list[str]) -> list[str]:
    bounds = getBounds(grid)

    # Find the robot starting point and initial delta
    curr: coords = (0,0)
    d: delta = X
    for row, line in enumerate(grid):
        for col,tile in enumerate(line):
            if tile == '^':
                curr, d = (row,col), U 
            elif tile == '<':
                curr, d = (row,col), L 
            elif tile == '>':
                curr, d = (row,col), R 
            elif tile == 'v':
                curr, d = (row,col), D 
    
    steps: list[str] = []
    forward = 0
    while True:
        ny,nx = move(curr, d)
        if insideBounds((ny,nx), bounds) and grid[ny][nx] == '#':
            curr = (ny,nx)
            forward += 1 
        else:
            # Stopped in current direction
            if forward > 0: steps.append(str(forward))
            forward = 0 
            # Try turn left and right
            ly, lx = move(curr, leftOf[d])
            ry, rx = move(curr, rightOf[d])
            if insideBounds((ly,lx), bounds) and grid[ly][lx] == '#':
                d = leftOf[d]
                steps.append('L')
            elif insideBounds((ry,rx), bounds) and grid[ry][rx] == '#':
                d = rightOf[d]
                steps.append('R')
            else:
                break 
    return steps

def generateInputs(steps: list[str]) -> list[int]:
    minSize = 4     # start with first 4
    increment = 2   # process in pairs
    minMatch = 3    # substring has to have at least 3 matches in the string
    maxLength = 20 
    fullSteps = ','.join(steps)
    programName = ['A', 'B', 'C']

    programs: list[str] = []
    while len(steps) > 0:
        end = minSize
        endMatches: dict[int,list[int2]] = {}
        while True:
            matches = findMatches(steps[:end], steps)
            ok1 = len(matches) >= minMatch 
            ok2 = len(','.join(steps[:end])) <= maxLength
            if ok1 and ok2:
                endMatches[end] = matches
                end += increment # grow bigger
            else:
                # Get the end with most matches, tie-breaker: higher idx
                end = max((len(matches), idx) for idx, matches in endMatches.items())[1]
                programIdx = len(programs)
                programs.append(','.join(steps[:end]))
                steps = replaceMatches(steps, endMatches[end], programName[programIdx])
                while len(steps) > 0 and steps[0] in programName:
                    steps.pop(0) # remove the leading program names
                break
            
    sequence: list[str] = []
    while len(fullSteps) > 0:
        for i, program in enumerate(programs):
            if fullSteps.startswith(program):
                fullSteps = fullSteps[len(program):].strip(',')
                sequence.append(programName[i])
                break
    
    main = ','.join(sequence) + '\n'
    for i in range(len(programs)):
        programs[i] += '\n'
    feed = 'n\n'

    inputs = [main] + programs + [feed]
    return [ord(x) for x in ''.join(inputs)]

def findMatches(needle: list[str], haystack: list[str]) -> list[int2]:
    windowSize = len(needle)
    i, limit = 0, len(haystack)
    matches: list[int2] = []
    while i < limit:
        if haystack[i:i+windowSize] == needle:
            matches.append((i, i+windowSize))
            i += windowSize # move past matching window 
        else:
            i += 1
    return matches 

def replaceMatches(steps: list[str], matches: list[int2], name: str ) -> list[str]:
    for start,end in matches:
        for i in range(start,end):
            steps[i] = name
    return steps

if __name__ == '__main__':
    do(solve, 19, 17)

'''
RunProgram:
- Similar to 1909 IntCode program, with few additions:
- For the input for Part 2, pre-compute the input queue (see below)
- For the output, if it's not an ASCII code return right away (for Part 2)
- Otherwise, we convert the output number to a char based on its ASCII code, 
  building the grid from the output tiles; we end a grid line when we see a newline (10)

Part 1:
- Run the program to build the grid; we dont need inputs for Part 1
- Find the intersections in the grid: # tiles that are also have # tiles in NEWS
- Output the total row * col of the found intersections

Part 2:
- Set numbers[0] to 2, to make the robot move 
- Let the robot traverse the scaffold in the grid and compute the input queue from the steps
- Run the program with the input stream, and the output should be a non-ASCII number 
- Traverse Grid:
    - Find the robot position in the grid and its initial direction by finding ^<>v
    - Robot's strategy for traversing is: keep going forward in the current direction
    - Increment the forward step if we can still step on a scaffold in the next tile 
    - Otherwise, the current direction ends here and we add the current forward count to the steps 
    - Try to turn left and right and check which direction has a scaffold 
    - Add L or R to the step (turn), and change the direction
    - Stop if it cannot move forward, left or right
    - Return the step sequence which consists of L, R, and numbers (forward counts)
- Generate Inputs:
    - From the step sequence, we need to generate the int input sequence 
    - Segment the steps into 3 programs: A, B, C so that the main program just call them in sequence
    - When trying to look for viable program, these are the rules:
        1 Has to have at least 4 steps (minSize)
        2 Increment the size of the window by 2 (process in pairs)
        3 The resulting substring should have at least 3 matches in the step sequence
        4 The resulting string sequence (joined by comma) should be 20 chars or less
    - Start with the window from 0 to minSize
    - Count the number of matches of this window in the remaining steps:
        - Do a sliding window approach to find matches
        - If we find a match, move past the matching window
        - Otherwise, increment by 1 to check the next index's window
    - Check that condition 3 and 4 above are satisfied
    - If both conditions pass, we add current end to viable windows and increment it by 2 to make the
      window bigger in the next iteration 
    - If any condition fails, we are ready to choose the best window
    - Select the end with the most matches, tie-breaker: higher index = bigger window 
    - Add this window to the list of current programs  
    - Replace all instances of this window with the program name (A, B, C)
    - This is important to keep the sequence intact: if we just plain remove it from the steps, 
      we could match a window that previously didn't exist: e.g. ABC, by removing B, we could match AC
    - Then remove any leading program names from the steps (A,B,C)
    - Repeat until all the steps are replaced and removed
    - After finding the 3 programs, we generate the main sequence by matching the windows to the known programs
    - The final input sequence is the main sequence + newline, program A, B, C with newlines, and 'n' with newline 
    - Convert these characters to ASCII code to form the input stream
'''