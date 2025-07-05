# Advent of Code 2020 Day 18
# John Roy Daradal 

import re
from aoc import *

def data(full: bool) -> list[str]:
    def fn(line: str) -> str:
        line = line.replace(' ', '')
        return f'({line})'
    return [fn(line) for line in readLines(20, 18, full)]

def solve() -> Solution:
    exprs = data(full=True)

    # Part 1 
    eval1 = lambda expr: int(evaluateExpr(expr))
    total1 = getTotal(exprs, eval1)

    # Part 2 
    eval2 = lambda expr: int(evaluateExpr2(expr))
    total2 = getTotal(exprs,eval2)

    return newSolution(total1, total2)

def evaluateOp(op: str, lhs: str, rhs: str) -> str:
    a, b = int(lhs), int(rhs)
    match op:
        case '+':
            return str(a+b)
        case '*':
            return str(a*b)
    return '0'

def evaluateExpr(expr: str) -> str:
    # Remove expr parens
    expr = expr[1:-1]
    lhs, op = '', ''
    curr = ''
    i, limit = 0, len(expr)
    while i < limit:
        char = expr[i]
        if char == '(':
            closer = findCloser(expr, i)
            curr = evaluateExpr(expr[i:closer+1])
            i = closer+1
        elif char in ('+','*'):
            if lhs == '':
                lhs = curr
            else:
                lhs = evaluateOp(op, lhs, curr)
            op = char
            curr = ''
            i += 1
        else: # if digit, add to current
            curr += char
            i += 1
    return evaluateOp(op, lhs, curr)

def evaluateExpr2(expr: str) -> str:
    # Remove expr parens 
    expr = expr[1:-1]
    lhs, op = '', ''
    curr, expr2 = '', ''
    i, limit = 0, len(expr)
    while i < limit:
        char = expr[i]
        if char == '(':
            closer = findCloser(expr, i)
            curr = evaluateExpr2(expr[i:closer+1])
            i = closer+1
        elif char in ('+','*'):
            if lhs == '':
                lhs = curr 
            else:
                if op == '+':
                    lhs = evaluateOp(op, lhs, curr)
                elif op == '*':
                    expr2 += lhs + '*'
                    lhs = curr
            op = char
            curr = ''
            i += 1
        else: # digit, add to current 
            curr += char 
            i += 1

    tail = '' 
    if op == '+':
        tail = evaluateOp(op, lhs, curr)
    elif op == '*':
        tail = f'{lhs}*{curr}'
    expr2 += tail
    return evaluateExpr(f'({expr2})') if '*' in expr2 else expr2 

if __name__ == '__main__':
    do(solve, 20, 18)

'''
Solve: 
- Wrap each expression in parentheses
- For Part 1, get the total of evaluated expressions using left-to-right parsing:
    - Remove the expression parentheses 
    - Start with the lhs, op, and curr to be empty
    - Go through the characters in the expression one at a time 
    - If we see a digit, add to the current string and move to next char 
    - If we see operators (+,*):
        - If lhs is still empty, we set the lhs to the current string 
        - If lhs is already set (and so will op), we evaluate: lhs op curr and set the result as the new lhs 
        - Either way, we remember this current op (for next operation) and reset curr to empty; move to next char
    - If we see an opening parentheses, we have found a group:
        - Find the closing parentheses so we can get the full group text 
        - We set current string to result of recursively calling evaluateExpr on the group
        - We skip all the way to the char after the group
    - Return the final evaluation of the remaining lhs op curr
- For Part 2, get the total of evaluated expressions where sum has higher precedence:
    - Similar to Part 1: remove expr parens, go through expr chars
    - Similar processing for digits and seeing a group: call itself recursively on the group 
    - Also similar processing for operators when lhs is empty, and remembering current op and resetting the curr to blank
    - However, we only evaluate the lhs op curr if the operator is + 
    - If the operator is *, we add it to the residual expression
    - After exiting the loop, check the remaining op:
        - If +, the tail is lhs op curr 
        - If *, keep the expression string lhs*curr
    - Add the tail to residual expression
    - Check if still has operator * in residual expression
    - If there is, call the evaluateExpr from Part 1 on it
    - Otherwise, the outer operators must have been all + and we can return the final value
'''