# Advent of Code 2019 Day 25
# John Roy Daradal 

import itertools
from aoc import *
from intcode import *

RoomInfo = tuple[str, list[str], str] # name, doors, item

doorOptions = ['north', 'south', 'east', 'west']
badItems = ['giant electromagnet', 'photons', 'molten lava', 'escape pod', 'infinite loop']
UNKNOWN, NONE = '?', ''
OPP: dict[str,str] = {
    'north' : 'south',
    'south' : 'north',
    'east'  : 'west',
    'west'  : 'east',
}

class Explorer:
    def __init__(self):
        self.prevRoom: str = NONE
        self.roomDoors: dict[str, dict[str, str]] = {}
        self.invItems: list[str] = []
        self.goalItems = 8
        self.startRoom = 'Hull Breach'
        self.checkRoom = 'Security Checkpoint'
        self.roomPath: list[str] = []
        self.checkRoomPath: list[str] = []
        self.triggerDoor: str = ''
        self.comboMode = False
        self.comboCommands: list[list[int]] = []
    
    def explore(self, output: str) -> list[int]:
        commands: list[str] = []
        room, doors, item = parseRoom(output)

        # Add to roomDoors if new room 
        if room not in self.roomDoors:
            self.roomDoors[room] = {door : NONE for door in doorOptions}
            for door in doors:
                self.roomDoors[room][door] = UNKNOWN 

        # Update step to previous and current room 
        if self.prevRoom != NONE and len(self.roomPath) > 0:
            door = self.roomPath[-1] # last step 
            # Prev room's step led to current room 
            self.roomDoors[self.prevRoom][door] = room 
            # Current room's ooposite step leads back to previous room 
            self.roomDoors[room][OPP[door]] = self.prevRoom
        
        # If room has item which is not bad, take it 
        if item != NONE and item not in badItems:
            commands.append('take %s' % item)
            self.invItems.append(item)

        # Check if already in check room 
        if room == self.checkRoom: 
            if len(self.invItems) == self.goalItems: # all items collected
                # Find trigger door to Pressure-Sensitive Floor
                for door in self.roomDoors[room]:
                    if self.roomDoors[room][door] == UNKNOWN:
                        self.triggerDoor = door 
                        break 
                self.comboMode = True
                self.createCombos()
                return self.tryCombo()
            else: # not all items collected yet
                # Set path to checkRoom 
                self.checkRoomPath = self.roomPath[:]
                # undo last step
                door = self.roomPath.pop()
                commands.append(OPP[door])
                self.prevRoom = NONE
        else:
            self.prevRoom = room 
            # Find first unexplored door 
            for door in doors:
                if self.roomDoors[room][door] == UNKNOWN:
                    commands.append(door)
                    self.roomPath = updateRoomPath(self.roomPath, door)
                    break 
            else: # no unknown door found
                if len(self.roomPath) == 0:
                    # currently at startRoom + no unexplored = go to checkRoom
                    # must have completed items now
                    for door in self.checkRoomPath:
                        commands.append(door)
                    self.prevRoom = NONE
                else:
                    # no unknown door at current room = deadend = undo last step 
                    door = self.roomPath.pop()
                    commands.append(OPP[door])

        return createInputs(commands)

    def tryCombo(self) -> list[int]:
        return self.comboCommands.pop(0)
    
    def createCombos(self):
        remove: list[list[str]] = []
        for i in range(8):
            take = i+1 
            for combo in itertools.combinations(self.invItems, take):
                remove.append(list(combo))
        
        for i, combo in enumerate(remove):
            commands: list[str] = []
            if i > 0:
                # Pick up previous dropped items
                for dropped in remove[i-1]:
                    commands.append('take %s' % dropped)
            # Drop current combo items
            for drop in combo:
                commands.append('drop %s' % drop)
            # Go to PSF by going through trigger door
            commands.append(self.triggerDoor)

            cmd = createInputs(commands)
            self.comboCommands.append(cmd)
                
def data(full: bool) -> dict[int,int]:
    line = readFirstLine(19, 25, full)
    numbers = toIntList(line, ',')
    memory = defaultdict(int)
    for i,x in enumerate(numbers):
        memory[i] = x 
    return memory

def solve() -> Solution:
    numbers = data(full=True)
    password = runProgram(numbers)
    return newSolution(password, "")

def runProgram(numbers: dict[int, int]) -> str:
    i, rbase = 0, 0 
    outputs: list[str] = []
    inputs: list[int] = []
    bot = Explorer()
    while True:
        word = str(numbers[i])
        head, tail = word[:-2], word[-2:]
        cmd = int(tail)
        if cmd == 99: break 

        if cmd in (1,2,7,8): # Add, Multiply, LessThan, Equals
            in1, in2, out = numbers[i+1], numbers[i+2], numbers[i+3]
            m1, m2, m3 = modes(head, 3)
            a = param2(in1, m1, rbase, numbers)
            b = param2(in2, m2, rbase, numbers)
            c = index(out, m3, rbase)
            if cmd == 1:
                numbers[c] = a + b
            elif cmd == 2:
                numbers[c] = a * b
            elif cmd == 7: 
                numbers[c] = 1 if a < b else 0
            elif cmd == 8:
                numbers[c] = 1 if a == b else 0
            i += 4
        elif cmd == 3: # Input
            m = modes(head, 1)[0]
            idx = index(numbers[i+1], m, rbase)
            if len(inputs) == 0:
                # Parse the room output and decide where to go
                output = ''.join(outputs)
                outputs = []

                if bot.comboMode:
                    inputs = bot.tryCombo()
                else:
                    inputs = bot.explore(output)

            numbers[idx] = inputs.pop(0)
            i += 2
        elif cmd == 4: # Output
            m = modes(head, 1)[0]
            output = param2(numbers[i+1], m, rbase, numbers)
            outputs.append(chr(output))
            i += 2 
        elif cmd == 9: # relative base 
            m = modes(head, 1)[0]
            jmp = param2(numbers[i+1], m, rbase, numbers)
            rbase += jmp 
            i += 2
        elif cmd == 5 or cmd == 6: #Jump-if-True/False
            p1, p2 = numbers[i+1], numbers[i+2]
            m1, m2 = modes(head, 2)
            isZero = param2(p1, m1, rbase, numbers) == 0
            doJump = isZero if cmd == 6 else (not isZero)
            if doJump:
                i = param2(p2, m2, rbase, numbers)
            else:
                i += 3
    
    output = ''.join(outputs)
    return getPassword(output)

def parseRoom(output: str) -> RoomInfo:
    room, item = NONE, NONE
    doors: list[str] = []
    listMode = NONE
    for line in splitStr(output, '\n'):
        line = line.strip()
        if line.startswith('=='):
            room = line.strip('=').strip()
        elif line == '':
            listMode = NONE
        elif line == 'Doors here lead:':
            listMode = 'doors'
        elif line == 'Items here:':
            listMode = 'item'
        elif listMode == 'doors' and line.startswith('-'):
            door = line.strip('-').strip()
            doors.append(door)
        elif listMode == 'item' and line.startswith('-'):
            item = line.strip('-').strip()
    return (room, doors, item)

def updateRoomPath(roomPath: list[str], door: str) -> list[str]:
    if len(roomPath) > 0 and roomPath[-1] == OPP[door]:
        # last step is the opposite of current step
        roomPath.pop() # cancel out the last step
    else:
        roomPath.append(door)
    return roomPath

def getPassword(output: str) -> str:
    words = splitStr(output, None)
    if 'typing' in words:
        idx = words.index('typing')
        return words[idx+1]
    else:
        return ''

def createInputs(commands: list[str]) -> list[int]:
    cmd = '\n'.join(commands) + '\n'
    return [ord(x) for x in cmd]

if __name__ == '__main__':
    do(solve, 19, 25)

'''
Solve:
- Similar to 1917 (ASCII Intcode), except for input and output:
    - For input, get the input digits from the explorer; also, consume the outputs stored so far and reset
    - For output, collect the ASCII outputs into a list for parsing by the explorer later
- Explorer starts in explore mode:
    - Our goal in this mode is to explore all rooms, get the 8 safe items, and find the path to the check room
    - Upon entering the room, we parse the room info from the output stored so far
    - Get the room name, doors, and item in the room (if any)
    - If it's a new room, initialize its doors to UNKNOWN (unexplored), while those without doors are set to NONE
    - If we came from a previous room, we update the dual direction of doors:
        - The door we took is the last step of the path 
        - Set previous room's door to this room 
        - Set this room's opposite door to the previous room
        - Example: Prev=Room A, going east => Room B 
        - Room[A][east] = B, Room[B][west] = A
    - If the room has an item which is not in the list of bad items, take it 
    - List of bad items were known from previous manual exploration of the grid
    - Add command: take <item>, and add the item to your inventory
    - If we have reached the check room (Security Checkpoint), but we don't have all 8 items yet, 
      we remember the current path as the path to the check room, then we backtrack, so we can explore other rooms
    - If not yet in the check room, find the first unexplored door in the current room and go to that room 
    - If there are no more unknown doors at this room, we are at a deadend, so we undo the previous step
    - If there are no unknown doors and we are at the start room (Hull Breach), we go to the check room as we have all 8 items now
    - In updating the room path, if the last step is the opposite of the new step, 
      we just cancel them out; otherwise, we add the new step to the end of the path
- After getting all 8 items, we go to the checkRoom and switch to combo mode:
    - Find the trigger door: the room that leads to the Pressure-Sensitive Floor; this would be the only UNKNOWN door in the check room
    - In combo mode, the explorer will try out all combinations of items that will stop the program
    - We first create all item combinations: remove 1, remove 2, ..., remove 8
    - Then, we create the command list for testing these combinations:
    - If it is not the first combo, we add 'take <item>' commands for the dropped items in the previous combo
    - Then we add 'drop <item>' commands for the items to be dropped for this combo
    - Finally we add the trigger door command (NEWS) to test the combination
- The password is found when the right combination of items are held at the Pressure-Sensitive Floor:
    - This will allow the program to exit; we parse the last output of the program
    - Find the word 'typing' in the output as the password will be right next to it
- No problem for Part 2
'''
