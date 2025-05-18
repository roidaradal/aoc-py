# Advent of Code 2022 Day 02
# John Roy Daradal 

from aoc import readLines, getTotal, do

rps = tuple[int,int]
R,P,S = 1,2,3 
L,D,W = 0,3,6

def data(T: dict[str,int], full: bool) -> list[rps]:
    def fn(line: str) -> rps:
        p = line.split()
        return (T[p[0]], T[p[1]])
    return [fn(line) for line in readLines(22, 2, full)]

def part1():
    T = {'A': R, 'B': P, 'C': S, 'X': R, 'Y': P, 'Z': S}
    games = data(T, full=True)
    total = getTotal(games, computeScore)
    print(total)

def part2():
    T = {'A': R, 'B': P, 'C': S, 'X': L, 'Y': D, 'Z': W}
    games = data(T, full=True)
    total = getTotal(games, coerceScore)
    print(total)

winsOver = {R: S, P: R, S: P}
losesTo  = {S: R, R: P, P: S}

def computeScore(game: rps) -> int:
    opp, you = game
    score = you 
    if opp == you:
        score += D 
    elif winsOver[you] == opp:
        score += W
    return score

def coerceScore(cfg: rps) -> int:
    opp, out = cfg 
    if out == W:
        you = losesTo[opp]
    elif out == L:
        you = winsOver[opp]
    else: # Draw
        you = opp 
    return computeScore((opp, you))

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Get the total score of each RPS game 
- Base score = value of your hand (R=1, P=2, S=3)
- If same hand, add score for draw (D=3)
- If your hand wins over opp, add score for winning (W=6)
- Create a lookup table winsOver and losesTo for easily determining
  the result of your hand vs opponent's hand

Part2:
- Figure out the hand that will ensure the corect outcome 
- If outcome is draw, choose the same hand as opp 
- If outcome is win, choose the hand that your opp loses to 
- If outcome is lose, coose the hand that your will make your opponent win
- Reuse the computeScore from Part1
'''