# Advent of Code 2018 Day 15
# John Roy Daradal 

from aoc import *

class Result:
    def __init__(self): 
        self.score: int = 0 
        self.winner: str = ''
        self.initial: int = 0 
        self.left: int = 0

class Combat:
    def __init__(self, grid: list[list[str]]):
        self.grid = grid 
        self.players: list[Player] = []
        self.round: int = 0
        self.initial: dict[str,int] = {'G': 0, 'E': 0}

    @property 
    def activePlayers(self):
        return [p for p in self.players if p.isAlive]
    
    @property 
    def sortedPlayers(self):
        return sorted(self.activePlayers, key=lambda p: p.pos)
    
    @property 
    def result(self) -> Result:
        r = Result()
        total = 0
        for player in self.activePlayers:
            total += player.hp 
            r.left += 1 
            r.winner = player.name 
        r.score = total * self.round 
        r.initial = self.initial[r.winner]
        return r

class Player:
    combat: Combat|None = None 
    DMG = {'E': 3, 'G': 3}

    def __init__(self, name: str, pos: coords):
        self.name = name 
        self.opp = 'E' if name == 'G' else 'G'
        self.pos = pos 
        self.hp = 200 
        self.isAlive = True
    
    @property 
    def dmg(self) -> int:
        return self.DMG[self.name]

    @property 
    def vulnerable(self) -> set[coords]:
        if self.combat is None: return set()
        grid = self.combat.grid
        near = surround4(self.pos)
        invalid = ('#', self.name) # wall or same kind 
        return set((y,x) for y,x in near if grid[y][x] not in invalid)
    
    def moveToEnemy(self, attackSpots: set[coords]):
        if self.combat is None: return 

        # Filter: only consider reachable attack spots 
        reachableSpots = findReachable(self.combat, self.pos)
        options = [(v,k) for k,v in reachableSpots.items() if k in attackSpots]

        # If no reachable spot, end turn 
        if len(options) == 0: return 

        # Get nearest attack spot, tie-breaker: reading order 
        attackSpot = min(options)[1]

        # Get player's available moves (UDLR)
        near = surround4(self.pos)
        moveSpots = [(y,x) for y,x in near if self.combat.grid[y][x] == '.']

        # Get shortest path to attackSpot 
        goalPath = findReachable(self.combat, attackSpot)
        options = [(v,k) for k,v in goalPath.items() if k in moveSpots]
        nxt = min(options)[1]

        # Move to next coords 
        y,x = self.pos
        self.combat.grid[y][x] = '.' # vacate current position 
        y,x = nxt 
        self.combat.grid[y][x] = self.name 
        self.pos = nxt
    
    def attack(self):
        if self.combat is None: return 
        # Possible attack points 
        near = surround4(self.pos)
        attackSpots = [(y,x) for y,x in near if self.combat.grid[y][x] == self.opp]
        if len(attackSpots) == 0: return 

        # Choose opponent to attack
        if len(attackSpots) == 1:
            attackPos = attackSpots[0]
            opp = [p for p in self.combat.activePlayers if p.pos == attackPos][0]
        else:
            opps = [p for p in self.combat.activePlayers if p.pos in attackSpots]
            options = [(p.hp, p.pos, p) for p in opps]
            opp = min(options)[2]

        # Attack opponent
        opp.hp -= self.dmg
        if opp.hp <= 0:
            y,x = opp.pos 
            self.combat.grid[y][x] = '.' # remove player from grid 
            opp.isAlive = False

def data(full: bool) -> Combat:
    grid = [list(line) for line in readLines(18, 15, full)]
    combat = Combat(grid)
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == 'G' or char == 'E':
                player = Player(char, (row,col))
                combat.players.append(player)
    return combat

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    combat = data(full=True)
    Player.combat = combat 
    result = simulate(combat)
    return result.score

def part2() -> int:
    dmg = 4 
    score = 0
    while True:
        combat = data(full=True)
        Player.combat = combat 
        Player.DMG = {'G': 3, 'E': dmg}
        result = simulate(combat)
        if result.winner == 'E' and result.left == result.initial:
            score = result.score 
            break
        dmg += 1
    return score

def simulate(combat: Combat) -> Result:
    # Initialize players count 
    for p in combat.players:
        combat.initial[p.name] += 1

    while True:
        stop = False 
        for player in combat.sortedPlayers:
            if not player.isAlive: continue 

            attackSpots, hasOpp = findAttackSpots(combat, player.name)
            if not hasOpp:
                stop = True 
                break 

            # not yet in place to attack = move 
            if player.pos not in attackSpots:
                player.moveToEnemy(attackSpots)

            # in range to attack 
            if player.pos in attackSpots:
                player.attack()

        if stop: break
        combat.round += 1

    return combat.result

def findAttackSpots(combat: Combat, name: str) -> tuple[set[coords], bool]:
    opps = [p for p in combat.activePlayers if p.opp == name]
    spots: set[coords] = set()
    for opp in opps:
        spots = spots.union(opp.vulnerable)
    hasOpp = len(opps) > 0
    return spots, hasOpp

def findReachable(combat: Combat, curr: coords) -> dict[coords,int]:
    reach: dict[coords,int] = {}
    q: list[tuple[coords,int]] = [(curr, 0)]
    while len(q) > 0:
        curr, steps = q.pop(0)
        if curr in reach: continue 
        reach[curr] = steps 
        for nxt in surround4(curr):
            y,x = nxt 
            if nxt in reach or combat.grid[y][x] != '.': continue 
            q.append((nxt, steps+1))
    return reach

if __name__ == '__main__':
    do(solve, 18, 15)

'''
Simulate:
- Initialize players' count (for Part 2 checking if no elf dies)
- Repeat until one side has no more opponents to attack, incrementing the round counter
- Alive players attack in reading order (row-col)
- Check if there are still opponents to attack (condition for stopping)
- Find the current player's spots to attack: union of opponents' vulnerable spots
    - Player's vulnerable spots = surround4 (UDLR) but spot is not a wall (#) or occupied by ally
- If current player's position is not yet in any of the attack spots, move the player towards the enemy:
    - First, find the reachable spots from the player's position using BFS (can only move UDLR for next step)
    - End turn if no reachable attack spots 
    - Get the nearest reachable attack spot, tie-breaker: reading order 
    - Get the current player's available moves: surround4 (UDLR) if spot is open (.)
    - Use BFS to figure out the reachable moveSpots and the shortest path to it 
    - Choose the moveSpot that has the shortest path to the attackSpot
    - Vacate the player's old position in the grid (change to .) and move to the nextSpot 
    - Update the current player's position to the nextSpot
- If the current player is in one of the attack spots, the current player attacks:
    - Find the possible attack points: UDLR but spot is occupied by opponent
    - If only one possible option, this is the attacked opponent 
    - If multiple options, choose opponent with lowest HP, tie-breaker: reading order
    - Attacking opponent reduces its HP with player's damage 
    - If opp's HP falls becomes 0 or less, remove player from grid and opp dies

Solve:
- For Part 1, simulate the combat using dmg=3 for both E and G
- For Part 2, start with dmg=4 for E and increase until we find the damage value that 
  ensures the elves win and no elf dies (final count is same as initial count)
- Output the score of the combat: total HP of players left * round number
'''