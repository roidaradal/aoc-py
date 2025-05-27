# Advent of Code 2021 Day 08
# John Roy Daradal 

from aoc import *

Pair = tuple[list[str], list[str]] # digits, output
Candidates = dict[int, list[str]]
Domain = dict[str, list[str]]
Clues = tuple[Candidates, Candidates] # Count, Length
Map = dict[str,str]

def data(full: bool) -> list[Pair]:
    def fn(line: str) -> Pair:
        head, tail = splitStr(line, '|')
        return head.split(), tail.split()
    return [fn(line) for line in readLines(21, 8, full)]

def part1():
    pairs = data(full=True)
    # Length of {1: 2, 4: 4, 7: 3, 8:7}
    fn = lambda p: sum(1 for x in p[1] if len(x) in (2,3,4,7))
    total = getTotal(pairs, fn)
    print(total)

def part2():
    pairs = data(full=True) 
    m, clues = digitMapClues()
    def fn(pair: Pair) -> int:
        return solve(pair, m, clues)
    total = getTotal(pairs, fn)
    print(total)

def digitMapClues() -> tuple[Map, Clues]:
    digits = [x  for x in 'abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg'.split()]
    m: Map = {}
    for i,code in enumerate(digits):
        m[code] = str(i)
    clues = getClues(digits)
    return m, clues

def getClues(digits: list[str]) -> Clues:
    freq: dict[str,int] = defaultdict(int)
    size: dict[str,int] = {}
    for d in digits:
        d = sortedStr(d)
        size[d] = len(d)
        for x in d:
            freq[x] += 1
    count: Candidates = defaultdict(list)
    length: Candidates = defaultdict(list)
    for k,v in freq.items():
        count[v].append(k)
    for k,v in size.items():
        length[v].append(k)
    return count, length

def solve(pair: Pair, m: Map, clues: Clues) -> int:
    digits, output = pair 
    clues2 = getClues(digits)
    t = alignClues(clues, clues2)
    return translateOutput(output, m, t)

def alignClues(clues1: Clues, clues2: Clues) -> Map:
    (count1,length1), (count2,length2) = clues1, clues2 
    t: Map = {}
    domain: Domain = {}
    for k, items2 in count2.items():
        items1 = count1[k]
        if len(items1) == 1 and len(items2) == 1:
            s1, s2 = items1[0], items2[0]
            t[s2] = s1 
        else:
            for s in items2:
                domain[s] = items1[:]
    
    for k in (2,3,4):
        code = length2[k][0]
        choices = set(length1[k][0])
        unmapped = set(code)
        while len(choices) > 1:
            for c in code:
                if c in t:
                    unmapped.remove(c)
                    choices.remove(t[c])
        if len(choices) == 1:
            b, a = list(unmapped)[0], list(choices)[0]
            t, domain = assign(b, a, t, domain)
    return t

def assign(b: str, a: str, t: Map, domain: Domain) -> tuple[Map, Domain]:
    t[b] = a 
    if b in domain:
        del domain[b]
    
    sure = []
    domain2: Domain = {}

    for k, items in domain.items():
        if a in items:
            items.remove(a)
        if len(items) == 1:
            sure.append((k, items[0]))
        else:
            domain2[k] = items 

    for (b,a) in sure:
        t, domain2 = assign(b,a,t,domain2)
    return t, domain2

def translateOutput(output: list[str], m: Map, t: Map) -> int:
    orig: list[str] = []
    for code in output:
        out = [t[x] for x in code]
        orig.append(''.join(sorted(out)))

    digit = [m[code] for code in orig]
    d = ''.join(digit)
    return int(d)

if __name__ == '__main__':
    do(part1)
    do(part2)

'''
Part1:
- Count the number of times digit 1,4,7,8 appears (they have unique segment counts)
- Go through the pairs and count the number of times the length 2,3,4,7 appears in the outputs

Part2:
- Get the original clues from the correct digit mapping (digitMapClues)
- For each pair (digits, output), solve the mapping by using the digitMapClues results
    - GetClues for the pair's digits 
    - Align the original clues from the pair's clues to produce the translation table
    - Use the translation table to produce the displayed digit
- Output the total of the displayed digits

GetClues:
- Given a list of segment activations that are translated, figure out clues to the mapping 
- Sort the digits to make it canonical form 
- Keep track of word sizes : some digits have unique lengths (1,4,7,8)
- Keep track of how many times each letter appears in the mapping
- Clue #1: Count = Group the letters by the number of times they appear in the words
- Clue #2: Length = Group the words by their lengths

AlignClues:
- Check the counts in clues2; if there is only 1 item with that count for both clues1 and clues2,
  we can assign the item in clues2 to be translated to the item in clues1
- Otherwise, we add items from clues1 to the domain of each item in clues2 (for that count)
- For length 2,3,4 (these are the lengths with multiple possible digits):
    - Use the first code with that length from clues2; initialize all letters to be unmapped
    - Initialize its choices to the letters of the first code with that length from clues1
    - Check each code letter; if already in translation table T, remove from unmapped and choices
    - If there is only 1 choice left, we can add this to the mapping

Assign:
- Add to the translation table, and delete from domain if still there 
- Remove from other domains (since already assigned)
- If another domain's size becomes 1, add to sure assignments 
- For sure assignments, call assign recursively
'''