# Advent of Code 2020 Day 05
# John Roy Daradal 

from aoc import *

Seat = tuple[list[int], list[int]]
T = {'F': 0, 'B': 1, 'L': 0, 'R': 1}

def data(full: bool) -> list[Seat]:
    def fn(line: str) -> Seat: 
        row = [T[x] for x in line[:7]]
        col = [T[x] for x in line[7:]]
        return (row, col)
    return [fn(line) for line in readLines(20, 5, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    seats = data(full = True)
    maxID = 0 
    for seat in seats:
        maxID = max(maxID, computeID(seat))
    return maxID

def part2() -> int:
    seats = data(full = True)
    ids = [computeID(seat) for seat in seats]
    ids.sort()
    seatID = 0
    for i in range(1, len(ids)):
        if ids[i] - ids[i-1] > 1:
            seatID = ids[i]-1
            break 
    return seatID

numRows, numCols = 128, 8
def computeID(seat: Seat) -> int: 
    rows, cols = seat 
    row = binaryMoves(rows, numRows)
    col = binaryMoves(cols, numCols)
    return (row*8) + col 

def binaryMoves(sides: list[int], limit: int) -> int:
    start, end = 0, limit 
    for s in sides[:-1]:
        mid = start + ((end-start) // 2)
        if s == 0:
            end = mid 
        elif s == 1:
            start = mid 
    return start if sides[-1] == 0 else end-1

if __name__ == '__main__':
    do(solve, 20, 5)

'''
Data:
- Get first 7 chars, map F => 0, B => 1
- Get remaining chars, map L => 0, R => 1

Part1:
- Compute the seat ID of each seat, get the max ID 
- SeatID row: binaryMoves(rows)
- SeatID col: binaryMoves(cols)
- Return row*8 + col

Part2:
- Compute all seat IDs similar to Part1 
- Sort the IDs 
- Find the gap in the ids: successive items where diff > 1

BinaryMoves:
- Similar to binary search 
- Initialize: start = 0, end = limit 
- Process all moves (0 or 1) except last one
- if 0: make end = mid 
- if 1: make start  mid 
- If last move is 0, return start 
- If last move is 1, return end-1
'''