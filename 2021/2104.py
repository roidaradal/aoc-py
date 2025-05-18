# Advent of Code 2021 Day 04
# John Roy Daradal 

from aoc import *

class Bingo:
    def __init__(self, card: list[list[int]]):
        self.card = card 
        self.rows = len(card)
        self.cols = len(card[0])
        self.marked: dict[coords,bool] = {}
        self.lookup: dict[int,coords]  = {}
        for row, line in enumerate(card):
            for col, number in enumerate(line):
                c = (row,col)
                self.lookup[number] = c
                self.marked[c] = False

    def mark(self, number: int):
        if number in self.lookup:
            c = self.lookup[number]
            self.marked[c] = True 

    @property
    def hasWon(self) -> bool:
        for row in range(self.rows):
            if all(self.marked[(row,c)] for c in range(self.cols)): 
                return True 
        for col in range(self.cols):
            if all(self.marked[(r,col)] for r in range(self.rows)):
                return True        
        return False
    
    @property 
    def score(self) -> int:
        unmarked = [c for c,marked in self.marked.items() if not marked]
        return sum(self.card[row][col] for row,col in unmarked)

def data(full: bool) -> tuple[list[int], list[Bingo]]:
    lines = readLines(21, 4, full)
    numbers = toIntList(lines[0], ',')
    cards, card = [], []
    for line in lines[2:]:
        if line == '':
            cards.append(Bingo(card))
            card = []
        else:
            card.append(toIntList(line, None))
    cards.append(Bingo(card))
    return (numbers, cards)

def part1():
    numbers, cards = data(full = True)
    playBingo(numbers, cards, 1)

def part2():
    numbers, cards = data(full = True)
    playBingo(numbers, cards, len(cards))
    
def playBingo(numbers: list[int], cards: list[Bingo], targetWinnerCount: int):
    winners = set()
    for number in numbers:
        for player, card in enumerate(cards):
            if player in winners: continue 

            card.mark(number)
            if card.hasWon:
                winners.add(player)
            if len(winners) == targetWinnerCount:
                score = number * card.score 
                print(score)
                return

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
PlayBingo:
- In Part 1, targetWinnerCount = 1 so play ends once a winner is found
- In Part 2, targetWinnerCount = len(cards), so last winner's score is output
- To simulate Bingo game, go through the numbers in order
- For each card, mark the number if it is in the card 
- After marking a card, check if it has won; if it has, add it to winners set 
- If target number of winners is reached, output score computed by the last number drawn * cardScore 

Bingo:
- Store grid of card numbers and store the number of rows and cols 
- marked is a dictionary that maps if number at coords is marked (already drawn)
- lookup maps the number => coords for easily lookup during marking 
- When marking a card with a number, check if number is in lookup; if it is, get the coords and mark coords as True 
- To check if card has won, check if any row or column is all marked True 
- To compute the card's score, get the unmarked coords and sum up their corresponding card numbers
'''