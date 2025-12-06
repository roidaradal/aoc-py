# Advent of Code 2025 Day 06
# John Roy Daradal 

from aoc import *
from functools import reduce

def data(full: bool) -> list[str]:
    return [line.strip('\n') for line in readLines(25, 6, full, strip=False)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    lines = data(full=True)
    lastLine = len(lines)-1 
    
    # Get the operands and the operators
    allOperands: list[list[int]] = []
    for i,line in enumerate(lines[:lastLine]):
        for col, number in enumerate(line.strip().split()):
            if i == 0:
                allOperands.append([int(number)])
            else:
                allOperands[col].append(int(number))
    operators = lines[lastLine].split()

    # Get the total of all operations
    total = sum(getResult(operators[i], operands) for i,operands in enumerate(allOperands))

    return total

def part2() -> int:
    lines = data(full=True)
    lastLine = len(lines)-1

    # Build the string grid
    grid: StrGrid = [list(line) for line in lines[:lastLine]]
    gridRows = len(grid)

    # Get the operators and the operator indexes
    # This serves as the limits for the columns
    operators: list[str] = []
    indexes: list[int] = []
    for i, char in enumerate(lines[lastLine]):
        if char == ' ': continue 
        operators.append(char)
        indexes.append(i)
    indexes.append(len(grid[0])+1) # add last limit

    # Get the total of all operations
    total = 0
    for i, operator in enumerate(operators):
        # The current and next operator indexes become boundaries for the columns
        start, end = indexes[i], indexes[i+1]-1
        operands: list[int] = []
        for col in range(start, end):
            # Build the number from top row to bottom, along current column
            num = ''
            for row in range(gridRows):
                num += grid[row][col]
            operands.append(int(num.strip()))
        total += getResult(operator, operands)
    return total

def getResult(operator: str, operands: list[int]) -> int:
    if operator == '+':
        return sum(operands)
    elif operator == '*':
        return reduce(lambda x, y: x * y, operands, 1)
    return 0

if __name__ == '__main__':
    do(solve, 25, 6)

'''
Part1:
- Get the operands and operators from the input 
- For each line, split the numbers by whitespace
- These numbers are added to the operands list for each column
- The last line contains the operators split by whitespace
- Sum up the results of applying the operation on the operands
- + gets the sum of operands, while * gets the product

Part2:
- Treat the input as a string grid, except for the last line (operators)
- Get the operators and their column indexes as this will serve as the limits 
  for the column boundary processing when doing the operations
- Add the last limit to the end (numCols+1)
- To perform the operations, go through the column boundaries
- For each column in the range, build the number by going through the rows from 
  top to bottom along the current column
- Collect the operands and apply the operation
- Output the total of the result operations
'''