# Advent of Code 2023 Day 04
# John Roy Daradal 

from aoc import *

Game = tuple[set[int], set[int]] # winners, numbers

def data(full: bool) -> list[Game]:
    def fn(line: str) -> Game:
        tail = line.split(':')[1]
        winners, numbers = splitStr(tail, '|')
        winners = toIntList(winners, None)
        numbers = toIntList(numbers, None)
        return (set(winners), set(numbers))
    return [fn(line) for line in readLines(23, 4, full)]

def part1():
    games = data(full=True) 
    total = getTotal(games, score)
    print(total)

def part2():
    games = data(full=True)
    total = countTotalCards(games)
    print(total) 

def score(game: Game) -> int:
    winners, numbers = game 
    common = len(winners.intersection(numbers))
    return 0 if common == 0 else 2 ** (common-1)

def countTotalCards(games: list[Game]) -> int:
    limit = len(games)
    count = {i:1 for i in range(limit)}
    for i,game in enumerate(games):
        winners, numbers = game 
        common = len(winners.intersection(numbers))
        for j in range(common): 
            k = i + j + 1 
            if k < limit:
                count[k] += count[i]
    return sum(count.values())

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Compute the total score of the card games
- Count the winning numbers (get intersection)
- Since the point of the card is 1, 2, 4, 8, ... (double the previous),
  use 2 ** (common-1) if there are winning cards

Part2:
- Start by having count = 1 for each card 
- For each card, compute the number of winning numbers = X
- Increase the count of the succeeding X cards by the number of current cards
- Return the total number of cards
'''