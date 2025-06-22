# Advent of Code 2021 Day 13
# John Roy Daradal 

from aoc import *

def data(full: bool) -> tuple[list[coords], list[strInt]]:
    fold = False 
    dots: list[coords] = []
    folds: list[strInt] = []
    for line in readLines(21, 13, full):
        if line == '':
            fold = True 
        elif fold:
            axis, value = splitStr(splitStr(line, None)[-1], '=')
            folds.append((axis, int(value)))
        else:
            x,y = toInt2(line, ',')
            dots.append((y,x))
    return dots, folds

def solve() -> Solution:
    dots, folds = data(full=True)

    # Part 1 
    count = foldPaper(dots, folds, True)

    # Part 2
    foldPaper(dots, folds, False)

    return newSolution(count, "")

Paper = list[list[str]]

def foldPaper(dots: list[coords], folds: list[strInt], firstOnly: bool) -> int:
    rows = max(c[0] for c in dots) + 1 
    cols = max(c[1] for c in dots) + 1 
    paper: Paper = [['.' for _ in range(cols)] for _ in range(rows)]
    for r,c in dots: paper[r][c] = '#'

    for axis,repeat in folds:
        if axis == 'y':
            paper = foldUp(paper, repeat)
        elif axis == 'x':
            paper = foldLeft(paper, repeat)
        if firstOnly: break 
    
    if not firstOnly:
        for line in paper:
            print(''.join(line))
    
    count = sum(sum(1 for char in line if char == '#') for line in paper)
    return count

def foldUp(paper: Paper, fold: int) -> Paper:
    half1 = paper[:fold]
    half2 = paper[fold+1:][::-1]
    size1, size2 = len(half1), len(half2)
    paper2: Paper = []
    if size1 >= size2:
        offset = size1-size2 
        paper2 += half1[:offset]
        for i, line2 in enumerate(half2):
            line1 = half1[offset+i]
            paper2.append(merge(line1, line2))
    else:
        offset = size2-size1 
        paper2 += half2[:offset]
        for i, line1 in enumerate(half1):
            line2 = half2[offset+i]
            paper2.append(merge(line1, line2))
    return paper2

def foldLeft(paper: Paper, fold: int) -> Paper:
    paper2: Paper = []
    for line in paper:
        half1 = line[:fold]
        half2 = line[fold+1:][::-1]
        size1, size2 = len(half1), len(half2)
        line2: list[str] = []
        if size1 >= size2:
            offset = size1-size2 
            line2 += half1[:offset]
            line2 += merge(half1[offset:], half2)
        else:
            offset = size2-size1 
            line2 += half2[:offset]
            line2 += merge(half1, half2[:offset])
        paper2.append(line2)
    return paper2

def merge(line1: list[str], line2: list[str]) -> list[str]:
    return ['#' if '#' in (m1,m2) else '.' for m1,m2 in zip(line1,line2)]

if __name__ == '__main__':
    do(solve, 21, 13)

'''
Solve:
- For Part 1, fold once and count the number of # in the resulting paper 
- For Part 2, do all the folds and display the paper to reveal the 8-letter code 

FoldPaper:
- Initialize the paper with blanks (.), add the dots as # 
- Process the fold commands in order: for y-axis: fold up, for x-axis, fold left
- Fold Up at y=fold:
    - First half is the rows from 0 to fold 
    - Second half is rows fro fold+1 to the end, but reversed (since it's being folded up)
    - If half1 is bigger than half2:
        - Compute the outer rows that is all half1 (size1-size2)
        - Add the outer rows of half1 to the resulting paper 
        - For the overlapping part of half1 and half2, merge their pixels:
          if either of them is #, result is #, otherwise .
    - Process is similar for half2 > half1; just reversed roles
- Fold Left at x=fold:
    - Process each line of the paper 
    - First half is the line's column 0 up to fold 
    - Second half is from fold+1 to the end, but reversed (since it's being folded left)
    - Compare the sizes of half1 and half2, similar to fold up 
    - Initialize the resulting paper with the outer collumns of the bigger half 
    - For the overlapping parts, merge their pixels similar to above
'''