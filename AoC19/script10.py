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
import math
from typing import Tuple,Iterable,List
os.chdir("/home/karlchen/Desktop/AdventOfCode/AoC19")
#os.chdir("/home/robinkoch/Desktop/AdventOfCode/AoC19")



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



def remove_arr_from_list(arr,list_):
    idx = [all(arr == elem) for elem in list_]
    ix = np.argwhere(idx)
    list_.pop(int(ix[0]))
    return list_


def coincident(one, two):
  one_hat = one / np.linalg.norm(one)
  two_hat = two / np.linalg.norm(two)
  dotp = np.dot(one_hat,two_hat)
  if math.isclose(1,dotp,abs_tol=1e-09):
      return True
  return False



'''
inputfile = "Input_10_test2.txt"
asteroid_map = asteroid_map_from_file(inputfile)
positions = np.transpose(np.nonzero(asteroid_map))

#container for number of visible asteroids per position
visible_per_pos = np.zeros(len(positions))
#check each asteroid
for m,pos1 in enumerate(positions):
    print(f"checking position {m}")
    #create a list of vectors pointing to other asteroids
    sight_vectors = [np.empty(2) for _ in range(len(positions))]
    #also how far they are away
    dists = np.empty(len(positions))
    for n,pos2 in enumerate(positions):
        sight_vectors[n] = np.transpose(pos2-pos1)
        dists[n] = np.linalg.norm(pos2-pos1)

    #sort sight vectors from closest to farthest asteroid, then kick self-reference
    sight_vectors = [x for _, x in sorted(zip(dists,sight_vectors), key=lambda pair: pair[0])]
    sight_vectors = sight_vectors[1:]

    #now fix one vector at a time and check whether others are multiples of first vector
    # if yes, drop them
    ix = 0
    while ix<len(sight_vectors):
        #print(ix)
        vector1 = sight_vectors[ix]
        sv_copy = copy.deepcopy(sight_vectors)
        sv_copy = remove_arr_from_list(vector1,sv_copy)
        for vector2 in sv_copy:
            if coincident(vector1,vector2):
                sight_vectors = remove_arr_from_list(vector2,sight_vectors)
        ix += 1
    visible_per_pos[m] = len(sight_vectors)
maxval = max(visible_per_pos)
maxpos = positions[np.argmax(visible_per_pos)]
    
print(f"Solution for Puzzle10.1:\n Best is {maxpos} with {max(visible_per_pos)} asteroids detected")

'''
#puzzle10.2

#We know from 10.1 that the station is at [31,25]
# if we sort the direction vectors by polar coordinates (i.e. angle) we can
# find the next asteroid to evaporate

def cart_to_polar(vector: Iterable[int]) -> List[int]:
    x = vector[0]
    y = vector[1]
    z = x + 1j * y
    r = np.abs(z)#np.sqrt(x**2+y**2)
    t = np.angle(z,deg=True)#arctan2(y,x)
    if t<0:
        t += 360
    return([r,t])

def polar_to_cart(vector: Iterable[int]) -> List[int]:
    r = vector[0]
    t = np.radians(vector[1])
    x = r * np.cos(t)
    y = r * np.sin(t)
    return([x,y])

#def rotate(matrix):
#    return np.array([x for x in zip(*matrix[::-1])])


def find_new_laser_angle(angle_before,sight_vectors):
    #find index in list of objects which is closest clockwise to old laser angle
    l = [ast for ast in sight_vectors if ast[1]<angle_before]
    if not l:
        #we have no objects with angles smaller than angle before, so reset at 360
        l = [ast for ast in sight_vectors if ast[1]<360]
    return(l[0][1])

#def rotate_point(point,shape_of_map):
#    return((point[1],shape_of_map[1]-point[0]-1))

inputfile = "Input_10.txt"
asteroid_map = asteroid_map_from_file(inputfile)
laser_pos = (31,25)
asteroid_map[laser_pos] = 3


positions = list(np.transpose(np.nonzero(asteroid_map)))

laser_idx = [x for x,pos in enumerate(positions) if all(laser_pos==pos)]
positions.pop(laser_idx[0])

#calculate direction vectors in polar coordinates
sight_vectors = [cart_to_polar(pos-laser_pos) for pos in positions]

#sort vectors, positions by polar angle, reverse because we turn clockwise
sight_vectors = [x for x in sorted(sight_vectors, reverse=True, key=lambda pair: pair[1])]


#this is the lasers first shot
laser_angle = cart_to_polar([-1,0])[1]

#find asteroid closest to the laser having the same angle as initial_laser_angle
num_vaporized = 0
destroyed = list([0 for _ in range(len(sight_vectors))])
while sight_vectors:
    in_line = [ast_vector for ast_vector in sight_vectors if ast_vector[1] == laser_angle]
    destroyed[num_vaporized] =  in_line[-1]
    sight_vectors.remove(in_line[-1])
    num_vaporized += 1
    if sight_vectors:
        laser_angle = find_new_laser_angle(laser_angle,sight_vectors)

destroyed_directions_cart = [polar_to_cart(x) for x in destroyed]
destroyed_direction_cart = [[round(x) for x in direction] for direction in destroyed_directions_cart]
destroyed_pos = [[x+y for x,y in zip(laser_pos,direction)] for direction in destroyed_direction_cart]
dp200 = destroyed_pos[199]
sol = dp200[1]*100+dp200[0]
print(f"Solution for puzzle 10.2:\n Position ({dp200[1]},{dp200[0]})\nKey: {int(sol)}")
