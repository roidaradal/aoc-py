from aoc import str2 

EdgeMap = dict[str2, int]

class Graph:
    def __init__(self):
        self.vertices: set[str] = set()
        self.edges: EdgeMap = {}