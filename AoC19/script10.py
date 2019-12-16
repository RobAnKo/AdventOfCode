#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:25:54 2019

@author: karlchen
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
os.chdir("/home/karlchen/Desktop/AdventOfCode/AoC19")



def asteroid_map_from_file(inputfile):
    with open(inputfile) as infile:
        lines = infile.readlines()
    lines = [l.strip() for l in lines]
    height = len(lines)
    width = len(lines[0])
    map_ = np.zeros((height,width))
    for y,line in enumerate(lines):
        for x,char in enumerate(line):
            if char == ".":
                 map_[y,x] = 0
            elif char == "#":
                 map_[y,x] = 1
            else:
                print("input error: must be '.' or '#'")
    return(map_)


inputfile = "Input_10_test.txt"
asteroid_map = asteroid_map_from_file(inputfile)
positions = np.transpose(np.nonzero(asteroid_map))

independent_per_pos = np.zeros(len(positions[0]))
for m,pos1 in enumerate(positions):
    #for each asteroid, create a list of vectors to other asteroids
    #sight_vectors = np.empty((len(positions),2))
    sight_vectors = [np.empty(2) for _ in range(len(positions))]
    #also how far they are away
    dists = np.empty(len(positions))
    for n,pos2 in enumerate(positions):
        sight_vectors[n] = np.transpose(pos1-pos2)
        dists[n] = np.linalg.norm(pos1-pos2)
    #sort sight vectors from closest to farthest asteroid, then kick self-reference
    distsort = np.argsort(dists)
    sight_vectors = [x for _, x in sorted(zip(dists,sight_vectors), key=lambda pair: pair[0])]
    sight_vectors = sight_vectors[1:]

    #now gather vectors and by doing so kill those which are multiples of the gathered vector
    sv_copy = copy.deepcopy(sight_vectors)
    for vector1 in sv_copy:
        #check wether vector is still available
        #if yes, go through all the other vectors and kick them if they are multiples
        if vector1 in sight_vectors:
            for vector2 in sv_copy:
                quot = vector1/vector2
                if quot[0] == quot[1] and quot[1]>0:
                    sight_vectors.remove(vector2)
    independent_per_pos[m] = len(sight_vectors)

            
    
    #n_independent = np.linalg.matrix_rank()
    
