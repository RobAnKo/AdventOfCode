#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 17:47:27 2019

@author: robinkoch
"""

import os
import numpy as np
from array import array
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sn
import re
from sortedcontainers import SortedSet
import scipy
from scipy import signal
from datetime import datetime
import copy
import time
from functools import reduce
os.chdir("/home/robinkoch/Documents/AdventOfCode/AoC20")


def array_from_csv(inputfile):
    return pd.read_csv(inputfile, header = None).values


# puzzle 1.1 & 1.2 together
inputfile = "input_1.txt"
numbers = array_from_csv(inputfile)


def multiply_2020_sum(numbers,n):
    combs = list(itertools.combinations(numbers, n))
    #generator because only used once
    sums = (sum(x) for x in combs)
    mults = np.array([mult(x) if y==2020 else 0 for x,y in zip(combs,sums)])
    return(int(mults[mults.nonzero()]))


def mult(args):
    prod = 1
    for a in args:
        prod *=a
    return prod



print(multiply_2020_sum(numbers,2))
print(multiply_2020_sum(numbers,3))

####
        #We learned here that itertools might be faster than for-loops, but doesn't have to be. 
        #It depends on size of problem and location of solution.
####


# puzzle 2
inputfile = "input_2.txt"
pws = array_from_csv(inputfile)


# puzzle 2.1
def number_of_valid_pws(pws):
    n = 0
    for pw in pws:
        parts = pw[0].split()
        range_ = parts[0]
        range_ = range_.split('-')
        mini = int(range_[0])
        maxi = int(range_[1])
        letter = parts[1][0]
        password = parts[2]
        if mini <= password.count(letter) <= maxi:
            n+=1
    return n


print(number_of_valid_pws(pws))
        
# puzzle 2.2
def number_of_valid_pws_2(pws):
    n = 0
    for pw in pws:
        parts = pw[0].split()
        indices = parts[0]
        indices = indices.split('-')
        i1 = int(indices[0])
        i2 = int(indices[1])
        letter = parts[1][0]
        password = parts[2]
        i1b = password[i1-1]==letter
        i2b = password[i2-1]==letter
        if i1b + i2b == 1:
            n+=1
    return n

print(number_of_valid_pws_2(pws))


# puzzle 3
inputfile = "input_3.txt"
mountain = array_from_csv(inputfile).astype('str')
directions = [[1,1],[3,1],[5,1],[7,1],[1,2]]

# puzzle 3.1
def tree_encounters(mountain, direction):
    h = len(mountain)
    w = len(mountain[0][0])
    posx = direction[0]
    posy = direction[1]
    path = ""
    while posy < h:
        path += mountain[posy][0][posx]
        posx += direction[0]
        posy += direction[1]
        if posx >= w:
            posx -= w
    print(path.count("#"))
    return path.count("#")

print(tree_encounters(mountain, directions[1]))


# puzzle 3.2
def multiple_tree_encounters(mountain, directions):
    tree_mult = 1
    for i in range(len(directions)):
        tree_mult *= tree_encounters(mountain, directions[i]);
    return tree_mult

print(multiple_tree_encounters(mountain, directions))

# puzzle 4
inputfile = "input_4.txt"
passport_data = array_from_csv(inputfile).astype('str')


# puzzle 4.1
def valid_passports(passport_data):
    return num_valid

print(valid_passports(passport_data))


# puzzle 4.2
def fun_4_2(passport_data):
    return 0

print(fun_4_2(passport_data))
