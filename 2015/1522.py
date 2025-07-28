# Advent of Code 2015 Day 22
# John Roy Daradal 

import heapq
from aoc import *

# you: (hp, mana)
# opp: (hp, dmg)
# spell : (manaCost, dmg, hpRegen)
# timer : (shield, poison, recharge)
# effect: (manaCost, numTurns, effectType)

ARMOR, DMG, MANA = 0, 1, 2

spells: list[int3] = [
    (53, 4, 0), # missile
    (73, 2, 2), # drain
]

effects: list[int3] = [
    (113, 6, ARMOR),
    (173, 6, DMG),
    (229, 5, MANA),
]

effectStats: dict[int, int] = {
    ARMOR   : 7, 
    DMG     : 3,
    MANA    : 101,
}

def data(full: bool) -> int2:
    values: list[int] = []
    for line in readLines(15, 22, full):
        tail = splitStr(line, ':')[1]
        values.append(int(tail))
    hp, dmg = values 
    return (hp, dmg)

def solve() -> Solution:
    oppHP, oppDmg = data(full=True)
    State.oppDmg = oppDmg

    # Part 1
    mana1 = findMinMana(oppHP, False)

    # Part 2
    mana2 = findMinMana(oppHP, True)
    
    return newSolution(mana1, mana2)
    
def findMinMana(oppHP: int, loseHP: bool) -> int:
    you: int2 = (50, 500)
    timer: int3 = (0, 0, 0)

    pq: list[State] = []
    state = State(0, you, oppHP, timer)
    heapq.heappush(pq, state)
    
    while len(pq) > 0:
        state = heapq.heappop(pq)
        if state.hasWon:
            return state.manaUsed
        for branch in branchState(state, loseHP):
            if branch.isFinished and not branch.hasWon: continue # skip losing branches
            heapq.heappush(pq, branch)
    return 0

class State:
    oppDmg = 0 

    def __init__(self, manaUsed: int, you: int2, oppHP: int, timer: int3):
        self.manaUsed = manaUsed 
        self.manaLeft = you[1]
        self.youHP = you[0]
        self.oppHP = oppHP
        self.timer = timer
        self.spellArmor = 0
        self.isFinished = self.youHP <= 0 or self.oppHP <= 0 
        self.hasWon = self.oppHP <= 0

    def __lt__(self, other) -> bool:
        return self.manaUsed < other.manaUsed
        
    def applyEffects(self):
        newTimer: list[int] = []
        self.spellArmor = 0
        for i, timeLeft in enumerate(self.timer):
            if timeLeft > 0:
                if i == ARMOR:
                    # Activate armor
                    self.spellArmor = effectStats[ARMOR]
                elif i == DMG:
                    # Reduce opponent HP by dmg
                    self.oppHP -= effectStats[DMG]
                elif i == MANA:
                    # Restore mana 
                    self.manaLeft += effectStats[MANA]
                timeLeft -= 1
            newTimer.append(timeLeft)
        time1, time2, time3 = newTimer
        self.timer = (time1, time2, time3)

    # Opponent's turn
    def nextState(self):
        self.applyEffects()
        if self.checkGameEnd(): return

        oppDmg = max(self.oppDmg - self.spellArmor, 1)
        self.youHP -= oppDmg
        self.checkGameEnd()

    def checkGameEnd(self) -> bool:
        if self.oppHP <= 0:
            self.isFinished = True 
            self.hasWon = True 
            return True 
        elif self.youHP <= 0:
            self.isFinished = True 
            self.hasWon = False 
            return True 
        else:
            return False

def branchState(state: State, loseHP: bool) -> list[State]:
    if loseHP:
        state.youHP -= 1 
    if state.checkGameEnd(): return [state]

    state.applyEffects()
    if state.checkGameEnd(): return [state]

    branches: list[State] = []

    # Try spells you can afford to cast
    for manaCost, spellDmg, hpRegen in spells:
        if manaCost > state.manaLeft: continue # skip if cannot afford to cast spell
        manaUsed = state.manaUsed + manaCost 
        manaLeft = state.manaLeft - manaCost
        youHP = state.youHP + hpRegen 
        oppHP = state.oppHP - spellDmg 

        branch = State(manaUsed, (youHP, manaLeft), oppHP, state.timer)
        if branch.isFinished:
            if branch.hasWon:  
                return [branch]
            else:
                continue

        branch.nextState()
        if branch.isFinished:
            if branch.hasWon: 
                return [branch]
        else:
            branches.append(branch)

    # Try effects you can afford to cast and is not currently active
    for manaCost, numTurns, effect in effects:
        if manaCost > state.manaLeft: continue # skip if cannot afford to cast effect
        timer1, timer2, timer3 = state.timer
        if effect == ARMOR:
            if timer1 > 0: continue # skip if armor effect is active
            timer1 = numTurns
        elif effect == DMG:
            if timer2 > 0: continue # skip if dmg effect is active
            timer2 = numTurns
        elif effect == MANA:
            if timer3 > 0: continue # skip if mana effect is active
            timer3 = numTurns
        
        manaUsed = state.manaUsed + manaCost 
        manaLeft = state.manaLeft - manaCost
        branch = State(manaUsed, (state.youHP, manaLeft), state.oppHP, (timer1, timer2, timer3))
        branch.nextState()
        if branch.isFinished:
            if branch.hasWon:
                return [branch]
        else:
            branches.append(branch)
            
    return branches

if __name__ == '__main__':
    do(solve, 15, 22)

'''
Solve:
- Separate the list of spells and list of effects:
    - Spells are represented by (manaCost, damage, hpRegen)
    - Effects are represented by (manaCost, numTurns, effectType)
    - Keep a separate lookup for effect => effect stat value
- For Part 1, find the minimum mana spent where the player wins
- For Part 2, do the same as in Part 1, but before each player turn, he loses 1 HP
- Start with player at 50 HP with 500 mana, and effect timers set to 0 (no active effects yet)
- Use a priority queue that processes state with minimum manaUsed first
- From the removed state from the pq, check if the state has won: if it has, return the state's manaUsed:
  since we have been processing the least manaUsed first, the first state that wins is what we're looking for 
- If not yet won, branch the state and as long as the branch is not a losing state, we add it to the PQ

State:
- Contains manaUsed, manaLeft, playerHP, opponentHP, effect timers, spellArmor 
  and flags to indicate whether game is finished and if player has won
- We add a function to compare states: use manaUsed: less is better
- CheckGameEnd: checks if the game should end
    - If opponent's HP is at or below 0, game is done, and player has won 
    - If player's HP is at or below 0, game is done, and player has lost 
    - Otherwise, game is not yet done
    - This is called each time we apply an effect or we update player/opponent's HP
- NextState: simulates the opponent's turn
    - Apply effects before the opponent's turn; then check if we need to end the game 
    - If game is not yet done, the opponent damage = max(oppDmg - spellArmor, 1); that is, if the 
      spellArmor makes the damage fall below 1, we will use the floor damage of 1
    - Spell armor is initially 0, that gets updated if the armor effect is active 
    - Reduce the palyer's HP by the opponent damage, and check if we need to end the game
- ApplyEffects: applies the active effects
    - Check each effect timer; skip those that are at 0
    - If timeLeft > 0, the effect is active
    - For armor effect, update the spellArmor to the stats[armor]
    - For damage effect (poison), reduce the opponent's HP by the stats[dmg]
    - For mana effect, increase the manaLeft by stats[mana]
    - Reduce the timer of the active timers by 1

BranchState:
- If loseHP flag is True (Part 2), we decrease the player's HP by 1 at the start and check if game should end 
- Call state.applyEffects to apply the active effects before the player's turn, and check if we need to end game after
- Try spells you can afford to cast:
    - Skip spell if you cannot afford to cast it (manaCost > manaLeft)
    - Update the manaUsed (+manaCost), manaLeft (-manaCost), playerHP (+hpRegen), and opponentHP (-spellDamage)
    - Create a branch state with the updated values; check if that branch is done (no need to continue)
    - If not yet done, simulate the opponent's turn by calling nextState
    - Check if the branch has won: return that branch immediately, otherwise, add it to list of branches to return
- Try effects you can afford to cast, that is not currently active:
    - Skip effect if you cannot afford to cast it (manaCost > manaLeft)
    - Skip effect if it has an active timer
    - Start the effect's timer = numTurns; update the manaUsed and manaLeft (same as in spell)
    - Create a branch state with the updated stats and timers (no need to check end, since we don't have an active spell that updates player/opponent's HP)
    - Call nextState() to simulate the opponent's turn
    - Finally, check if the branch has won: return branch immediately; otherwise, add to list of branches
'''