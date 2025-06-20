# Advent of Code 2016 Day 05
# John Roy Daradal 

from aoc import * 

def data(full: bool) -> str:
    return readFirstLine(16, 5, full)

def solve() -> Solution:
    return newSolution(part1(), part2())

pwdLength = 8 

def part1() -> str:
    door = data(full=True)
    hashGen = md5HashGenerator(door, '00000', 0)
    pwd = ['.'] * pwdLength
    for i in range(pwdLength):
        _, hash = next(hashGen)
        pwd[i] = hash[5]
        print(''.join(pwd))
    return ''.join(pwd)

def part2():
    door = data(full=True)
    hashGen = md5HashGenerator(door, '00000', 0)
    indexes = [str(x) for x in range(pwdLength)]
    pwd = ['.'] * pwdLength 
    while any(p == '.' for p in pwd): 
        _, hash = next(hashGen)
        if hash[5] not in indexes: continue
        idx = int(hash[5])
        if pwd[idx] == '.':
            pwd[idx] = hash[6]
            print(''.join(pwd))
    return ''.join(pwd)

if __name__ == '__main__':
    do(solve, 16, 5)

'''
Part1:
- Increment i until you find an md5Hash of (doorI) that starts with 00000
- Each time you find a valid hash, add the 6th character to the password string
- Continue with the next i after finding a password character
- Repeat 8 times to complete the password 

Part2:
- Initialize password to all '.' 
- Similar processing as in Part 1 
- If hash is valid (starts with 00000), check if 6th character is a valid password index 
- If password index is still '.', replace with the 7th hash character
- Repeat until password has no more '.'
'''