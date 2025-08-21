# Advent of Code 2022 Day 25
# John Roy Daradal 

from aoc import *

T: dict[str, int] = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
snafuDigits: list[int] = [-2, -1, 0, 1, 2]
snafuChars: str = '=-012'

def data(full: bool) -> list[str]:
    return readLines(22, 25, full)

def solve() -> Solution:
    fuels = data(full=True)
    total = sum(snafuToDecimal(fuel) for fuel in fuels)

    maxVal: dict[int, int] = {}
    maxVal[-1] = 0
    idx = 0
    while True:
        limit =  (2*(5**idx)) + maxVal[idx-1]
        maxVal[idx] = limit
        if total <= limit: break 
        idx += 1

    code: list[str] = []
    current = total
    while idx >= 0:
        for i, digit in enumerate(snafuDigits):
            value = digit * (5**idx)
            limit = value + maxVal[idx-1]
            if current <= limit:
                code.append(snafuChars[i])
                current -= value
                break        
        idx -= 1
    snafu = ''.join(code)

    return newSolution(snafu, '')

def snafuToDecimal(code: str) -> int:
    maxPower = len(code)-1
    total = 0
    for i,x in enumerate(code):
        p = maxPower-i 
        total += T[x] * (5 ** p)
    return total

if __name__ == '__main__':
    do(solve, 22, 25)

'''
Solve:
- Snafu digits consist of 0, 1, 2, - (-1) and = (-2)
- Convert the snafu digits to decimal:
    - If snafu digit is ABCD, the decimal value is:
      D*1 + (C*5^1) + (B*5^2) + (A*5^3)
    - SNAFU is a number system with base 5
    - From left to right, convert the snafu digit to its equivalent number 
      and multiply by 5 ** (maxPower-idx), where maxPower = len(code)-1
- Get the total fuel needed, by getting the sum of decimal values above
- Convert the total fuel to snafu digits
- First while-loop is trying to find the number of digits needed:
    - Start with idx=0 (length 1), increment until we find a valid limit
    - Maximum value at this idx is 2 * (5^idx) + maxVal[idx-1]
    - 2 is the max snafu digit, and we multiply the values with 5^idx at that position
    - We also add the maximum value of the previous position, to complete the rest of the digits
    - We stop if the total fuel <= limit
- Second while-loop is computing the snafu digit at each index
    - Start with the leftmost index (the index we stopped at in the first loop)
    - Check the snafu digits from -2 to 2, compute the value if we used this digit at this index
    - Then compute the maximum value we can obtain if we use this digit: value + maxValue[idx-1]
    - If the current value (starts at the total fuel) <= limit, we use this digit
    - Add the corresponding snafu code to the list, and subtract the value from the current value
- Output the snafu digits computed above
- No problem for Part 2
'''