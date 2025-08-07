# Advent of Code 2019 Day 23
# John Roy Daradal 

from aoc import *
from intcode import *

def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 23, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    computers: dict[int, Computer] = {}
    limit = 50
    for address in range(limit):
        computers[address] = Computer(address)

    y1 = 0
    xnat, ynat = 0, 0 
    history: list[int] = []
    i = 0 
    while True:
        computer = computers[i]
        if computer.status != STOPPED:
            output = computer.nextStep()
            if len(output) == 3:
                recipient, x, y = output 
                if recipient == 255:
                    if y1 == 0:
                        y1 = y # Part 1: first Y value sent to NAT 
                    xnat, ynat = x, y
                elif recipient in computers:
                    computers[recipient].queue.append(x)
                    computers[recipient].queue.append(y)
        i = (i + 1) % limit 
        if all(computer.status == STOPPED for computer in computers.values()):
            # Detect all computers stopped => exit loop
            break
        if xnat != 0 and ynat != 0 and all(computer.isIdle for computer in computers.values()):
            # Detect all computers idle => feed NAT packet to computer 0 
            # Check if this yNAT value has already been sent before
            if ynat in history:
                history.append(ynat)
                break
            history.append(ynat)
            computers[0].queue.append(xnat)
            computers[0].queue.append(ynat)

    # Part 2
    y2 = history[-1] # last yNAT value in history is the one that repeated

    return newSolution(y1, y2)

ASLEEP, ACTIVE, STOPPED = 0, 1, 2 

class Computer:
    def __init__(self, address: int):
        self.address = address
        self.memory = data(full=True)
        self.status = ASLEEP 
        self.idx = 0
        self.rbase = 0
        self.queue: list[int] = [] 
        self.output: list[int] = []
        self.lastStep: str = ''
    
    @property 
    def isIdle(self) -> bool:
        return len(self.queue) == 0 and self.lastStep == 'wait'

    def nextStep(self) -> list[int]:
        while True:
            word = str(self.memory[self.idx])
            head, tail = word[:-2], word[-2:]
            cmd = int(tail)
            if cmd == 99:
                self.status = STOPPED
                self.lastStep = 'stop'
                return []
            
            if cmd in (1,2,7,8): # Add, Multiply, LessThan, Equals 
                in1, in2, out = self.memory[self.idx+1], self.memory[self.idx+2], self.memory[self.idx+3]
                m1, m2, m3 = modes(head, 3)
                a = param2(in1, m1, self.rbase, self.memory)
                b = param2(in2, m2, self.rbase, self.memory)
                c = index(out, m3, self.rbase)
                if cmd == 1:
                    self.memory[c] = a + b 
                elif cmd == 2:
                    self.memory[c] = a * b 
                elif cmd == 7:
                    self.memory[c] = 1 if a < b else 0 
                elif cmd == 8:
                    self.memory[c] = 1 if a == b else 0
                self.idx += 4
            elif cmd == 3: # input 
                m = modes(head, 1)[0]
                idx = index(self.memory[self.idx+1], m, self.rbase)
                if self.status == ASLEEP:
                    self.memory[idx] = self.address
                    self.status = ACTIVE
                elif self.status == ACTIVE:
                    if len(self.queue) == 0:
                        self.memory[idx] = -1 
                        self.lastStep = 'wait'
                    else:
                        self.memory[idx] = self.queue.pop(0)
                        self.lastStep = 'input'
                self.idx += 2
                return []
            elif cmd == 4: # output
                m = modes(head, 1)[0]
                out = param2(self.memory[self.idx+1], m, self.rbase, self.memory)
                self.output.append(out)
                self.idx += 2 
                if len(self.output) == 3:
                    output = self.output[:]
                    self.output = []
                    self.lastStep = 'output'
                    return output
            elif cmd == 9: # relative base
                m = modes(head, 1)[0]
                jmp = param2(self.memory[self.idx+1], m, self.rbase, self.memory)
                self.rbase += jmp 
                self.idx += 2
            elif cmd == 5 or cmd == 6: # jump-if-true/false 
                p1, p2 = self.memory[self.idx+1], self.memory[self.idx+2]
                m1, m2 = modes(head, 2)
                isZero = param2(p1, m1, self.rbase, self.memory) == 0 
                doJump = isZero if cmd == 6 else (not isZero)
                if doJump:
                    self.idx = param2(p2, m2, self.rbase, self.memory)
                else:
                    self.idx += 3

if __name__ == '__main__':
    do(solve, 19, 23)

'''
Solve:
- Intcode program is similar to 1909, except for the input and output commands
    - For input command, if computer is still ASLEEP, input is the computer's address and set status to ACTIVE
    - If computer is already active, check the message queue:
        - If queue is empty, input is -1, and the computer is waiting for packets in the queue
        - If not empty, input is the the front of the queue (this is dequeued)
    - For output command, store in a list of outputs, return the output list if it has 3 items already
      and reset the output list to empty
- Create the 50 computers each running their own Intcode programs, and has unique addresses (0-49)
    - Initialize computer's status to ASLEEP (not yet active)
    - Computer also keeps an internal message queue for packets received
    - The computer output is also kept as groups of 3
    - Computer is considered idle if no items in the queue, and the last step was waiting (input=-1)
    - Reaching the command=99, we set the computer to STOPPED status
- We simulate concurrency by going through the computers one-by-one, running them until an input/output command,
  and moving to the next one, wrap-around to first computer if necessary:
    - Skip computers that are already STOPPED 
    - Run the next step of a computer, which runs until an input / output command is encountered
    - If the output returned is a group of 3, we send the (x,y) value to the recipient computer
        - If the recipient address is 255, we will send it to the NAT; update the X,Y values of the NAT
        - Take note of the first Y value sent to the NAT, as this is the output for Part 1
        - If the recipient is a computer, we send the X and Y values to the recipient's queue
    - If all computers are stopped, we exit the loop
    - If all computers are detected as idle, and we have X,Y values for NAT, we send the X,Y values
      to computer 0's queue to resume the network activity
    - We keep track of the Y values being sent to computer 0 to resume the activity
    - If we see a Y value already sent before, we exit the loop, and output this value for Part 2
'''