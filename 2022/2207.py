# Advent of Code 2022 Day 07
# John Roy Daradal 

import sys
from aoc import *

class Item:
    def __init__(self, name: str, path: str, size: int):
        self.name = name 
        self.path = path 
        self.size = size 
        self.parent: Item|None = None 
        self.children: list[Item]|None = None 
    
    @property
    def isDir(self) -> bool:
        return self.children is not None 

    def computeSize(self):
        if self.children is None: return 
        size = 0
        for child in self.children:
            size += child.size 
        self.size = size

FileSystem = dict[str,Item]
cmdCD = "$ cd"
cmdLS = "$ ls"
pathGlue = "/"

def data(full: bool) -> FileSystem:
    fs: FileSystem = {}
    cwd: Item|None = None
    for line in readLines(22, 7, full):
        if line.startswith(cmdCD):
            name = line.split()[2]
            if name == ".." and cwd != None:
                cwd = cwd.parent 
            else:
                cwd, _ = getDir(fs, name, cwd)
        elif line == cmdLS:
            continue 
        else:
            head, tail = line.split()
            if head == 'dir':
                item, isNew = getDir(fs, tail, cwd)
                if isNew and cwd != None and cwd.children != None: 
                    cwd.children.append(item)
            else:
                item, isNew = getFile(fs, tail, int(head), cwd)
                if isNew and cwd != None and cwd.children != None:
                    cwd.children.append(item)
    
    dirPaths: list[str] = []
    for path, item in fs.items():
        if item.isDir: dirPaths.append(path)
    # Sort by path depth, process deepest-first
    dirPaths.sort(key = lambda p: len(p.split(pathGlue)), reverse=True)
    for path in dirPaths:
        fs[path].computeSize()
    return fs

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> int:
    fs = data(full=True)
    def totalSize(item: Item) -> int:
        if item.isDir and item.size <= 100_000:
            return item.size
        return 0
    items = [i for i in fs.values()] 
    return getTotal(items, totalSize)

def part2() -> int:
    fs = data(full=True) 
    total = 70_000_000
    required = 30_000_000 
    free = total - fs['/'].size 
    minimum = required - free 

    minSize = sys.maxsize
    for item in fs.values():
        if item.isDir and item.size >= minimum:
            minSize = min(minSize, item.size)
    return minSize

def getDir(fs: FileSystem, name: str, parent: Item|None) -> tuple[Item, bool]:
    path = name if parent is None else parent.path + name + pathGlue 
    item = fs.get(path, None)
    if item != None: # already existing
        return item, False 
    item = Item(name, path, 0)
    item.parent = parent 
    item.children = []
    fs[path] = item 
    return item, True

def getFile(fs: FileSystem, name: str, size: int, parent: Item|None) -> tuple[Item, bool]:
    path = name if parent is None else parent.path + name 
    item = fs.get(path, None)
    if item != None: # already existing 
        return item, False 
    item = Item(name, path, size)
    item.parent = parent 
    fs[path] = item 
    return item, True

if __name__ == '__main__':
    do(solve, 22, 7)

'''
Part1:
- Get FileSystem items that are directories and with size <= 100,000
- Output the total size of these items

Part2:
- Total disk space = 70M; free disk space = 70M - size of root directory 
- Required free space = 30M; minimum size to delete = 30M - free space
- Get FileSystem directories with size >= minimum 
- Output the minimum size of valid directories

FileSystem:
- Process the commands one line at a time 
- If cd command:
    - If cd .., change cwd to the cwd's parent 
    - Otherwise, change the cwd to the directory name 
- Skip the LS command, only interested in what follows
- Otherwise, this are lines after LS (could be file or dir)
- If dir, use getDir and add to the cwd's children 
- If file, use getFile (with its filesize) and add to the cwd's children
- After building the FS, compute the sizes of directories
- Get the directory paths and sort by depth (number of parts if split by /)
- Process deepest-first (leaf-to-root) directories [children before parents]
- Run computeSize on the directories; size = total size of children

GetDir/GetFile:
- Build the dir/file's path by combining the parent's path (if exists) and the file name
- If that path already exists in the fs, return it (with False = not new)
- If dir, initialize the children to empty list to make item.isDir true (not None)
- Otherwise, create the item and add to fs (return True to indicate new file)
'''