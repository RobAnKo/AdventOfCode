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
#os.chdir("/home/karlchen/Desktop/AdventOfCode/AoC19")
os.chdir("/home/robinkoch/Desktop/AdventOfCode/AoC19")

from Intcoder import IntCoder


class PaintRobot(IntCoder):
    
    def __init__(self, memory,initial_input):
        super(PaintRobot,self).__init__(memory)
        self._painted_tiles = {}
        self._initial_position = (100,100)
        self._position = self._initial_position
        self._direction = (0,1) #up
        self._initial_in = initial_input
        
    def _get_tile_color(self):
        if self._position in self._painted_tiles.keys():
            return self._painted_tiles[self._position]
        else:
            if not self._initial_in is None:
                out = self._initial_in
                self._initial_in = None
            else:
                out = 0
            return out
            
    def _paint_and_move(self):
        t_col = self._get_tile_color()
        outs = self._get_output(t_col)
        #did we halt at any of the two output generations?
        if outs[0] != -1:
            self._painted_tiles[self._position] = outs[0]
        else:
            self._done = True
        if outs[1] != -1:
            self._rotate(outs[1])
            self._move()
        else:
            self._done = True
        
    def _rotate(self,inputval):
        left_rots = {(-1,0):(0,-1),(0,-1):(1,0),(1,0):(0,1),(0,1):(-1,0)}
        right_rots = {(1,0):(0,-1),(0,-1):(-1,0),(-1,0):(0,1),(0,1):(1,0)}
        if inputval == 0:
            self._direction = left_rots[self._direction]
        elif inputval == 1:
            self._direction = right_rots[self._direction]
        else:
            print("attention, not a valid direction input for rotation")
    
    def _move(self):
        self._position = tuple([x+y for x,y in zip(self._position,self._direction)])
    
    
    def _get_output(self,input_value = 0):
        self._input_value = input_value
        outputs = []
        while len(outputs)<2:
            out = self._step()
            if out is not None:
                outputs.append(out)
        return(outputs)
    
    def go(self):
        while not self._done:
            self._paint_and_move()
    
    def num_of_painted_tiles(self):
        return(len(self._painted_tiles))

    def create_painting(self):
        grid = np.zeros((201,201))
        for tile,color in self._painted_tiles.items():
            grid[tile] = color
        return grid
        
        
inputfile = "Input_11.txt"
intcode = PaintRobot.read_from_file(inputfile)
#intcode = [3,9,3,10,1,9,10,11,104,0,98]
initial_tile_color = 1
robby = PaintRobot(intcode, initial_tile_color)

robby.go()
painting = robby.create_painting()
sn.heatmap(painting)
print(f"Solution: {robby.num_of_painted_tiles()}")