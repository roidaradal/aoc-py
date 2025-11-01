# Advent of Code 2024 Day 22
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    return [int(line) for line in readLines(24, 22, full)]

def solve() -> Solution:
    secrets = data(full=True)

    allPrices: list[list[int]] = []
    allDiffs: list[list[int]] = []
    total = 0
    for x in secrets:
        prev = price(x)
        prices: list[int] = []
        diffs: list[int] = []
        for _ in range(2000):
            x = nextSecret(x)
            curr = price(x)
            diff = curr-prev 
            prices.append(curr)
            diffs.append(diff)
            prev = curr 
        allPrices.append(prices)
        allDiffs.append(diffs)
        # Part 1
        total += x

    # Part 2
    sequences: dict[int4, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for buyer, diffs in enumerate(allDiffs):
        for i in range(3, len(diffs)):
            seq: int4 = (diffs[i-3], diffs[i-2], diffs[i-1], diffs[i])
            if buyer not in sequences[seq]:
                sequences[seq][buyer] = allPrices[buyer][i]
    maxTotal = max(sum(prices.values()) for prices in sequences.values())

    return newSolution(total, maxTotal)

def nextSecret(x: int) -> int:
    x = pruneSecret((x * 64)   ^ x)
    x = pruneSecret((x // 32)  ^ x) 
    x = pruneSecret((x * 2048) ^ x)
    return x 

def pruneSecret(x: int) -> int:
    return x % 16777216

def price(x: int) -> int:
    return x % 10

if __name__ == '__main__':
    do(solve, 24, 22)

'''
Part1:
- To compute the next secret key from the current key: 
    - Mix(y)    => x = x ^ y 
    - Prune()   => x = x % 16777216
    - The next key is computed by doing 3 steps of mixing and pruning:
    prune(mix(x*64)), then prune(mix(x//32)), then prune(mix(x*2048))
- For each starting secret key from the buyers, compute the next 2000 secret keys
- Output the total of the buyers' last secret keys

Part2:
- The price is the ones digit of the secret key (x % 10)
- The price also indicates the number of bananas you get once you sell
- While we compute the next 2000 secret keys of each buyer in Part 1, we also monitor the 
  price differences of the current price and the previous price
- After generating all the buyers' secret keys, we will find the best 4-length price diff sequence
  that will maximize the total bananas we get after selling
- For each buyer, go through their price diff list and check 4-length sequences
- If it is the first time you see this 4-length sequence for this buyer, we take note of the price
  for selling at this point, which is also equivalent to the amount of bananas we get
- Finally, go through the sequences and sum up the total price for this sequence from the buyers that have it
- Output the maximum total price from the sequences
'''