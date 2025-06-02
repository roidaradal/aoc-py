# Advent of Code 2015 Day 11
# John Roy Daradal 

from aoc import *

def data(full: bool) -> str:
    return readLines(15, 11, full)[0]

def solve():
    password = data(full=True)
    
    # Part 1 
    password = nextValidPassword(password)
    print(password)

    # Part 2 
    password = nextValidPassword(password)
    print(password)

def nextValidPassword(password: str) -> str:
    while True:
        password = nextPassword(password)
        if isValidPassword(password):
            return password

limit = ord('z')
invalid = ('i', 'o', 'l')

def nextPassword(password: str) -> str:
    idx = len(password)-1 
    chars: list[str] = []
    while True:
        n = ord(password[idx]) + 1 
        if n > limit:
            chars.append('a')
            idx -= 1
        else:
            if chr(n) in invalid:
                n += 1
            chars.append(chr(n))
            return password[:idx] + ''.join(reversed(chars))

def isValidPassword(password: str) -> bool:
    if any(x in password for x in invalid):
        return False 
    
    # Check for increasing straight substrings 
    prev = ord(password[0])
    size, sizes = 1, []
    for char in password[1:]:
        curr = ord(char)
        if curr - prev == 1:
            size += 1
        else:
            sizes.append(size)
            size = 1
        prev = curr 
    sizes.append(size)
    if not any(x >= 3 for x in sizes):
        return False 
    
    # Check pairs that have same letter
    pairs = []
    for i in range(len(password)-1):
        a, b = password[i], password[i+1]
        if a == b:
            pairs.append(i)
    
    if len(pairs) < 2:
        return False 
    elif len(pairs) == 2 and abs(pairs[0]-pairs[1]) == 1:
        return False 
    
    return True

if __name__ == '__main__':
    do(solve)

'''
Solve:
- For Part 1, print the next valid password of the input 
- For Part 2, print the next valid password of the answer in Part 1
- To generate the next valid password, compute the next password and check if valid

NextPassword:
- Start with the last index
- Increase the current index's character
- If already past z, wrap-around to a and move to the previous index 
- Otherwise, check if part of invalid charaters (iol); if it is, add 1 more 
- Copy the prefix up to the current index, and add the reversed collected characters

IsValidPassword:
- Check if any of the invalid characters are in the password 
- Check for increasing straight substrings (e.g. abc, def); check that any of the lengths is at least 3
- Check pairs that contain the same letters; must contain at least 2 and non-overlapping
'''