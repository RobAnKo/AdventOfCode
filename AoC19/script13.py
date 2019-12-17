#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:25:54 2019

@author: karlchen
"""


import os
import numpy as np
import seaborn as sn
#os.chdir("/home/karlchen/Desktop/AdventOfCode/AoC19")
os.chdir("/home/robinkoch/Desktop/AdventOfCode/AoC19")

from Intcoder import IntCoder


class GameDrawer(IntCoder):
    
    def __init__(self, memory):
        super(GameDrawer,self).__init__(memory)
        self._grid = np.zeros((24,42))
        self._outputs = []
        self._joystick_position = 0
        
    def build_game(self):
        outs = self._get_outputs()
        while len(outs)==3:
            x_idx = outs[0]
            y_idx = outs[1]
            obj = outs[2]
            self._grid[y_idx,x_idx] = obj
            outs = self._get_outputs()
    
        
    def _get_outputs(self):
        outputs = []
        while not self._done and len(outputs)<3:
            out = self._step()
            if not out is None:
                outputs.append(out)
        return outputs
    
    def _get_ball_idx(self):
        return [int(x) for x in np.nonzero(self._grid == 4)]
    
    def play(self):
        self._memory[0] = 2
        self._ball_pos = self._get_ball_idx() 
        

        
    
#puzzle13.1
inputfile = "Input_13.txt"
intcode = GameDrawer.read_from_file(inputfile)
#intcode = [3,9,3,10,1,9,10,11,104,0,98]
drawer = GameDrawer(intcode)

drawer.build_game()
sol = np.nonzero(drawer._grid == 4)

#puzzle13.2
drawer._done = False
drawer.play()





