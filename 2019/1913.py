# Advent of Code 2019 Day 13
# John Roy Daradal 

from aoc import *
from intcode import *

def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 13, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    # Part 1
    numbers = data(full=True)
    count = runProgram(numbers, False) 

    # Part 2  
    numbers = data(full=True)
    numbers[0] = 2
    score = runProgram(numbers, True)

    return newSolution(count, score)

def moveJoystick(ballPos: coords, paddlePos: coords) -> int:
    bx = ballPos[1]
    px = paddlePos[1]
    return cmp(bx, px)

def runProgram(numbers: dict[int, int], playGame: bool) -> int:
    i, rbase = 0, 0 
    grid: dict[coords, int] = {}
    outputs: list[int] = []
    score = 0
    ballPos = (0,0)
    paddlePos = (0,0)
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
            move = moveJoystick(ballPos, paddlePos)
            numbers[idx] = move
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            out = param2(numbers[i+1], m, rbase, numbers)
            outputs.append(out)
            if len(outputs) == 3:
                x, y, tile = outputs
                outputs = [] # reset
                if x == -1 and y == 0:
                    score = tile
                else:
                    grid[(y,x)] = tile
                    if tile == 3:
                        paddlePos = (y,x)
                    elif tile == 4:
                        ballPos = (y,x)
                # if playGame: displayGame(grid, score)
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
    
    if playGame:
        return score
    else:
        count = sum(1 for tile in grid.values() if tile == 2)
        return count
    
def displayGame(grid: dict[coords,int], score: int):
    ys = [c[0] for c in grid.keys()]
    xs = [c[1] for c in grid.keys()]
    y1, x1 = min(ys), min(xs)
    y2, x2 = max(ys), max(xs)
    os.system('clear')
    print('Score:', score)
    for y in range(y1, y2+1):
        row = []
        for x in range(x1, x2+1):
            tile = grid.get((y,x), 0)
            pixel = ' '
            if tile == 1:
                pixel = '#'
            elif tile == 2:
                pixel = '*'
            elif tile == 3:
                pixel = '_'
            elif tile == 4:
                pixel = 'O'
            row.append(pixel)
        print(''.join(row))

if __name__ == '__main__':
    do(solve, 19, 13)

'''
Solve:
- For Part 1, run the program and count the number of block tiles (2) in the grid 
- For Part 2, set memory 0 to 2, run the program and output the final score

RunProgram:
- Similar to 1909 Intcode, but with modified input (3) and output (4)
- For input, figure out how to move the joystick by comparing the current ball and paddle positions
    - Compare the x values of the ball and paddle
    - If ball.x < paddle.x, go left: input = -1 
    - If ball.x > paddle.y, go right: input = 1 
    - Otherwise, stay put: input = 0
- For output, process the output in triples (wait for 3 outputs):
    - First 2 outputs specify the x and y coords of the tile
    - The 3rd output specifies the tile type: 0 = empty, 1 = wall, 2 = block, 3 = paddle, 4 = ball
    - But if x,y is (-1,0), the 3rd value is the current score
    - If tile is 3 (paddle) or 4 (ball), update the paddle and ball position values
'''