# Advent of Code 2021 Day 21
# John Roy Daradal 

import itertools 
from functools import cache
from aoc import *

trackSize = 10

def data(full: bool) -> list[int]:
    starts: list[int] = []
    for line in readLines(21, 21, full):
        start = splitStr(line, ':')[1]
        starts.append(int(start)-1)
    return starts

def solve() -> Solution:
    position = data(full=True)
    p1, p2 = position

    # Part 1
    score: list[int] = [0,0]
    diceSize, goalScore = 100, 1000
    player, dice, count = 0, 0, 0
    product = 1
    while True:
        rolls = [(dice + i) % diceSize for i in range(3)]
        steps = (sum(rolls) + 3) % trackSize
        position[player] = (position[player] + steps) % trackSize
        score[player] += position[player] + 1

        count += 3
        dice = (dice + 3) % diceSize

        if score[player] >= goalScore:
            opp = (player + 1) % 2 
            product = count * score[opp]
            break
        else:
            player = (player + 1) % 2

    # Part 2
    w1, w2 = countWinners(p1, 0, p2, 0)
    maxWin = max(w1, w2)

    return newSolution(product, maxWin)

@cache 
def countWinners(p1: int, s1: int, p2: int, s2: int) -> int2:
    goalScore = 21
    w1, w2 = 0, 0
    for rolls1 in itertools.product([1,2,3], repeat=3):
        np1 = (p1 + sum(rolls1)) % trackSize 
        ns1 = (s1 + np1 + 1)
        if ns1 >= goalScore:
            w1 += 1
            continue 
        for rolls2 in itertools.product([1,2,3], repeat=3):
            np2 = (p2 + sum(rolls2)) % trackSize 
            ns2 = (s2 + np2 + 1)
            if ns2 >= goalScore:
                w2 += 1
            else:
                nw1, nw2 = countWinners(np1, ns1, np2, ns2)
                w1 += nw1 
                w2 += nw2
    return w1, w2

if __name__ == '__main__':
    do(solve, 21, 21)

'''
Part1:
- Start with the 2 players' initial positions, and their scores initialized to 0
- Starting with player 1, the players alternate and play their turn until one of them scores at least 1000:
    - At each player's turn, he rolls the dice 3 times, where the results are: dice, dice+1, dice+2
    - On the next turn, the dice starts at dice+3; it wraps around back to 1 after reaching 100
    - Example: Starting with 1,2,3, the next turn gives 4,5,6, then the next turn gives 7,8,9, etc.
    - Sum up the 3 dice values = number of steps; use % trackSize (10), since we need to wrap-around the track
    - The player's position is updated by the number of steps; wrap around the track size if necessary
    - The player's score is increased by the position in which he landed after moving
    - Count the total number of dice rolls (incremented by 3 in each round)
- If one player already reaches a score of at least 100, we stop the game
- Output the product of the losing player's score and the number of dice rolls so far

Part2:
- In this game version, each player rolls a dice with 3 possible values, 3 times during his turn
- Game ends when a player reaches a score of at least 21
- Count the number of games player 1 and player 2 can possibly win given their initial positions
- At each dice roll, the universe splits into 3 versions: where 1, 2, or 3 was rolled
- Use a cached recursive function to compute the number of wins for player 1 and player 2,  
  given both of their current positions and scores; initial call = initial positions and scores = 0
    - Go through the 27 possibilites of player 1 rolling his dice: product([1,2,3], repeat=3)
    - Compute the new position and score of player 1 if this dice combo is used
    - If the new score of player 1 reaches at least 21, increment the wins for player 1
    - If not, continue with player 2's turn
    - Go through the 27 possibilities of player 2 rolling his dice: product([1,2,3], repeat=3)
    - Compute the new position and score of player 2 if this dice combo is used
    - If the new score of player 2 reaches at least 21, increment the wins for player 2
    - If not, recursively call countWinners with the 2 player's new positions and scores
    - Increment player 1 and 2's win totals by the returned values of countWinners
- Use functools.cache since a lot of the subproblems would be overlapping
- Output the number of wins for the player with more possible wins
'''