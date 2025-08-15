# Advent of Code 2020 Day 22
# John Roy Daradal 

from aoc import *

State = tuple[int,...]

def data(full: bool) -> tuple[list[int], list[int]]:
    cards: dict[int, list[int]] = {}
    player = 0
    for line in readLines(20, 22, full):
        if line == 'Player 1:':
            player = 1 
            cards[player] = []
        elif line == 'Player 2:':
            player = 2 
            cards[player] = []
        elif line == '': 
            continue 
        else:
            cards[player].append(int(line))
    return cards[1], cards[2]

def solve() -> Solution:
    # Part 1
    p1, p2 = data(full=True)
    score1 = playGame(p1, p2)

    # Part 2 
    p1, p2 = data(full=True)
    _, cards = playRecursiveGame(p1, p2)
    score2 = computeScore(cards)

    return newSolution(score1, score2)

def computeScore(cards: list[int]) -> int:
    limit = len(cards)
    total = 0
    for i,card in enumerate(cards):
        total += card * (limit-i)
    return total

def playGame(p1: list[int], p2: list[int]) -> int:
    while True:
        v1 = p1.pop(0)
        v2 = p2.pop(0)
        if v1 > v2:
            p1 += [v1, v2]
            if len(p2) == 0:
                return computeScore(p1)
        else:
            p2 += [v2, v1]
            if len(p1) == 0:
                return computeScore(p2)
            
def playRecursiveGame(p1: list[int], p2: list[int]) -> tuple[int, list[int]]:
    done: list[State] = []
    while True:
        state = gameState(p1, p2)
        if state in done:
            return (1, p1)
        done.append(state)

        v1 = p1.pop(0)
        v2 = p2.pop(0)
        winner = 0
        if len(p1) >= v1 and len(p2) >= v2:
            # both players have enough cards to play a new game
            np1 = [x for x in p1[:v1]]
            np2 = [x for x in p2[:v2]]
            winner, _ = playRecursiveGame(np1, np2)
        else:
            winner = 1 if v1 > v2 else 2
        
        if winner == 1:
            p1 += [v1, v2]
            if len(p2) == 0:
                return (1, p1)
        elif winner == 2:
            p2 += [v2, v1]
            if len(p1) == 0:
                return (2, p2)

def gameState(p1: list[int], p2: list[int]) -> State:
    state = p1 + [-1] + p2 
    return tuple(state)

if __name__ == '__main__':
    do(solve, 20, 22)

'''
Part1:
- Given the two players' cards, play the game, and output the score of the winning player
    - Each player takes out their first card; compare the two cards, higher card = wins 
    - Place the 2 cards (with winner's card on top), to the back of winning player's deck
    - Check if the loser's deck becomes empty; if it does, end the game and compute the winner's score
- Score of remaining cards is cardValue * (len(cards)-idx); factor is descending from len(cards) to 1
    - Example: if there are 5 cards: 3,1,4,5,2
    - 3*5 + 1*4 + 4*3 + 5*2 + 2*1

Part2:
- Given the two players' cards, play the recursive game, and output the score of the winning player
- Remember the state of player1 and player2's decks (in order) before the start of each round
- If we have seen this state before, this game automatically makes player1 the winner
- Otherwise, we remove the players' top cards and compare them, similar to Part 1
- If the number of remaining cards of each player is >= the value of card recently drawn, 
  both players have enough cards to play a new game, so we recursively start a new game and note the winner of that
- In the new recursive game, we copy the number of cards specified by the drawn card for each player
- If not, at least one player doesn't have enough cards to recurse, so we compare their top cards as usual
- We still place the 2 cards (winner's card on top) to the back of winning player's deck
- We also check if the loser's deck becomes empty, as this will stop the game 
'''