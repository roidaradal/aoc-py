# Advent of Code 2015 Day 15
# John Roy Daradal 

from aoc import *

attr = tuple[int,int,int,int,int]

def data(full: bool) -> dict[str,attr]:
    m: dict[str,attr] = {}
    for line in readLines(15, 15, full):
        key, tail = splitStr(line, ':')
        a,b,c,d,e = [int(x.split()[1]) for x in splitStr(tail, ',')]
        m[key] = (a,b,c,d,e)
    return m

def solve():
    m = data(full=True)

    # Part 1
    maxScore = findBestScore(m, 0)
    print(maxScore)

    # Part 2 
    maxScore = findBestScore(m, 500)
    print(maxScore)

def findBestScore(m: dict[str,attr], goal: int) -> int:
    i1, i2, i3, i4 = sorted(m.keys())
    maxScore = 0
    for a in range(101):
        for b in range(101):
            if a + b > 100: continue 
            for c in range(101):
                if a + b + c > 100: continue
                for d in range(101):
                    if a + b + c + d != 100: continue 
                    combo = {i1: a, i2: b, i3: c, i4: d}
                    if goal > 0 and calories(combo, m) != goal: continue
                    maxScore = max(maxScore, comboScore(combo, m))
    return maxScore

def comboScore(combo: dict[str,int], m: dict[str,attr]) -> int:
    total = [0, 0, 0, 0]
    for k, amt in combo.items():
        for i in range(4):
            total[i] += m[k][i] * amt 
    a,b,c,d = [max(0,x) for x in total]
    return a*b*c*d

def calories(combo: dict[str,int], m: dict[str,attr]) -> int:
    total = 0 
    for k, amt in combo.items():
        total += m[k][-1] * amt 
    return total

if __name__ == '__main__':
    do(solve)

'''
Part1:
- Try out combinations of amounts for ingredient 1, 2, 3, 4, from 0 to 100
- If a partial combination exceeds 100, skip immediately 
- Make sure the combination of ingredient amounts equal to 100
- Compute the comboScore of the combination:
    - Start with totals of the first 4 attributes set to 0 
    - For each amount in the combo, increment the attribute total by the attribute value * amount 
    - Ensure totals don't go below 0 
    - Score is the product of the 4 totals
- Output the max score

Part2:
- Similar to Part 1, but only consider combos whose total calorie count is 500 
- Compute the calorie total similar to comboScore, but only using the last attribute (calorie)
'''