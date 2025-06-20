# Advent of Code 2018 Day 07
# John Roy Daradal 

from aoc import *

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)

    def candidates(self, done: list[str]) -> list[str]:
        candidates = []
        for n in self.nodes:
            if n in done: continue 
            if all(dep in done for dep in self.edges[n]):
                candidates.append(n)
        return sorted(candidates)
    
    def nextTask(self, done: list[str]) -> str:
        return self.candidates(done)[0]

def data(full: bool) -> Graph:
    g = Graph()
    for line in readLines(18, 7, full):
        p = line.split()
        v1, v2 = p[1], p[-3]
        g.nodes.add(v1)
        g.nodes.add(v2)
        g.edges[v2].append(v1)
    for node in g.nodes:
        if node not in g.edges:
            g.edges[node] = []
    return g

def solve() -> Solution:
    return newSolution(part1(), part2())

def part1() -> str:
    g = data(full=True)
    order = []
    for _ in range(len(g.nodes)):
        node = g.nextTask(order)
        order.append(node)
    order = ''.join(order) 
    return order

def part2() -> int:
    g = data(full=True)
    limit = len(g.nodes)
    fixed, workers = 60, 5
    timer = 0
    done, ongoing = [], []
    queue = {i: ('', 0) for i in range(workers)}
    while len(done) < limit:
        candidates = [x for x in g.candidates(done) if x not in ongoing]
        available  = [i for i,task in queue.items() if task[0] == '']
        count = min(len(candidates), len(available))
        for i in range(count):
            q, node = available[i], candidates[i]
            queue[q] = (node, duration(node) + fixed)
            ongoing.append(node)

        for i in range(workers):
            task, left = queue[i]
            if task == '': continue 
            left -= 1 
            if left == 0:
                queue[i] = ('', 0)
                done.append(task)
                ongoing.remove(task)
            else:
                queue[i] = (task,left)
        timer += 1
    return timer

def duration(task: str) -> int:
    return ord(task) - 64

if __name__ == '__main__':
    do(solve, 18, 7)

'''
Part1:
- Topologically sort the tasks
- Select the next task with all dependency tasks already done

Part2:
- Initialize queues for each worker (no task yet)
- Candidate tasks are all tasks with all dependencies already done and not ongoing
- Count the number of available queues (no task assigned)
- Get the min between number of candidate tasks and number of available queues
- Assign the  candidate tasks to the available queues, add to ongoing list
- Duration of task depends on its ord(x), with the fixed time added
- For each queue with a task, decrement the time left to finish 
- Once a task in a queue hits 0 time left, we can free up that queue,
  add the task to done and remove from ongoing
- Increase the timer tick after each round
- Output the timer value after all tasks done processing
'''