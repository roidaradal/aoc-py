# Advent of Code 2019 Day 16
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[int]:
    line = readFirstLine(19, 16, full)
    return toIntLine(line)

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> str:
    signal = data(full=True)
    limit = len(signal)
    mask: dict[int,list[int]] = {}
    for idx in range(limit):
        mask[idx] = createMask(idx, limit)

    for _ in range(100):
        signal = [fft(signal, mask[idx]) for idx in range(len(signal))]
    return ''.join(str(x) for x in signal[:8])

def part2() -> str:
    signal = data(full=True)
    skip = int(''.join(str(x) for x in signal[:7]), 10)
    signal = (signal * 10000)[skip:]
    limit = len(signal)
    for _ in range(100):
        total = 0
        for i in range(limit-1, -1, -1):
            total += signal[i]
            signal[i] = total % 10
    return ''.join(str(x) for x in signal[:8])

def createMask(idx: int, limit: int) -> list[int]:
    base = [0, 1, 0, -1]
    mask: list[int] = []
    repeat = idx + 1
    for b in base:
        mask += [b] * repeat
    size = len(mask)
    if size <= limit:
        copies = limit // size
        mask = mask * (copies+1) 
    mask = mask[1:] # exclude first 
    return mask[:limit]

def fft(signal: list[int],  mask: list[int]) -> int:
    return abs(sum(a * b for a,b in zip(signal,mask))) % 10

if __name__ == '__main__':
    do(solve, 19, 16)

'''
Part1:
- Create the mask for idx 0 to N-1; better to compute once since we'll use these 100x 
    - To create the mask, repeat (idx+1) each base number (0, 1, 0, -1) according to the index;
    - The full mask is repeated until it can cover the whole size of the signal 
    - Exclude the first mask bit, and slice the front part that will align with the signal size
- Transform the signal using FFT transform 100 times:
    - FFT of signal list and mask list = sum(a*b), then get the last digit of the result
    - Abs(x) % 10 gets ones digit of result; make sure to abs since -x % 10 does not yield x
    - Transform full signal: apply FFT on the list using the index mask -> this becomes the new value for that index
- Output the first 8 digits of the resulting signal 

Part2:
- First 7 digits of the input tells you the offset of where to read the output later; 
  we will skip this amount of digits and start reading the 8-digit output 
- Fully expand the signal by repeating it 10,000 times
- Because of how the mask is constructed, we can discard the front part of the signal before the skip:
    - At idx=0, repeat 1x: 0,1,0,-1, remove first => 0 zeros in the prefix 
    - At idx=1, repeat 2x: 0,0,1,1,0,0,-1, remove first => 1 zero in the prefix
    - At idx=Middle, repeat (M+1)x,  (M+1)0s, (M+1)1s, remove first => M 0s in the prefix, M 1s at back
    - If skip is somewhere after the middle, at idx S, the mask is S 0s followed by N-S 1s, provided S > middle
- From skip up to last digit, the pattern of the mask looks like this:
    Example: Skip starts at 4
    Idx = 4  1 1 1 1    (4 leading zeros) 
    Idx = 5  0 1 1 1    (5 leading zeros)
    Idx = 6  0 0 1 1    (6 leading zeros)
    Idx = 7  0 0 0 1    (7 leading zeros)
- Since the masks are 1, we just need to sum the values from Idx to end; that is, the digit at idx X only relies on digits from X to end
    Idx 4 = Sum(signal[4:N])
    Idx 5 = Sum(signal[5:N])
    Idx 6 = Sum(signal[6:N])
- But instead of repeatedly doing the sums, we can accumulate the sum starting from the end 
  and have its last digit be the digit for the next signal at that index
    - Example: Signal is [5, 6, 7, 8]
    - Start at Idx 3: Total = 0 + 8,        Next Idx 3 = 8 
    - At Idx 2      : Total = 8 + 7 = 15    Next Idx 2 = 5 
    - At Idx 1      : Total = 15 + 6 = 21   Next Idx 1 = 1 
    - At Idx 0      : Total = 21 + 5 = 26   Next Idx 0 = 6
''' 