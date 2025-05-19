# Advent of Code 2015 Day 07
# John Roy Daradal 

from aoc import *

LET, AND, OR, NOT, LSHIFT, RSHIFT = 'LET', 'AND', 'OR', 'NOT', 'LSHIFT', 'RSHIFT'

def data(full: bool) -> list[tuple]:
    def fn(line: str) -> tuple:
        expr, res = splitStr(line, '->')
        if AND in expr or OR in expr:
            cmd = AND if AND in expr else OR
            v1, v2 = [tryParseInt(x) for x in splitStr(expr, cmd)]
            return (res, cmd, v1, v2)
        elif LSHIFT in expr or RSHIFT in expr:
            cmd = LSHIFT if LSHIFT in expr else RSHIFT
            v1, v2 = [tryParseInt(x) for x in splitStr(expr, cmd)]
            return (res, cmd, v1, v2)
        elif NOT in expr:
            v = splitStr(expr, NOT)[-1]
            return (res, NOT, v)
        else:
            v = tryParseInt(expr)
            return (res, LET, v)
    return [fn(line) for line in readLines(15, 7, full)]

def solve():
    commands = data(full=True)
    a = solveA(commands) 
    print(a)
    
    override = {'b' : a}
    a = solveA(commands, override)
    print(a) 

def solveA(commands: list[tuple], override: dict[str,int]|None = None) -> int:
    value = {}
    defer = []
    for cmd in commands:
        rcv, op = cmd[0], cmd[1]
        if op == LET:
            v = cmd[2]
            if type(v) == int:
                value[rcv] = v
            else:
                defer.append(([v], rcv, op, None))
        elif op == AND or op == OR:
            vars, consts = getVars([cmd[2], cmd[3]])
            defer.append((vars, rcv, op, consts[0] if len(consts) > 0 else None))
        elif op == LSHIFT or op == RSHIFT:
            v, param = cmd[2], cmd[3]
            defer.append(([v], rcv, op, param))
        elif op == NOT:
            v = cmd[2]
            defer.append(([v], rcv, op, None))
    
    if override is not None:
        for k,v in override.items():
            value[k] = v

    while len(defer) > 0:
        defer2 = []
        for d in defer:
            x, rcv, op, param = d 
            if any(v not in value for v in x): 
                defer2.append(d)
                continue 
            if op == AND:
                value[rcv] = value[x[0]] & (value[x[1]] if param is None else param)
            elif op == OR:
                value[rcv] = value[x[0]] | (value[x[1]] if param is None else param)
            elif op == LSHIFT:
                value[rcv] = value[x[0]] << param
            elif op == RSHIFT:
                value[rcv] = value[x[0]] >> param
            elif op == NOT:
                value[rcv] = ~value[x[0]]
            elif op == LET:
                value[rcv] = value[x[0]]
            if value[rcv] < 0:
                value[rcv] += 65536
        defer = defer2 
        if 'a' in value: break 
    
    return value['a']
    
def getVars(items: list) -> tuple[list,list]: # vars, consts 
    vars =   [x for x in items if type(x) == str]
    consts = [x for x in items if type(x) == int]
    return vars, consts

if __name__ == '__main__':
    do(solve)

'''
Solve:
- For Part 1, solve for value of A
- For Part 2, take the value of A from Part 1 and make it override the value of B; solve for A again
- To solve for A, process only the commands where their variables already have assigned values
- Otherwise, defer the command; repeat until all commands are processed or until 'a' has a value
- Preprocess:
    - If LET command and the value is not a variable, assign to value lookup; otherwise defer 
    - If AND/OR command, figure out the vars and consts among the params 
    - If LSHIFT/RSHIFT command, the param is sure to be an explicit int
    - If NOT command, param is sure to be a variable
    - Defer the rest of the other command types (not LET)
- If any override given, add them to value lookup now
- In processing deferred commands, defer it back if any variable is not yet assigned
- Otherwise, process the commands accordingly
- For AND/OR, the second param depends on whether there is a value param, otherwise just use the 2nd variable param
- If result becomes negative, wrap-around by adding 65536
'''