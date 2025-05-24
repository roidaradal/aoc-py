# Advent of Code 2020 Day 10
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    numbers = [int(x) for x in readLines(20, 10, full)]
    numbers.append(0)
    numbers.append(max(numbers) + 3)
    return numbers 

def part1():
    numbers = data(full=True)
    numbers.sort()
    diffs: dict[int,int] = defaultdict(int)
    for i in range(1, len(numbers)):
        d = numbers[i] - numbers[i-1]
        diffs[d] += 1
    print(diffs[1] * diffs[3])

def part2():
    numbers = data(full=True)
    numbers.sort()
    count =  {numbers[-1] : 1}
    i = len(numbers) - 2 
    while i >= 0:
        curr = numbers[i]
        valid = [x for x in numbers[i+1:i+4] if x-curr <= 3]
        count[curr] = sum(count[x] for x in valid)
        i -= 1
    print(count[numbers[0]])

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Sort the adapters
- Go through adjacent adapter pairs and tally the difference counts
- Output the product of the diff-1 and diff-3 counts

Part2:
- Sort the adapters
- For the built-in adapter, fixed to 1 arrangement = last position
- Starting from penultimate adapter going to first, get the number of different adapters that can connect to it
- Look at a 3-window size after current adapter and keep only those with a difference of <= 3
- Sum up the counts of the valid next adapters => this becomes the count for the current adapter
- They are guaranteed to have counts because we are going backwards (last to first)
- Finally, output the count of the first number: this is the number of valid arrangements for adapters
'''