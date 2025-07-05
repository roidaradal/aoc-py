# Advent of Code 2020 Day 16
# John Roy Daradal 

from aoc import *

Fields = dict[str, list[int2]]
Ticket = list[int]

def data(full: bool) -> tuple[Fields, Ticket, list[Ticket]]:
    fields: Fields = {}
    ticket: Ticket = []
    nearby: list[Ticket] = []
    part = 1
    for line in readLines(20, 16, full):
        if line == '':
            continue 
        elif line == 'your ticket:':
            part = 2
        elif line == 'nearby tickets:':
            part = 3
        elif part == 1:
            key, tail = splitStr(line, ':')
            ranges = splitStr(tail, 'or')
            fields[key] = [toInt2(r, '-') for r in ranges]
        elif part == 2:
            ticket = toIntList(line, ',')
        elif part == 3:
            nearby.append(toIntList(line, ','))
    return fields, ticket, nearby

def solve() -> Solution:
    fields, yourTicket, nearby = data(full=True)

    # Part 1
    total = 0
    valid: list[Ticket] = []
    for ticket in nearby:
        isValid = True
        for number in ticket:
            if not isValidNumber(number, fields):
                total += number 
                isValid = False 
        if isValid: valid.append(ticket)
    valid.append(yourTicket)

    # Part 2 
    T = findMapping(fields, valid)
    departure = 1
    for field, idx in T.items():
        if not field.startswith('departure'): continue
        departure *= yourTicket[idx]

    return newSolution(total, departure)

def isValidNumber(number: int, fields: Fields):
    for ranges in fields.values():
        if inRange(number, ranges): return True
    return False

def inRange(number: int, ranges: list[int2]) -> bool:
    for start,end in ranges:
        if start <= number <= end: return True 
    return False

def findMapping(fields: Fields, tickets: list[Ticket]) -> dict[str, int]:
    limit = len(fields)
    keys = list(fields.keys())
    domain: dict[int, list[str]] = {i: keys[:] for i in range(limit)}

    for ticket in tickets:
        for i, number in enumerate(ticket):
            valid: list[str] = []
            for key in domain[i]:
                if inRange(number, fields[key]):
                    valid.append(key)
            domain[i] = valid

    T: dict[str, int] = {}
    while len(T) != limit:
        idx = -1
        for idx, options in domain.items():
            if len(options) == 1:
                break
        key = domain[idx][0]
        T[key] = idx 
        del domain[idx]
        for idx in domain:
            domain[idx] = [k for k in domain[idx] if k != key]
    return T

if __name__ == '__main__':
    do(solve, 20, 16)

'''
Part1
- Go through each nearby ticket; for each ticket, check the numbers 
- If a number in the ticket cannot be a valid number, add it to the total 
- Output the total of invalid numbers from all nearby tickets
- To check if a ticket number is valid, go through all field ranges:
  if the number is in any of the field ranges, it is valid

Part2:
- While doing Part 1, collect the tickets where all numbers were valid
- Add your ticket to the list of valid tickets
- Find the mapping of field to ticket index 
- Start with the domain of each index initialized to all possible fields 
- For each ticket, go through the ticket numbers 
- Reduce the ticket indexes domains by filtering out invalid values by range checking
- Deduce the final mapping by repeatedly assigning indexes with only 1 key in the domain left 
- Remove that value from other indexes' domains, creating a domino effect of creating another index with 1 key left 
- Repeat until we get the full mapping of field => index
- After getting the mapping, get the product of all numbers in your ticket where its mapped 
  key starts with departure
'''