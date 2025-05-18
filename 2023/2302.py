# Advent of Code 2023 Day 02
# John Roy Daradal 

from aoc import *

class Game:
    def __init__(self, number: int):
        self.id = number 
        self.draws = []
    
    def addDraw(self, line: str):
        r,g,b = 0,0,0
        for part in line.split(','):
            number, color = splitStr(part, None)
            number = int(number)
            if color == 'red':
                r = number 
            elif color == 'green':
                g = number
            elif color == 'blue':
                b = number 
        self.draws.append((r,g,b))

def data(full: bool) -> list[Game]:
    def fn(line: str) -> Game:
        head, tail = splitStr(line, ':')
        number = int(head.split()[1])
        game = Game(number)
        for draw in splitStr(tail, ';'):
            game.addDraw(draw)
        return game

    return [fn(line) for line in readLines(23, 2, full)]

def part1():
    games = data(full=True)
    total = getTotal(games, validID) 
    print(total)

def part2():
    games = data(full=True)
    total = getTotal(games, gamePower)
    print(total)

def validID(game: Game) -> int:
    isValid = True 
    for r,g,b in game.draws:
        if r > 12 or g > 13 or b > 14:
            isValid = False 
    return game.id if isValid else 0

def gamePower(game: Game) -> int:
    maxR, maxG, maxB = 0,0,0
    for r,g,b in game.draws:
        maxR = max(maxR, r)
        maxG = max(maxG, g)
        maxB = max(maxB, b)
    return maxR * maxG * maxB

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Determine if game is valid or not: cannot have r>12 or g>13 or b>14
- If valid, add game.id to total

Part2:
- Determine the maximum number or r, g, b cubes 
- Multiply the 3 numbers to form the power
'''