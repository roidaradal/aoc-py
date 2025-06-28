# Advent of Code 2017 Day 18
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str3]:
    def fn(line: str) -> str3:
        p = splitStr(line, None)
        cmd, p1 = p[0], p[1]
        p2 = '' if len(p) == 2 else p[2]
        return (cmd, p1, p2)
    return [fn(line) for line in readLines(17, 18, full)]

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    commands = data(full=True)
    limit = len(commands)
    reg: dict[str,int] = defaultdict(int)
    lastFreq: int = 0
    idx = 0
    while True:
        cmd, p1, p2 = commands[idx]
        step = 1
        match cmd:
            case 'snd':
                lastFreq = valueOf(p1, reg)
            case 'set':
                reg[p1] = valueOf(p2, reg)
            case 'add':
                reg[p1] += valueOf(p2, reg)
            case 'mul':
                reg[p1] *= valueOf(p2, reg)
            case 'mod':
                reg[p1] %= valueOf(p2, reg)
            case 'jgz':
                if valueOf(p1, reg) > 0:
                    step = valueOf(p2, reg)
            case 'rcv':
                if valueOf(p1, reg) != 0:
                    return lastFreq
        idx += step 
        if idx < 0 or idx >= limit: break        
    return 0

def part2() -> int:
    commands = data(full=True)
    p0 = Program(0, commands)
    p1 = Program(1, commands)
    turn = 0 
    while True:
        program = p0 if turn == 0 else p1
        other   = p1 if turn == 0 else p0
        value = program.next()
        turn = (turn+1) % 2 
        if value != None:
            other.queue.append(value)

        if p0.isDone and p1.isDone:
            break 
        elif p0.isDone and p1.hopelessWaiting:
            break 
        elif p1.isDone and p0.hopelessWaiting:
            break 
        elif p0.hopelessWaiting and p1.hopelessWaiting:
            break

    return p1.sendCount

def valueOf(x: str, reg: dict[str,int]) -> int:
    v = tryParseInt(x)
    return v if type(v) == int else reg[x]

class Program:
    def __init__(self, pid: int, commands: list[str3]):
        self.commands = commands 
        self.idx = 0
        self.limit = len(commands)
        self.reg: dict[str,int] = defaultdict(int)
        self.reg['p'] = pid
        self.queue: list[int] = []
        self.sendCount: int = 0
        self.isWaiting: bool = False 
        self.isDone: bool = False

    @property
    def hopelessWaiting(self) -> bool:
        return self.isWaiting and len(self.queue) == 0

    def next(self) -> int|None:
        if self.isDone: return None

        cmd, p1, p2 = self.commands[self.idx]
        step = 1
        out: int|None = None
        match cmd:
            case 'snd':
                self.sendCount += 1
                out = valueOf(p1, self.reg)
            case 'rcv':
                if len(self.queue) == 0:
                    self.isWaiting = True 
                    return None 
                else:
                    self.reg[p1] = self.queue.pop(0)
            case 'set':
                self.reg[p1] = valueOf(p2, self.reg)
            case 'add':
                self.reg[p1] += valueOf(p2, self.reg)
            case 'mul':
                self.reg[p1] *= valueOf(p2, self.reg)
            case 'mod':
                self.reg[p1] %= valueOf(p2, self.reg)
            case 'jgz':
                if valueOf(p1, self.reg) > 0:
                    step = valueOf(p2, self.reg)

        self.idx += step 
        if self.idx < 0 or self.idx >= self.limit: 
            self.isDone = True

        return out

if __name__ == '__main__':
    do(solve, 17, 18)

'''
Part1:
- Start with command index at 0, registers using defaultdict (default 0)
- Process the current command:
    - snd: update last frequency to valueOf(p1)
    - set: set reg[p1] = valueOf(p2)
    - add: set reg[p1] = reg[p1] + valueOf(p2)
    - mul: set reg[p1] = reg[p1] * valueOf(p2)
    - mod: set reg[p1] = reg[p1] % valueOf(p2)
    - jgz: if valueOf(p1) > 0, command index step = valueOf(p2)
    - rcv: if valueOf(p1) != 0, return last frequency
- Unless step was modified by jgz, increment the command index by 1
- Check if index is out of bounds (left/right): stop

Part2:
- This problem models two programs running concurrently, with message passing 
- Create 2 programs P0 and P1 with their own state, commands, registers, and queues
    - Both programs start at command index = 0 
    - Both programs initialize reg['p'] = 0 or 1 (their program id)
- Start with P0, they take turns to run to model concurrency
- At a program's turn, we execute it similar to command processing in Part 1:
    - If program.isDone: do nothing and return
    - Process the command at the current index, similar to Part 1, except snd and rcv
    - snd: increment the program's sendCount and return the valueOf(p1)
    - rcv: if queue, the program will wait and do nothing; otherwise, it takes the first item 
      in the queue and set reg[p1] to that value
    - The program's own index is incremented by the step (1, if not modified by jgz), 
      except for when rcv command made it wait and terminated early
    - If program's index goes out of bounds, we mark it as done
- If a program returns a value, we send it to the other program's queue
- Check for loop termination conditions:
    - Both programs are done 
    - One program is done, while the other is waiting and has an empty queue
    - Both programs are waiting and have empty queues (deadlock)
- Output p1's sendCount
'''