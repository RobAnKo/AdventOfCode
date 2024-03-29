#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 4 10:44:27 2021

@author: robinkoch
"""

import os
import numpy as np
from array import array
import pandas as pd
import itertools
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sn
import re
from sortedcontainers import SortedSet
import scipy
from scipy import signal
from datetime import datetime
import copy
import time
#from math import comb as mathcomb
from functools import reduce
#os.chdir("/home/karlchen/Documents/AdventOfCode/AoC21")
os.chdir("/home/robinkoch/Documents/AdventOfCode/AoC21")



def lines_from_txt(inputfile, typ = "string"):
    with open(inputfile, 'r') as in_f:
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

    

#helper function for multiplication of all elements in an iterable
def mult(args):
    prod = 1
    for a in args:
        prod *=a
    return prod

'''

# puzzle 1.1
print("Puzzle 1")
inputfile = "input_1.txt"
ns = lines_from_txt(inputfile, typ="int")
res = sum(np.diff(ns)>0)
print(f"The solution is {res}")

# puzzle 1.2
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w
res = sum(np.diff(moving_average(ns,3))>0)
print(f"The solution is {res}")


# puzzle 2.1
print("Puzzle 2")
inputfile = "input_2.txt"
moves = pd.read_csv(inputfile, delimiter=" ", names = ["direction", "value"])
movsums = moves.groupby(by=["direction"]).sum()
res = (movsums.value.down-movsums.value.up)*movsums.value.forward
print(f"The solution is {res}")
# puzzle 2.2
def move_with_aim(moves):
    aim = 0
    xlocation = 0
    ylocation = 0
    for k in range(moves.shape[0]):
        move = moves.iloc[k]
        if move.direction == 'forward':
            xlocation += move.value
            ylocation += aim*move.value
        elif move.direction == 'up':
            aim -= move.value
        elif move.direction == 'down':
            aim += move.value
        else:
            pass
    return xlocation*ylocation

res = move_with_aim(moves)
print(f"The solution is {res}")


# puzzle 3.1
print("Puzzle 3")
inputfile = "input_3.txt"
diagnostics = lines_from_txt(inputfile, typ="string")

def energy_consumtion(diagnostics):
    n_lines = len(diagnostics[0])
    diagnostics = [[int(b) if b=="1" else 0 for b in d] for d in diagnostics]
    means = [np.mean([line[k] for line in diagnostics]) for k in range(n_lines)]
    gamma = "".join(["1" if m>0.5 else "0" for m in means])
    epsilon = "".join(["0" if x=="1" else "1" for x in gamma])
    return int(gamma, base=2)*int(epsilon, base=2)

res = energy_consumtion(diagnostics)
print(f"The solution is {res}")

# puzzle 3.2

def extract_position(iterables, position):
    return [iterable[position] for iterable in iterables]

def find_bit_criterium(values,typ="most"):
    occurence_count = Counter(values)
    nz = occurence_count["0"]
    no = occurence_count["1"]
    if typ=="most":
        if no>=nz:
            return "1"
        else:
            return "0"
    elif typ=="least":
        if no<nz:
            return "1"
        else:
            return "0"

def find_rating(inp,typ):
    diagnostics = copy.deepcopy(inp)
    k=0
    while len(diagnostics) > 1:
        values_at_k = extract_position(diagnostics, k)
        if typ=="oxygen":
            bc = find_bit_criterium(values_at_k, "most")
        elif typ == "CO2":
            bc = find_bit_criterium(values_at_k, "least")
        diagnostics = [d for d,v in zip(diagnostics, values_at_k) if v == bc]
        k+=1
    return diagnostics[0]

    
res = int(find_rating(diagnostics, "oxygen"),base=2)*int(find_rating(diagnostics, "CO2"), base=2)
print(f"The solution is {res}")


#Puzzle 4.1
from Bingo import Bingo

print("Puzzle 4")
inputfile = "input_4.txt"


b = Bingo(inputfile)
b.initiate()
b.run(typ="first")

#Puzzle 4.2
b = Bingo(inputfile)
b.initiate()
b.run(typ="last")



#Puzzle 5.1
print("Puzzle 5")
inputfile = "input_5.txt"

def read_vent_lines(inputfile):
    with open(inputfile, "r") as f:
        l = f.readlines()
    lines = [[[int(idx) for idx in point.split(",")] 
             for point in line.strip().split(" -> ")] 
              for line in l]
    return lines

def test_straight(lines):
    idxs = np.zeros(len(lines), dtype = np.bool)
    for i,line in enumerate(lines):
        idxs[i] = isstraight(line)
    return idxs

def isstraight(line):
    if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
        return True
    else:
        return False

def find_boundaries(lines):
    xs = [point[0] for line in lines for point in line]
    ys = [point[1] for line in lines for point in line]
    return (max(xs)+1,max(ys)+1)

def draw_map(lines, typ="straight"):
    if typ=="straight":
        idxs = test_straight(vent_lines)
        relevant_lines = [line for line,idx in zip(lines,idxs) if idx]
    elif typ=="all":
        relevant_lines = lines
    
    sz = find_boundaries(relevant_lines)
    ventmap = np.zeros(sz,dtype=int)
    for rl in relevant_lines:
        xpoints = [rl[0][0], rl[1][0]]
        ypoints = [rl[0][1], rl[1][1]]
        
        if xpoints[1] > xpoints[0]:
            xsteps = range(xpoints[0], xpoints[1]+1)
        else:
            xsteps = range(xpoints[0], xpoints[1]-1,-1)
        
        if ypoints[1] > ypoints[0]:
            ysteps = range(ypoints[0], ypoints[1]+1)
        else:
            ysteps = range(ypoints[0], ypoints[1]-1,-1)
        
        if len(xsteps) > len(ysteps):
            zip_list = zip(xsteps, itertools.cycle(ysteps)) 
        else:
            zip_list = zip(itertools.cycle(xsteps), ysteps)
        
        for x,y in zip_list:
            ventmap[x,y] += 1
    return ventmap
    

vent_lines = read_vent_lines(inputfile)
#5.1
ventmap = draw_map(vent_lines, typ="straight")
res = np.sum(ventmap>1)
print(f"The solution is {res}")
#5.2
ventmap = draw_map(vent_lines, typ="all")
res = np.sum(ventmap>1)
print(f"The solution is {res}")


#Puzzle 6
print("Puzzle 6")
inputfile = "input_6_test.txt"

from Lanternfish import Lanternfish_brute
L = Lanternfish_brute(inputfile)
n = 80
L.run(n)
print(f"There are {L.n_fish} lanternfish after {n} days.")

from Lanternfish import Lanternfish_smart
L = Lanternfish_smart(inputfile)
n = 256
L.run(n)
print(f"There are {L.n_fish} lanternfish after {n} days.")
'''


#Puzzle 7
print("Puzzle 7")
inputfile = "input_7.txt"

# with open(inputfile, "r") as f:
#     positions = [int(x) for x  in f.read().strip().split(",")]

# med = int(np.median(positions))
# fuel = sum([abs(p-med) for p in positions])
# print(f"The crabs need {fuel} fuel to get to position {med}.")

# from CrabSubmarine import FuelOptimizer

# fo = FuelOptimizer(inputfile)
# fo.find_min_fuel()
# print(f"The crabs need {fo.min_fuel} fuel to get to position {fo.best_position}")


print("Puzzle 8")
inputfile = "input_8.txt"

lines = lines_from_txt(inputfile)
inputs = [line.split("|")[0].strip().split(" ") for line in lines]
outputs = [line.split("|")[1].strip().split(" ") for line in lines]

unique_lengths = [2,3,4,7]
res = sum([len(op) in unique_lengths for ops in outputs for op in ops])

print(f"There are {res} unique lengths.")

from SSD import Decoder

res = sum([Decoder(line).calculate_output() for line in lines])
print(f"The result is {res}.")


print("Puzzle 9")
inputfile = "input_9.txt"
x = np.fromfile(inputfile)
x = lines_from_txt(inputfile)
nrows = len(x)
ncols = len(x[0])
arr = np.empty([ncols, nrows], dtype="int")

for r in range(nrows):
    row = [int(n) for n in list(x[r])]
    arr[:,r] = row

def is_lowpoint(arr,x,y):
    sz = arr.shape
    val = arr[x,y]
    neighbours = []
    if x > 0:
        neighbours.append(arr[x-1,y])
    if y > 0:
        neighbours.append(arr[x,y-1])
    if x < sz[0]-1:
        neighbours.append(arr[x+1,y])
    if y < sz[1]-1:
        neighbours.append(arr[x,y+1])
    
    if np.all([val < n for n in neighbours]):
        return True 
    else:
        return False

lowpoints = np.empty(arr.shape, dtype="bool")
for y in range(nrows):
    for x in range(ncols):
        lowpoints[x,y] = is_lowpoint(arr,x,y)

score = sum(arr[lowpoints] +1)
print(f"The number of basins is {np.sum(lowpoints)}, the total risk score is {score}.")


from skimage import measure
basins = arr != 9

all_labels = measure.label(basins, connectivity = 1)
props = measure.regionprops(all_labels)
areas = [prop.area for prop in props]
res = mult(sorted(areas, reverse=True)[0:3])

print(f"The product of the three largest basins is {res}.")
