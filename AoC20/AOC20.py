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


#puzzle1.1 & 1.2 together
inputfile = "input_1.txt"
numbers = array_from_csv(inputfile)

# def multiply_2020_sum(numbers):
#     for i in numbers:
#         for j in numbers:
#             if i+j == 2020:
#                 return(i*j)

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


#puzzle2.1
inputfile = "input_2.txt"
pws = array_from_csv(inputfile)

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