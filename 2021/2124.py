# Advent of Code 2021 Day 24
# John Roy Daradal 

from aoc import *

def data(full: bool) -> list[str3]:
    def fn(line: str) -> str3:
        p = splitStr(line, None)
        if len(p) == 2:
            p1, p2 = p 
            return (p1, p2, '')
        else:
            p1, p2, p3 = p  
            return (p1, p2, p3)
    return [fn(line) for line in readLines(21, 24, full)]

def solve() -> Solution:
    commands = data(full=True)
    variables = extractVariables(commands)

    # Part 1 
    w = [9] * 14
    model1 = findBestModel(variables, w)

    # Part 2 
    w = [1] * 14 
    model2 = findBestModel(variables, w)

    return newSolution(model1, model2)

def findBestModel(variables: list[int3], w: list[int]) -> str:
    stack: list[int2] = []
    for idx, (a,b,c) in enumerate(variables):
        if a == 1:
            stack.append((idx, c))
        elif a == 26:
            pairIdx, lastC = stack.pop()
            # enforce the equality
            w[idx] = w[pairIdx] + lastC + b 
            if w[idx] > 9:
                extra = w[idx] - 9      # by how much does model[idx] exceed 9
                w[pairIdx] -= extra     # remove the extra from the pair
                w[idx] = 9              # cap model[idx] at 9 
            elif w[idx] < 1:
                deficit = 1 - w[idx]    # by how much does model[idx] lack to reach 1 
                w[pairIdx] += deficit   # add the deficit to the pair
                w[idx] = 1              # floor model[idx] at 1

    return ''.join([str(i) for i in w])

def extractVariables(commands: list[str3]) -> list[int3]: 
    variables: list[int3] = []
    for i in range(0, len(commands), 18):
        cmdA = commands[i+4]
        cmdB = commands[i+5]
        cmdC = commands[i+15]
        a, b, c = int(cmdA[2]), int(cmdB[2]), int(cmdC[2])
        variables.append((a,b,c))
    return variables

if __name__ == '__main__':
    do(solve, 21, 24)

'''
Solve: 
- From manual analysis of the program, there are 18 lines repeated 14 times:
    - In each subprogram, it only varies in the parameters at command 4, 5, and 15 (0-based index)
    - Extract the 3 variables (A@4,B@5,C@15) for the 14 subprograms
- By manual analysis of the subprogram structure, we can reduce it to this code:
        w = input                           Line 0
        x = (z % 26) + B == w ? 0 : 1       Line 3-4,6-8
        z = z // A                          Line 5
        z = (z * ((25*x)+1)) + ((w+C)*x)    Line 9-13, 14-18
- There are 2 types of subprograms: A=1 and A=26
- From the subprogram variables, we observe that if A=1, B >= 10 and if A=26, B <= 0
- For A=1 subprograms, we can simplify the code to:
        w = input 
        z = (z*26) + (w+C)
    - w has range 1..9, but since we add B which has range >= 10, the equality comparison will never be True
    - Therefore, x will always be 1 if A=1
    - We can ignore z = z // 1
    - Simplifying the last line, with x =1, it becomes z = (z*26) + (w+C)
- For A=26 subprograms, we can simplify the code to:
        w = input 
        if (z % 26) + B == w:
            z = z//26
        else:
            z = ((z//26)*26) + (w+C)
- The program start with several A=1 subprograms:
    - A=1 subprograms create next z using z = (z*26) + (w+C)
    - The current z is multiplied by 26, and we add (w+C)
    - This makes the z value larger every time we encounter A=1 subprograms
- The program ends with several A=26 subprograms:
    - A=26 subprograms can either divide z by 26 [if-part] 
      or keep the z at around the same magnitude and add (w+c) [else-part]
    - Since we want z=0 at the end for the model to be valid, we need to match the 
      (z*26) of A=1 subprograms with (z//26) for each A=26 subprograms for z to eventually be back to 0
    - The number of A=1 and A=26 subprograms also match (7 each)
    - But, the only way we can force the subprogram to divide by 26 is for the if-condition to be true
    - The model number will be valid if we always force (z%26)+B == w for A=26 subprograms
- So far, what we know is the ff:
    - For A=1 subprograms, we multiply z by 26 and add (w+C)
    - For A=26 subprograms, we must force (z%26)+B == w, so that we can divide z by 26, 
      hoping that it will eventually reduce to 0 at the end
    - What is z%26? This would be the (w+C) added by the A=1 subprogram!
    - In A=1, we multiply by 26 and add(w+C), so in A=26, when we z%26, the result would be (w+C)
    - So we need to enforce: (w_lastA1 + C_lastA1) + B_currA26 == w_currA26
    - So for A=1 subprograms, need to remember their C value
    - And for A=26 subprograms, need to remember their B value
- We can use a stack to pair off the A=1 (x26 + (w+C)) and A=26 (/26) subprograms:
    - If we see an A=1 subprogram, push its model index and C value 
    - If we see an A=26 subprogram, pop off the top item in the stack and enforce the equality above
    - If the w_currA26 value goes over 9, we set w_currA26 to 9 and adjust the w_lastA1 accordingly 
    - If the w_currA26 value goes below 1, we set w_currA26 to 1 and ajdjust the w_lastA1 accordingly
- For Part 1, we want the max model number, so we initialize our model to all 9s [14x]
- For Part 2, we want the min model number, so we initialize our model to all 1s [14x]
'''