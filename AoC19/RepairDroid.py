#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:12:04 2019

@author: robinkoch
"""

from Intcoder import IntCoder
import matplotlib.pyplot as plt
from random import choice
import numpy as np
import seaborn as sns
class RepairDroid(IntCoder):
    
    def __init__(self,memory):
        super(RepairDroid,self).__init__(memory)
        self._map = np.zeros((801,801))
        self._position = (400,400)
        self._figure = plt.figure()
        self._axes = plt.subplot(111)
        self._key_map = {}
        self._direction_dict = {1:(,0),2:(0,-1),3:(1,0),4:(0,1)}
        self._input_value = 1
        self._direction = self._direction_dict[self._input_value]
        self._nsteps = 0
    
    def _explore(self):
        while not np.count_nonzero(self._map == 2) and self._nsteps<100000:
            self._move()
            #self._show_map()
            self._nsteps+=1
    
    
    def _run(self):
        out = None
        while out is None:
            #self._pointer_idxs.append(self._pointer)
            #self._pointer_values.append(self._memory[self._pointer])
            #self._rel_bases.append(self._relative_base)
            out = self._step()
            #self._n_steps +=1
        return(out)
    
    def _move(self):
        output = self._run()
        #paint the map
        self._paint(output)
        self._walk_into_direction()
        
    def _walk_into_direction(self):
        new_position = tuple(p+d for p,d in zip(self._position,self._direction))
        if not self._map[new_position] == -1:
            self._position = new_position
        else:
            self._input_value =choice([1,2,3,4])
            print(self._input_value)
            self._direction = self._direction_dict[self._input_value]
        
        
    def _paint(self,output):
        if output == 0:
            self._map[[p+d for p,d in zip(self._position,self._direction)]]=-1
        elif output == 1:
            self._map[self._position] = 1
        elif output == 2:
            self._map[self._position] = 2
            
        
    
    def _show_map(self):
        self._axes.matshow(self._map)
    
    
inputfile = "Input_15.txt"
intcode = RepairDroid.read_from_file(inputfile)
RepDroid = RepairDroid(intcode)
RepDroid._explore()
