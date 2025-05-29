# Advent of Code 2023 Day 07
# John Roy Daradal 

from aoc import *
from functools import cmp_to_key

CARDS = 'AKQJT98765432'
power = {}

def data(full: bool) -> list[strInt]:
    def fn(line: str) -> strInt:
        return lineStrInt(line, None)
    return [fn(line) for line in readLines(23, 7, full)]

def part1():
    hands = data(full=True)
    computePower()

    hands = sorted(hands, key=cmp_to_key(compareHands))
    items = list(enumerate(hands))
    total = getTotal(items, score)
    print(total)

def part2():
    hands = data(full=True)
    computePower()
    power['J'] = 1 # Joker

    hands = sorted(hands, key=cmp_to_key(compareHands2))
    items = list(enumerate(hands))
    total = getTotal(items, score)
    print(total)

def computePower():
    value = 14 
    for card in CARDS:
        power[card] = value 
        value -= 1

def score(pair: tuple[int, strInt]) -> int:
    i, (_, bid) = pair 
    return (i+1) * bid

def compareHands(hand1: strInt, hand2: strInt) -> int:
    cards1, cards2 = hand1[0], hand2[0]
    score1 = computeScore(cards1)
    score2 = computeScore(cards2)
    if score1 == score2:
        return compareCards(cards1, cards2)
    else:
        return score1 - score2

def compareHands2(hand1: strInt, hand2: strInt) -> int:
    cards1, cards2 = hand1[0], hand2[0]
    score1 = computeScore2(cards1)
    score2 = computeScore2(cards2)
    if score1 == score2:
        return compareCards(cards1, cards2)
    else:
        return score1 - score2
    
def compareCards(cards1: str, cards2: str) -> int:
    for i in range(len(cards1)):
        card1, card2 = cards1[i], cards2[i]
        if card1 != card2:
            return power[card1] - power[card2]
    return 0

def computeScore(cards: str) -> int:
    group = groupHand(cards)
    category = tuple(sorted(group.values(), reverse=True))
    return categoryScore(category)

def computeScore2(cards: str) -> int:
    group = groupHand(cards)
    if 'J' in group:
        values = [v for k,v in group.items() if k != 'J']
        if len(values) == 0: values = [0] # in case all J 
        values = sorted(values, reverse = True)
        values[0] += group['J'] # add Joker to the max count
        category = tuple(values)
    else:
        category = tuple(sorted(group.values(), reverse=True))
    return categoryScore(category)

def groupHand(cards: str) -> dict[str,int]:
    group: dict[str,int] = defaultdict(int)
    for card in cards:
        group[card] += 1
    return group

def categoryScore(category: tuple) -> int:
    if category == (1,1,1,1,1): # High Card
        return 1 
    elif category == (2,1,1,1): # One Pair
        return 2 
    elif category == (2,2,1): # Two Pair 
        return 3
    elif category == (3,1,1): # Three-of-a-Kind
        return 4 
    elif category == (3,2): # Full House
        return 5
    elif category == (4,1): # Four-of-a-Kind
        return 6 
    elif category == (5,): # Five-of-a-Kind
        return 7
    else:
        return 0
    
if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Assign card power from A=14, K=13, ... 3, 2
- Sort the hands by using the standard way 
    - Compare the score of cards1 and cards2 
    - For the card hand's score, group the hand by numbers and 
      get the corresponding score for that hand (high card, 1P, 2P, 3OAK, FH, 4OAK, 5OAK)
    - If equal, compare their cards: compare the first cards, 2nd, and so on
    - If we find differing cards, compare their powers
- Compute the score of a hand by multiplying its rank (order) and bid
- Output the total score of the hands

Part2:
- Assign card powers similar to Part 1, but change J's power to 1 (Joker)
- Sort the hands using the custom version (using Joker)
    - Compare the score of cards1 and cards2: if no Joker, similar to Part 1
    - If has Joker, add the J count to the maximum count to improve the hand 
    - Get the category score of the improved hand
    - If equal, compare their cards, similar to Part 1
- Compute the scores of hands similar to Part 1, and output the total score
'''