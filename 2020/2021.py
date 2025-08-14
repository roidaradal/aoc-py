# Advent of Code 2020 Day 21
# John Roy Daradal 

from aoc import *

Pair = tuple[set[str], set[str]]

def data(full: bool) -> list[Pair]:
    def fn(line: str) -> Pair:
        line = line.strip(')').replace('contains', '')
        head, tail = splitStr(line, '(')
        ingredients = set(splitStr(head, None))
        allergens = set(splitStr(tail, ','))
        return ingredients, allergens
    return [fn(line) for line in readLines(20, 21, full)]

def solve() -> Solution:
    foods = data(full=True)

    # Part 1
    freq: dict[str, int] = defaultdict(int)
    candidates: dict[str, set[str]] = defaultdict(set)
    for ingredients, allergens in foods:
        for ingredient in ingredients:
            freq[ingredient] += 1
        for allergen in allergens:
            if len(candidates[allergen]) == 0:
                candidates[allergen] = ingredients 
            else:
                candidates[allergen] = candidates[allergen].intersection(ingredients)
    
    possible: set[str] = set()
    for ingredients in candidates.values():
        possible = possible.union(ingredients)
    
    for ingredient in possible:
        del freq[ingredient]
    count = sum(freq.values())

    # Part 2 
    T: dict[str, str] = {}
    for _ in range(len(candidates)):
        sureFood, sureAllergen = '', ''
        for allergen, domain in candidates.items():
            if len(domain) == 1:
                sureAllergen = allergen 
                sureFood = tuple(domain)[0]
                break 
        T[sureAllergen] = sureFood 
        for allergen in candidates:
            if sureFood in candidates[allergen]:
                candidates[allergen].remove(sureFood)
    dangerous = ','.join([T[allergen] for allergen in sorted(T.keys())])

    return newSolution(count, dangerous)

if __name__ == '__main__':
    do(solve, 20, 21)

'''
Part1:
- Go through the ingredients and allergens from the food list 
- Update the frequency of each ingredient encountered
- For each allergen, if the candidates for that allergen is still empty, initialize the candidates
  to the set of ingredients for this pairing
- If the candidates for allergen have already been established, take the intersection of existing and 
  the current set of ingredients
- Get the set of ingredients that are possible allergens, by taking the union of allergen candidates
- Remove the allergen candidates from the frequency table, leaving the non-allergen candidates
- Output the total frequency of non-allergen candidates

Part2:
- From the allergen and their candidate ingredients from Part 1, this forms a value => domain 
- Deduce the allergen => ingredient mapping by finding allergens with only 1 candidate left in the domain
- This will be a sure allergen => ingredient mapping, add it to the translation table
- Remove this ingredient from other unmapped allergen's domains, which in turn creates another singleton domain for another allergen
- After finding the final allergen => ingredient mapping, sort the allergens alphabetically
- Output the mapped ingredients from the sorted allergens, joined by comma
'''