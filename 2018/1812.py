# Advent of Code 2018 Day 12
# John Roy Daradal 

from aoc import *

def data(full: bool) -> tuple[dict[int,str],dict[str,str]]:
    lines = readLines(18, 12, full)
    defaultDot = lambda: '.'
    start = splitStr(lines[0], ':')[1]
    pots: dict[int,str] = defaultdict(defaultDot)
    for i,b in enumerate(start): pots[i] = b 
    
    T: dict[str,str] = defaultdict(defaultDot)
    for line in lines[2:]:
        k, v = splitStr(line, '=>')
        T[k] = v 
    return pots, T

def solve():
    pots, T = data(full=True)
    done: dict[str,int] = defaultdict(int)
    done[stateKey(pots)] = 0
    for t in range(200):
        transform(pots, T)
        score = scoreOf(pots)
        if t == 19:
            print(score)
        state = stateKey(pots)
        if state in done:
            N = 50_000_000_000 
            left = N-t 
            prev = done[state]
            step = score - prev 
            total = prev + (left*step)
            print(total)
            break
        done[state] = score

def transform(pots: dict[int,str], T: dict[str,str]):
    # Pad left side 
    minIdx = min(pots)
    if pots[minIdx] == '#':
        pots[minIdx-1] = '.'
        pots[minIdx-2] = '.'
    elif pots[minIdx+1] == '#':
        pots[minIdx-1] = '.'
    # Pad right side 
    maxIdx = max(pots)
    if pots[maxIdx] == '#':
        pots[maxIdx+1] = '.'
        pots[maxIdx+2] = '.'
    elif pots[maxIdx-1] == '#':
        pots[maxIdx+1] = '.'

    pots2: dict[int,str] = {}
    for idx in sorted(pots.keys()):
        w = ''.join(pots[idx+d] for d in (-2,-1,0,1,2))
        pots2[idx] = T[w]
    pots.clear()
    pots.update(pots2)

def stateKey(pots: dict[int,str]) -> str: 
    neg: list[str] = []
    pos: list[str] = []
    for k, v in sorted(pots.items()):
        if k < 0:
            neg.append(v)
        else:
            pos.append(v)
    half1 = ''.join(neg)
    half2 = ''.join(pos)
    return (half1+half2).strip('.') # remove extra spaces

def scoreOf(pots: dict[int,str]) -> int:
    return sum(i for i,b in pots.items() if b == '#')

if __name__ == '__main__':
    do(solve)

'''
Solve:
- Use a defaultdict to store the pots data: easier to expand left and right
- The state of a pots list can be frozen by sorting the pots by their pot index:
    - Collect the negative numbers and positive numbers separately 
    - Join the negative and positive numbers and remove extra spaces at the front/back (.)
- Keep track of done pots list states, so we know when it loops back; remember the score for this state
- Try for 200 generations, usually the looped state can be found within this range 
- At each generation, transform the pots throught the translation rules:
    - Pad the left side and right side of the pots: ensure that there are 2 dots on either side
    - Go through the windows of -2,-1,0,1,2 and extract the pot sequence for each window 
    - Translate the pot result of the given window using the translation table
- The score of a pots list is the sum of pot indexes that contain a plant (#)
- For Part 1, output the score of pots after 20 generations
- For Part 2, output the score of pots after 50 billion generations
    - We only need to find the looped state and compute from there 
    - Once we find a state that was already visited, compute how many steps are left from current t to 50B 
    - The step score is the difference of the current score and the previous state visited's score 
    - Multiply the number of steps left by the step score
    - Add the score of the previous state that was visited (from t=0 up to this point)
'''