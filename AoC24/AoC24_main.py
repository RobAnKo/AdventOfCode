#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 09:14:45 2024

@author: karlchen
"""
import numpy as np
import re
from typing import Union, List
from copy import deepcopy
from collections import deque
from math import log10, gcd
from itertools import combinations
from operator import sub
def lines_from_txt(path:str, typ:str = "string") -> list:
    with open(path, 'r') as in_f:
        lines = (line.rstrip('\n') for line in in_f.readlines())
    if typ == "string":
        return list(lines)
    elif typ == "float":
        return list(float(x) for x in lines)
    elif typ == "int":
        return list(int(x) for x in lines)
    else:
        print('typ has to be one of ["string", "float", "int"]')
        return None
    
def array_from_txt(path:str):
    with open(path, "r") as in_f:
        lines = np.array([list(line.rstrip("\n")) for line in in_f.readlines()])
    return lines
        
'''
## Puzzle 1.1
path = "./input_1.txt"
nums = lines_from_txt(path, typ= "string")
nums = [[int(x) for x in re.split("\s+", line)] for line in nums]
nums = [[nums[j][i] for j in range(len(nums))] for i in range(2)]    

def puzzle1_fun(nums):
    nums = [sorted(n) for n in nums]
    ans = sum((abs(x1-x2) for x1,x2 in zip(nums[0],nums[1])))
    return ans
        
#print(puzzle1_fun(nums))  

## Puzzle 1.2
def puzzle1_fun2(nums):
    d = {}
    simil_score = 0
    
    for n1 in nums[0]:
        if n1 not in d:
            d[n1] = n1 * sum((True for n2 in nums[1] if n1==n2))
        simil_score += d[n1]
        
    return simil_score


#print(puzzle1_fun2(nums))  


## Puzzle 2.1
path = "./input_2.txt"
reports = lines_from_txt(path)
reports = [[int(x) for x in re.split("\s+", line)] for line in reports]

def test_report(report: list, dampener: bool = False) -> bool:
    
    #base behaviour
    if not dampener:
        if report[0] < report[1]: #increase
            change = 1
        elif report[0] > report[1]: #decrease
            change = -1
        else: #no change -> not safe
            return False
        
        for i in range(len(report)-1): #go through all entries in report
            diff = report[i+1] - report[i]
            if (change == 1 and #increasing
            not (1 <= diff <= 3)): #not within allowed range
                    return False
            if (change == -1 and #decreasing
            not (-3 <= diff <= -1)):
                    return False
        return True #all diffs are within the allowed range
    
    #special case: one problem allowed
    else:
        for i in range(len(report)): #pop an individual value each time
            new_report = report.copy()
            new_report.pop(i)
            if test_report(new_report): #one safe version is enough
                return True
        return False #no reduced reports are safe
        
def puzzle2_fun1(reports):
    return sum(test_report(report, dampener=False) for report in reports)


#print(puzzle2_fun1(reports))

## Puzzle 2.2
def puzzle2_fun2(reports):
    return sum(test_report(report, dampener=True) for report in reports)

#print(puzzle2_fun2(reports))

## Puzzle 3.1
path = "./input_3.txt"
memory = "".join(lines_from_txt(path))

def mul_from_string(expression: str) -> int:
    numbers = [int(n) for n in expression.split(",")]
    return numbers[0]*numbers[1]

def extract_valid_muls(memory: str) -> List[str]:
    return re.findall("mul\((\d+?,\d+?)\)", memory)
    

def puzzle3_fun1(memory: str) -> int:
    muls = extract_valid_muls(memory)
    results = [mul_from_string(expression) for expression in muls]
    return sum(results)
    
#print(puzzle3_fun1(memory))

## Puzzle 3.1

def puzzle3_fun2(memory: str) -> int:
    result = 0
    do = True
    
    pattern = re.compile(r"mul\((\d+?,\d+?)\)")
    
    for i in range(len(memory)):
        if memory[i:i+2] == "do":
            if memory[i+2:i+4] == "()":
                do = True
                print("hactivation")
            elif memory[i+2:i+7] == "n't()":
                do = False         
                print("deactivation")
        elif memory[i:i+4] == "mul(":
            if do:
                mul = pattern.search(memory[i:i+13])
                if mul:
                    mul = mul.group(1)
                    print(mul)
                    temp = mul_from_string(mul)
                    print(f"temp: {temp}")
                    result += temp
    return result
                
#print(puzzle3_fun2(memory))

## Puzzle 4.1
    
path = "./input_4.txt"
word_search = np.array([[x for x in line] for line in lines_from_txt(path)])


def occurence_at_index(i,j,word_search):
    shape = word_search.shape

    words = [[word_search[i, j+t] for t in range(4) if j+t < shape[1]], #E
            [word_search[i, j-t] for t in range(4) if j-t >= 0], #W
            [word_search[i+t, j] for t in range(4) if i+t < shape[0]], #S
            [word_search[i-t, j] for t in range(4) if i-t >= 0], #N
            [word_search[i-t, j+t] for t in range(4) if i-t >= 0 and j+t < shape[1]], #NE
            [word_search[i+t, j+t] for t in range(4) if i+t < shape[0] and j+t < shape[1]], #SE
            [word_search[i+t, j-t] for t in range(4) if i+t < shape[0] and j-t >= 0], #SW
            [word_search[i-t, j-t] for t in range(4) if i-t >= 0 and j-t >= 0]] #NW
    
    counter = 0
    for w in words:
        #print(w)
        res = "".join(w)
        if res == "XMAS":
            counter += 1
    
    return counter
    
    
    
def puzzle4_fun1(word_search):
    n_xmas = 0
    
    for i,line in enumerate(word_search):
        for j, letter in enumerate(line):
            if letter == "X":
                n_xmas += occurence_at_index(i,j, word_search)
    
    return n_xmas

#print(puzzle4_fun1(word_search))


def test_position(i,j,word_search):
    shape = word_search.shape
    diag1 = "".join([word_search[i+t,j+t] for t in range(-1,2) 
                    if (0 <= i+t < shape[0] and
                        0 <= j+t < shape[1])])
    diag2 = "".join([word_search[i-t,j+t] for t in range(-1,2) 
                    if (0 <= i-t < shape[0] and
                        0 <= j+t < shape[1])])
  
        
    return ((diag1 == "SAM" or diag1 == "MAS") and
        (diag2 == "SAM" or diag2 == "MAS"))
           
    return ()
    
def puzzle4_fun2(word_search):
    n_xmas = 0
    
    for i, line in enumerate(word_search):
        for j, letter in enumerate(line):
            if letter == "A":
                n_xmas += test_position(i,j,word_search)
    return n_xmas

#print(puzzle4_fun2(word_search))


                
## Puzzle 5.1
path = "./input_5.txt"
inp = lines_from_txt(path)

def get_rules_and_updates(inp):
    rules = {}
    updates = []
    for line in inp:
        if "|" in line:
            sp = [int(x) for x in line.split("|")]
            if sp[0] in rules:
                rules[sp[0]].append(sp[1])
            else:
                rules[sp[0]] = [sp[1]]
        elif "," in line:
            updates.append([int(x) for x in line.split(",")])
    
    return rules, updates
        
def test_update(update, rules):
    
    for i, val in enumerate(update):
        if val in rules:
            values_after = rules[val]
            for val_after in values_after:
                if val_after in update[:i]:
                    return False #rule broken
    return True

def puzzle5_fun1(inp):
    ans = 0
    rules, updates = get_rules_and_updates(inp)
    
    for update in updates:
        if test_update(update, rules):
            ans += update[len(update)//2]
    
    return ans

#print(puzzle5_fun1(inp))
    
## Puzzle 5.2


def fix_update(update, rules):
    fixed = False
    for i, val in enumerate(update):
        if val in rules:
            values_after = rules[val]
            for val_after in values_after:
                if val_after in update[:i]:
                    update.remove(val_after)
                    update.append(val_after)
                    fixed = True
    if fixed:
        update = fix_update(update, rules)
    return update

    
def puzzle5_fun2(inp):
    ans = 0
    rules, updates = get_rules_and_updates(inp)
    
    for update in updates:
        if not test_update(update, rules):
            update = fix_update(update, rules)
            ans += update[len(update)//2]
    return ans

print(puzzle5_fun2(inp))



## Puzzle 6.1
path = "./input_6.txt"
inp = array_from_txt(path)





def puzzle6_fun0(inp, part2 = False):
    shape = inp.shape
    
    seen = set()

    direction_map = {0: (-1,0), #N
                     1: (0,1), #E
                     2: (1,0), #S
                     3: (0,-1) #W
                     } 
    
    for direction, sign in enumerate(["^", ">", "v", "<"]):
        if sign in inp:
            start = tuple(int(x) for x in np.where(inp == sign))
            seen.add(start)
            dy, dx = direction_map[direction]
            break
    
    y, x = start
    
    while y + dy in range(shape[0]) and x + dx in range(shape[1]):
        dy, dx = direction_map[direction]
        next_pos = (y+dy, x+dx)
        if inp[next_pos] == "#":
            direction += 1
            direction %= 4
        else:
            y += dy
            x += dx
            seen.add((y,x))
    
    if not part2: return len(seen)
    
    else:
        res = 0
        seen.remove(start)
        for y,x in seen:
            #print(y,x)
            inp[y,x] = "#"
            if test_for_loop(inp):
                #print("Found one!")
                res += 1
            inp[y,x] = "."
        return res
        
            
            
def test_for_loop(inp):
    shape = inp.shape
    
    direction_map = {0: (-1,0), #N
                     1: (0,1), #E
                     2: (1,0), #S
                     3: (0,-1) #W
                     } 
    
    seen = set()
    
    
    for direction, sign in enumerate(["^", ">", "v", "<"]):
        if sign in inp:
            y,x = (int(x) for x in np.where(inp == sign))
            dy, dx = direction_map[direction]
            break
    
    
    while y + dy in range(shape[0]) and x + dx in range(shape[1]):
        seen.add((y,x, direction))
        dy, dx = direction_map[direction]
        next_pos = (y+dy, x+dx)
        if inp[next_pos] == "#":
            direction += 1
            direction %= 4
        else:
            y += dy
            x += dx
        if (y,x,direction) in seen:
            return True
    
    return False
            
print(puzzle6_fun0(inp))
print(puzzle6_fun0(inp, True))



## Puzzle 7.1 & 2

path = "./input_7.txt"
inp = lines_from_txt(path)
inp = [list(map(int, line.replace(":","").split(" "))) for line in inp]
#inp = (line.split(": ") for line in inp)
#inp = {int(s[0]): [int(x) for x in s[1].split(" ")] for s in inp}


#This solution was adapted from Verulean314 (https://www.reddit.com/r/adventofcode/comments/1h8l3z5/comment/m0tv6di/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)


#number of digits in a number
def digits(n):
    return int(log10(n)) + 1

#check whether a number a ends in another number b
def endswith(a, b):
    return (a - b) % 10 ** digits(b) == 0


def is_tractable(test_value, numbers, check_concat=True):
    *head, n = numbers
    if not head: #length of numbers == 1
        return n == test_value
    
    #test whether last number is a divisor of test value
    q, r = divmod(test_value, n)
    if r == 0 and is_tractable(q, head, check_concat):
        return True
    #test whether concatenation is a possible path
    if (check_concat and 
        endswith(test_value, n) and 
        is_tractable(test_value // (10 ** digits(n)), head, check_concat)): # since we can get it through concat, check the remainder digits
        return True
    #check whether addition is a possible path
    return is_tractable(test_value - n, head, check_concat)


def solve(data):
    ans1 = ans2 = 0
    for line in data:
        test_value, *numbers = line
        if is_tractable(test_value, numbers, False):
            ans1 += test_value
            ans2 += test_value
        elif is_tractable(test_value, numbers):
            ans2 += test_value
    return ans1, ans2

print(solve(inp))


## Puzzle 8.1 & 2

path = "./input_8.txt"
inp = array_from_txt(path)


def puzzle8_fun0(inp, with_harmonics=False):
    sh = inp.shape[0]
    
    unique_freqs = set(np.unique(inp))
    unique_freqs.remove(".")
    
    antinodes = set()
    
    for freq in unique_freqs:
        xs,ys = np.where(inp == freq)
        
        
        for xpair, ypair in zip(combinations(xs,2), combinations(ys,2)):
            a = np.array([xpair[0], ypair[0]])
            b = np.array([xpair[1], ypair[1]])
            #print(f"a: {a}")
            #print(f"b: {b}")
            if not with_harmonics:
                c = 2*a - b
                d = 2*b - a
            
                for antinode in [c,d]:
                    if ((antinode>=0) & (antinode<sh)).all():
                        antinodes.add(tuple(antinode))
            
            else: #including harmonics
                diffvec = b-a
                #print(f"diffvec: {diffvec}")
                diffvec = diffvec // gcd(*diffvec)
                #print(f"diffvec: {diffvec}")
                current = a.copy()
                while ((current>=0) & (current<sh)).all():
                    antinodes.add(tuple(current))
                    current -= diffvec
                current = a.copy()
                while ((current>=0) & (current<sh)).all():
                    antinodes.add(tuple(current))
                    current += diffvec
    #for an in antinodes:
    #    if inp[an] == ".":
    #        inp[an] = "#"
    #print(inp)
    return len(antinodes)

print(puzzle8_fun0(inp))
print(puzzle8_fun0(inp, True))

'''
## Puzzle 9.1

path = "./input_9_test.txt"
inp = [int(x) for x in lines_from_txt(path)[0]]

def translate(raw: list) -> list:
    raw_idx = 0
    block_idx = 0
    blocks = [None for _ in range(len(raw)*9)]
    ID = 0
    
    while raw_idx < len(raw):
        length = raw[raw_idx]
        if not raw_idx % 2: #even -> data block
            blocks[block_idx:block_idx+length] = [ID for _ in range(length)]
            ID += 1
        else: #uneven -> free space
            pass
        block_idx += length
        raw_idx += 1
    
    return blocks[:block_idx]


def idxs_to_intervals(idxs: list) -> list:
    start_idx = 0
    stop_idx = 1
    intervals = []
    reached = False
    
    while not reached:
        current = idxs[start_idx]    
        stop_val = idxs[stop_idx]
        while stop_val - current == 1:
            current = stop_val
            stop_idx += 1
            if stop_idx < len(idxs):
                stop_val = idxs[stop_idx]
            else:
                reached = True
                break
        print([idxs[start_idx], stop_val])
        intervals.append([idxs[start_idx], stop_val])
        start_idx, stop_idx = stop_idx+1, stop_idx + 1
    
    return intervals
        

def compress(blocks, fullfiles=False):
    empty_idxs = [i for i,b in enumerate(blocks) if b is None]
    
    empty_blocks = idxs_to_intervals(empty_idxs)
    
    if not fullfiles:
        empty_pointer = 0
        put_idx = empty_idxs[empty_pointer]
        
        while put_idx < len(blocks):
            to_move = blocks.pop()
            if to_move is not None:
                blocks[put_idx] = to_move
                empty_pointer += 1
                put_idx = empty_idxs[empty_pointer]
    else:
        pass
        
        
    return blocks

def checksum(blocks):
    cs = 0
    
    for i, b in enumerate(blocks):
        cs += i*b

    return cs


def puzzle9_fun1(inp):
    blocks = translate(inp)
    compressed = compress(blocks)
    cs = checksum(compressed)
    return cs


def puzzle9_fun2(inp):
    blocks = translate(inp)
    compressed = compress(blocks, fullfiles=True)
    cs = checksum(compressed)
    return cs

print(puzzle9_fun1(inp))
print(puzzle9_fun2(inp))
