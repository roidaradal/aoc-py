# Advent of Code 2019 Day 22
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[strInt]:
    recipe: list[strInt] = []
    for line in readLines(19, 22, full):
        if line == 'deal into new stack':
            recipe.append(('deal', 0))
        elif line.startswith('deal with increment'):
            step = int(splitStr(line, None)[-1])
            recipe.append(('deal', step))
        elif line.startswith('cut'):
            step = int(splitStr(line, None)[-1])
            recipe.append(('cut', step))
    return recipe

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    recipe = data(full=True)
    n = 10007 
    goal = 2019 

    deck = list(range(10007))
    for cmd, step in recipe:
        if cmd == 'deal' and step == 0: 
            # deal into new stack = reverse
            deck = deck[::-1]
        elif cmd == 'cut':
            # cut N cards
            deck = deck[step:] + deck[:step]
        elif cmd == 'deal':
            # deal with increment
            deck2 = [-1] * n
            idx = 0
            for card in deck:
                deck2[idx] = card 
                idx = (idx + step) % n
            deck = deck2

    idx = deck.index(goal)        
    return idx

def part2() -> int:
    recipe = data(full=True)
    idx = 2020
    n = 119315717514047
    r = 101741582076661

    # Modular inverse, using Euler's theorem
    def modinv(x: int) -> int:
        return pow(x, n-2, n)
    
    # Express steps in the form y = a*x + b 
    # Since 3 steps are linear functions, they are composable
    # y = number at idx x
    # a = increment: diff bet 2 adjacent numbers    (initial 1)
    # b = offset: first number in the sequence      (initial 0)
    a, b = 1, 0
    for cmd, step in recipe:
        if cmd == 'deal' and step == 0:
            # deal into new stack = reverse
            # increment becomes -increment (from up <=> down)
            # offset = shift 1 left % N (e.g. from 0 to N-1)
            a = -a % n 
            b = (b + a) % n 
        elif cmd == 'cut':
            # cut cards 
            # update the offset = step becomes the front
            # to get step item, use (increment * step) 
            b = (b + (a * step)) % n 
        elif cmd == 'deal':
            # deal with increment
            # update increment = multiply by modular inverse of step
            a = (a * modinv(step)) % n 
    
    # Increment = a^r (numRounds) % n
    increment = pow(a, r, n)
    # Offset = 0 + b * (1 + a + a^2 + ... + a^r)
    # Geometric series
    offset = (b * (1-increment) * modinv((1-a) % n)) % n 

    out = ((idx * increment) + offset) % n 
    return out

if __name__ == '__main__':
    do(solve, 19, 22)

'''
Part1:
- Start with the deck of cards from 0-10,006
- Go through the shuffle steps in order:
    - If deal 0 (deal into new stack), just reverse the deck 
    - If cut N cards:
        - If N: take the first N cards to the back => deck[N:] + deck[:N]
        - If -N: take the last N cards to the front => deck[-N:] + deck[:-N]
        - Either way, the formula is deck[N:] + deck[:N]
    - If deal with increment N:
        - Create a new deck with empty slots (-1)
        - Starting from idx 0 and incrementing by the step (% deckSize), add
          the cards from the current deck to these positions
        - New deck becomes the current deck
- Output the index of card 2019 

Part2:
- Let N = deck size of 119315717514047
- The 3 shuffle steps can be expressed in linear equations: y = a*x + b
- Since the 3 functions are linear, they are composable 
- y = number at idx x
- a = increment: the difference between 2 adjacent numbers, initially 1
- b = offset: the first number in the sequence, initially 0
- Go through the shuffle steps in order, to create the final composed function:
- If deal 0 (deal into new stack), we reverse the deck:
    - We negate the increment (e.g. goes from 1 to -1) % N
    - Also update the offset: b = (b+a) % N
- If cut S (step) cards, we make S become the front 
    - Update offset to become S; to get item at S => a * S 
    - b = (b + (a * S)) % N
- If deal with increment S (step):
    - Update the increment, multiply by the modular inverse of step
    - a = (a * modinv(step)) % N
    - Modular inverse can be implemented in Python using pow(x, N-2, N)
- We now have the value for increment (a) and offset (b) for one round of the shuffle step
- Compute the increment and offset for the repeated number of rounds, r = 101741582076661
- Increment = a^r % N = pow(a, r, N)
- Offset = 0 + b * (1 + a^1 + a^2 + ... + a^r) = geometric series
- Offset = (b * (1-increment) * modinv((1-a) % n)) % n 
- To get the item at index 2020: ((2020 * increment) + offset) % N
- Reference:
  https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbnkaju/
'''