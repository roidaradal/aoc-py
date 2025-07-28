# Advent of Code 2015 Day 21
# John Roy Daradal 

import itertools
from aoc import *

Vector = tuple[int, int, int]

shop: dict[str, list[Vector]] = {
    'weapon': [
        (8,4,0),    # dagger
        (10,5,0),   # shortsword
        (25,6,0),   # warhammer 
        (40,7,0),   # longsword
        (74,8,0),   # greataxe
    ],
    'armor': [
        (0,0,0),    # no armor
        (13,0,1),   # leather
        (31,0,2),   # chainmail
        (53,0,3),   # splintmail
        (75,0,4),   # bandedmail
        (102,0,5),  # platemail
    ],
    'ring': [
        (0,0,0),    # no ring
        (25,1,0),   # dmg+1
        (50,2,0),   # dmg+2
        (100,3,0),  # dmg+3
        (20,0,1),   # def+1
        (40,0,2),   # def+2
        (80,0,3),   # def+3
    ],
}

def data(full: bool) -> Vector:
    values: list[int] = []
    for line in readLines(15, 21, full):
        tail = splitStr(line, ':')[1]
        values.append(int(tail))
    hp, dmg, armor = values 
    return (hp, dmg, armor)

def solve() -> Solution:
    opp = data(full=True)

    weapons, armors = shop['weapon'], shop['armor']
    ringCombos = list(itertools.combinations(shop['ring'], 2))

    minCost = sys.maxsize
    maxCost = 0
    for weapon, armor, rings in itertools.product(weapons, armors, ringCombos):
        you, cost = buildPlayer(weapon, armor, rings)
        playerWin = playGame(you, opp)
        
        if playerWin:
            # Part 1
            minCost = min(minCost, cost)
        else:
            # Part 2
            maxCost = max(maxCost, cost)

    return newSolution(minCost, maxCost)

def playGame(you: Vector, opp: Vector) -> bool:
    hp0, dmg0, arm0 = opp 
    hp1, dmg1, arm1 = you 
    atk0 = max(dmg0 - arm1, 1)
    atk1 = max(dmg1 - arm0, 1)

    turn = 1 # player starts 
    while True:
        if turn == 0: # opponent attacks
            hp1 -= atk0
            if hp1 <= 0: return False # opp wins
        elif turn == 1: # player attacks
            hp0 -= atk1 
            if hp0 <= 0: return True # player wins
        turn = (turn + 1) % 2

def buildPlayer(weapon: Vector, armor: Vector, rings: tuple[Vector, Vector]) -> tuple[Vector, int]:
    stats: list[Vector] = [weapon, armor, rings[0], rings[1]]
    totalCost: int = 0
    totalDmg, totalArm = 0, 0 
    for cost, dmg, arm in stats:
        totalCost += cost 
        totalDmg += dmg 
        totalArm += arm
    return (100, totalDmg, totalArm), totalCost

if __name__ == '__main__':
    do(solve, 15, 21)

'''
Solve:
- Represent the weapons, armor, and rings as a tuple of 3 ints: (cost, dmg, armor)
- For armor and ring list, add a (0,0,0) tuple to represent no armor and no ring
- Get the Cartesian product of the weapons, armors, and combinations of 2 rings
- For each (weapon, armor, rings) combo, build your player stats and get the total cost:
  sum up the damage and armor stats from the items, and the player starts at 100hp
- Simulate the game using the player stats vs the opponent stats:
    - The net damage of player and opponent = own damage - opp armor
    - We get max of the damage vs 1, so that if the net damage becomes 0 or negative, we still deal 1 dmg
    - Start with player's turn, then they alternate
    - On the player's turn to attack, reduce the opponent's hp by the player's net damage
    - On the opponet's turn to attack, reduce the player's hp by the opponent's net damage
    - After each turn, check if the hp of attacked player <= 0 = attacker wins
- If the player wins, update the min cost  (Part 1)
- If the player loses, update the max cost (Part 2)
'''