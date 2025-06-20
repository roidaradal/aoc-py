# Advent of Code 2018 Day 09
# John Roy Daradal 

from aoc import *

class Marble:
    def __init__(self, value: int):
        self.value = value 
        self.next: Marble = self
        self.prev: Marble = self

def data(full: bool) -> int2:
    line = readFirstLine(18, 9, full)
    p = line.split()
    return int(p[0]), int(p[-2])

def solve() -> Solution:
    players, lastMarble = data(full=True)

    # Part 1
    score1 = maxScore(players, lastMarble)
    
    # Part 2
    score2 = maxScore(players, lastMarble * 100)

    return newSolution(score1, score2)

def maxScore(players: int, lastMarble: int) -> int:
    score = [0 for _ in range(players)]
    player = 0
    curr = Marble(0)

    for m in range(1, lastMarble+1):
        if m % 23 == 0:
            prev7 = curr 
            for _ in range(7): prev7 = prev7.prev
            score[player] += m + prev7.value 
            # Remove prev7
            prev = prev7.prev 
            nxt  = prev7.next
            prev.next = nxt 
            nxt.prev  = prev 
            curr = nxt
        else:
            marble = Marble(m)
            next1 = curr.next 
            next2 = next1.next 
            next1.next = marble 
            marble.prev = next1 
            next2.prev = marble 
            marble.next = next2 
            curr = marble 
        player = (player + 1) % players 
    return max(score)

if __name__ == '__main__':
    do(solve, 18, 9)

'''
Solve:
- Start with all players score = 0 
- Go through each marbles from 1 to lastMarble, using current number as marble's value
- Increment the player counter at each turn (with wrap-around), so each player get their turn
- Use a DLL node for easy inserting / deleting of next/previous nodes
- Normally, we add a new marble with current value
- Insert it between the current marble's next and the one after that; make the new marble the current
- If marble's value is divisible by 23, we don't add a new marble
- We add that value to the current player's score, and get the marble 7 spots to the left
- We remove the prev7 marble and add its value to the current player's score too
- The new current marble is the removed marble's next marble
- For Part 2, last marble is 100x larger
'''