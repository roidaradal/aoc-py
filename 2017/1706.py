# Advent of Code 2017 Day 06
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    line = readFirstLine(17, 6, full)
    return toIntList(line, None)

def solve() -> Solution:
    banks = data(full=True)
    numBanks = len(banks)
    done, count = {}, 0
    state = tuple(banks)
    done[state] = count
    while True:
        # Redistribute banks
        index = argmax(banks)
        take = banks[index]
        banks[index] = 0 
        for i in range(take):
            idx = (index + i + 1) % numBanks
            banks[idx] += 1 
        
        count += 1
        state = tuple(banks)
        if state in done:
            # Part 1 and 2
            return newSolution(count, count-done[state])
        done[state] = count 
    
if __name__ == '__main__':
    do(solve, 17, 6)

'''
Solve:
- To create a snapshot of the banks' state, turn it into a tuple
- Add the initial banks' state to done with count 0
- Repeat until we find a state that has already been seen previously
- Choose the index of the bank with max value (lower index tie-breaker)
- Empty that bank (set to 0)
- Starting with next bank, distribute the value one by one (wrap-around)
- If state is already seen before, display the number of steps to get there (for Part 1)
- Since we have been keeping track of which step we found that state, we can get the difference
  between the current step count and when we found it first to get the loop length (for Part 2)
'''