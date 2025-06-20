# Advent of Code 2020 Day 04
# John Roy Daradal 

import re
from aoc import *

Passport = dict[str,str]

def data(full: bool) -> list[Passport]:
    passports = []
    p = {}
    for line in readLines(20, 4, full):
        if line == '':
            passports.append(p)
            p = {}
        else:
            for k,v in [pair.split(':') for pair in line.split()]:
                p[k] = v
    passports.append(p)
    return passports

def solve() -> Solution:
    passports = data(full=True)

    # Part 1
    count1 = countValid(passports, hasAllKeys)

    # Part 2 
    count2 = countValid(passports, isValid)

    return newSolution(count1, count2)

required = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
def hasAllKeys(p: Passport) -> bool:
    return all(k in p for k in required)

hclPattern = r'^#[0-9a-f]{6}$'
pidPattern = r'^[0-9]{9}$'
eclOptions = ('amb','blu','brn','gry','grn','hzl','oth') 
def isValid(p: Passport) -> bool:
    ok = 0 
    for k,v in p.items():
        if k == 'byr':
            if 1920 <= int(v) <= 2002: ok += 1
        elif k == 'iyr':
            if 2010 <= int(v) <= 2020: ok += 1
        elif k == 'eyr':
            if 2020 <= int(v) <= 2030: ok += 1 
        elif k == 'hgt' and (v.endswith('cm') or v.endswith('in')):
            x, unit = int(v[:-2]), v[-2:]
            if unit == 'cm' and 150 <= x <= 193: ok += 1
            elif unit == 'in' and 59 <= x <= 76: ok += 1
        elif k == 'hcl':
            if re.match(hclPattern, v) != None: ok += 1
        elif k == 'ecl':
            if v in eclOptions: ok += 1 
        elif k == 'pid':
            if re.match(pidPattern, v) != None: ok += 1
    return ok == len(required)

if __name__ == '__main__':
    do(solve, 20, 4)

'''
Part1:
- Count number of valid passports 
- Valid if has all required keys 

Part2:
- byr: 1920 <= x <= 2002
- iyr: 2010 <= x <= 2020 
- eyr: 2020 <= x <= 2030
- hgt: if cm, 150 <= x <= 193
- hgt: if in, 59 <= x <= 76
- hcl: v matches pattern #[0-9a-f]{6} exactly
- ecl: v in valid options
- pid: v matches pattern [0-9]{9} exactly
- Valid if count ok == count required keys
'''