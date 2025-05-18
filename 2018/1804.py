# Advent of Code 2018 Day 04
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[strInt]:
    def fn(line: str) -> strInt:
        head, tail = line.split(']')
        minute = int(head.split(':')[1])
        if 'asleep' in tail:
            return ('on', minute)
        elif 'wakes' in tail:
            return ('off', minute)
        else:
            p = tail.split()
            return ('guard', int(p[1].strip('#')))
    return [fn(line) for line in sorted(readLines(18, 4, full))]

def part1():
    logs = data(full=True)
    sleep = process(logs)

    guard = max((sum(s.values()), guard) for guard,s in sleep.items())[1]
    minute = max((count,m) for m,count in sleep[guard].items())[1]
    print(guard * minute)

def part2():
    logs = data(full=True)
    sleep = process(logs)

    guards = []
    for guard, s in sleep.items():
        count, minute = max((v,k) for k,v in s.items())
        guards.append((count, minute, guard))

    _, minute, guard = max(guards)
    print(guard * minute) 

def process(logs: list[strInt]) -> dict[int,dict[int,int]]:
    limit = len(logs)
    i, guard = 0, 0 
    sleep: dict[int,dict[int,int]] = defaultdict(lambda: defaultdict(int))
    while i < limit:
        cmd, x = logs[i]
        if cmd == 'guard':
            guard = x 
            i += 1 
        elif cmd == 'on':
            _, end = logs[i+1]
            for m in range(x, end):
                sleep[guard][m] += 1
            i += 2 
    return sleep

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Get the guard with the max total sleep time 
- Get that guard's minute he spent the most time sleeping

Part2:
- For each guard get the minute and duration he spent the most time sleeping
- Get the max duration for all guards, and use that guard's longest minute

SleepCount:
- Go through log entries (cmd,x)
- 'guard' cmd updates the current guard 
- 'on' cmd starts the sleep of current guard 
- get the corresponding 'off' limit (wake up) in the next entry 
- increment minute sleep count of current guard from start to end
'''