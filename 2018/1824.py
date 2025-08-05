# Advent of Code 2018 Day 24
# John Roy Daradal 

from aoc import *

class Group:
    def __init__(self, line: str):
        amplifier = ''
        if '(' in line:
            start = line.index('(')
            end = line.index(')') + 1
            amplifier = line[start+1:end-1] # remove parens
            line = line[:start] + line[end:]

        p = splitStr(line, None)
        self.boost = 0
        self.units = int(p[0])
        self.hp = int(p[4])
        self.initiative = int(p[-1])
        self.attackDamage = int(p[-6])
        self.attackType = p[-5]
        self.amplifier: dict[str, int] = defaultdict(lambda: 1)
        if amplifier != '':
            for phrase in splitStr(amplifier, ';'):
                head, tail = splitStr(phrase, 'to')
                factor = 0 if head == 'immune' else 2 # weak
                for kind in splitStr(tail, ','):
                    self.amplifier[kind] = factor

    @property 
    def isActive(self) -> bool:
        return self.units > 0
    
    @property 
    def power(self) -> int:
        if self.units <= 0: return 0
        return self.units * self.totalDamage
    
    @property 
    def totalDamage(self) -> int:
        return self.attackDamage + self.boost
    
    @property 
    def selectionRank(self) -> int2:
        return (self.power, self.initiative)
    
    def takeDamage(self, power: int, attackType: str) -> int:
        preUnits = self.units
        totalDamage = power * self.amplifier[attackType]
        unitsKilled = totalDamage // self.hp 
        self.units -= unitsKilled
        return min(unitsKilled, preUnits)

Groups = dict[str, dict[int, Group]]
immune, infect = 'immune', 'infect'

def data(full: bool) -> Groups:
    groups: Groups = {
        immune : {},
        infect : {},
    }
    gid, key = 0, ''
    for line in readLines(18, 24, full):
        if line == 'Immune System:':
            key, gid = immune, 0
        elif line == 'Infection:':
            key, gid = infect, 0
        elif line == '': 
            continue 
        else:
            groups[key][gid] = Group(line)
            gid += 1
    return groups

def solve() -> Solution:
    # Part 1 
    winner, alive1 = simulateBattle(boost=0)

    # Part 2
    alive2 = 0
    start, end = 0, 5000
    while True:
        mid = start + ((end-start) // 2)
        winner, alive2 = simulateBattle(boost=mid)
        if winner == immune: 
            end = mid 
        elif winner == infect:
            start = mid+1
        else: # draw
            break
        if end-start <= 2: 
            break 
    for boost in range(start, end):
        winner, alive2 = simulateBattle(boost)
        if winner == immune:
            break 

    return newSolution(alive1, alive2)

def simulateBattle(boost: int) -> strInt:
    groups = data(full=True)
    active: dict[str,int] = {k: len(v) for k,v in groups.items()}

    for group in groups[immune].values():
        group.boost = boost 

    while all(x > 0 for x in active.values()):
        targetOf: dict[str, dict[int, int]] = {}
        targetOf[immune] = selectTarget(groups, immune, infect)
        targetOf[infect] = selectTarget(groups, infect, immune)

        attackers: list[tuple[int, str, int]] = []
        for side in [immune, infect]:
            for atkID in targetOf[side]:
                group = groups[side][atkID]
                attackers.append((group.initiative, side, atkID))

        totalKilled = 0
        for _, side, atkID in sorted(attackers, key=lambda t: t[0], reverse=True):
            opp = immune if side == infect else infect
            atkGroup = groups[side][atkID]
            defID = targetOf[side][atkID]
            defGroup = groups[opp][defID]
            killed = defGroup.takeDamage(atkGroup.power, atkGroup.attackType)
            totalKilled += killed
            if not defGroup.isActive:
                active[opp] -= 1

        if totalKilled == 0: # reached a stalemate = draw
            return 'draw', 0

    winner = immune if active[immune] > 0 else infect 
    alive = sum(g.units for g in groups[winner].values() if g.isActive)
    return winner, alive

def selectTarget(groups: Groups, attacker: str, defender: str) -> dict[int,int]:
    targetOf: dict[int, int] = {}
    options: list[int] = [k for k in groups[defender].keys() if groups[defender][k].isActive]
    entries: list[tuple[Group, int]] = [(g,i) for i,g in groups[attacker].items() if g.isActive]
    for atkGroup, atkID in sorted(entries, key=lambda e: e[0].selectionRank, reverse=True):
        choices: list[tuple[int3, int]] = []
        for defID in options:
            defGroup = groups[defender][defID]
            dmgAmount = atkGroup.power * defGroup.amplifier[atkGroup.attackType]
            if dmgAmount == 0: continue 
            choices.append(((dmgAmount, defGroup.power, defGroup.initiative), defID))
        if len(choices) == 0: continue 
        _, defID = max(choices, key=lambda t: t[0])
        targetOf[atkID] = defID 
        options.remove(defID)
    return targetOf

if __name__ == '__main__':
    do(solve, 18, 24)

'''
Part1:
- Create the immune and infection groups from input; add group IDs for identity
- These are the group's dynamic properties:
    - isActive: number of alive units > 0 
    - power: if no more alive units, power = 0; otherwise, no. of units * totalDamage
    - totalDamage: attackDamage + attackBoost
    - selectionRank: (power, initiative), prioritize power, then use initiative as tie-breaker
- Process group's attack amplifiers: x0 if immune, x2 if weak (doubled)
- Simulate the battle with 0 attack boost for the immune group:
    - Keep a counter for how many groups are still active for immune and infection
    - Repeat until one side has no more active groups:
    - Select the targets for the immune groups and the infection groups
    - In descending order of initiative from all groups combined, they will attack their selected target group
    - The defending group takes the damage of the attacking group, based on their attack type 
    - The total damage a defending group takes is the attacking group's power * amplifier[attackType]
    - The no. of units killed for the defending group is the totalDamage // unitHP (extra damage that cannot fully kill 1 unit is ignored)
    - If there are no more active units in the defending group, it becomes inactive, and we update the active count for this side
    - Keep track of the total killed in this round; if there are none, reached a stalemate = return draw
    - After exiting the loop, if a winner emerges, we return the winning side and the total number of units for the active groups left
- For target selection of attacker to defender:
    - Defender options are groups that are still active
    - In descending selectionRank order of the attackers, it will examine how much damage it will cause to a defending group
    - If there are no groups it can attack, then it doesn't attack 
    - Otherwise, it will select the defending group where it will inflict the most damage
    - For tie-breakers, use the defending group's power first, then the initiative

Part2:
- Find the minimum attack boost value that will allow the immune group to win
- Use binary search to find this value: start with range 0 - 5000
- Simulate the battle with the middle as the attack boost:
    - If the immune group wins, then we can examine the lower side = set end = mid 
    - If the infect group wins, then we can examine the higher side = set start = mid+1
    - If draw, we break out of the loop, and do linear search after that
    - If range is only length 2 or less, we also do linear search
- Return the total number of units alive after we find the minimum attack boost that allows
  the immune side to win
'''