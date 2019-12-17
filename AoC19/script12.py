#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 01:59:19 2019

@author: karlchen
"""

import os
import pandas as pd
import numpy as np
import copy
from typing import List,Dict,Iterable
import re
import itertools as itt
import matplotlib.pyplot as plt

class MoonSystem():
    
    def __init__(self,input_positions: Iterable[Iterable]):
        self._positions = input_positions
        self._gravities = [[0]*len(input_positions[0])]*len(input_positions)
        self._velocities = [[0]*len(input_positions[0])]*len(input_positions)


#one step consists of gravitation calculation, velocity update and movement
    def _step(self):
        idxs = [x for x in range(len(self._positions))]
        #all pairs of moons
        combs = itt.combinations(idxs,2)
        for comb in combs:
            idx1 = comb[0]
            idx2 = comb[1]
            #calculate gravitations between two moons
            grav1,grav2 = self._grav_from_pos(self._positions[idx1],self._positions[idx2])
            #update existing gravity
            self._gravities[idx1] = [x+y for x,y in zip(self._gravities[idx1], grav1)]
            self._gravities[idx2] = [x+y for x,y in zip(self._gravities[idx2], grav2)]
        self._apply_forces()
        self._apply_velocities()
        
    def _apply_forces(self):
        for ix,vel, grav in zip(range(len(self._velocities)),self._velocities,self._gravities):
            self._velocities[ix] = [x+y for x,y in zip(vel,grav)]
        #reset gravity for next step
        self._gravities = [[0]*len(grav)]*len(self._gravities)
                            
    def _apply_velocities(self):
        for ix,pos, vel in zip(range(len(self._positions)),self._positions,self._velocities):
            self._positions[ix] = [x+y for x,y in zip(pos,vel)]
        
    def _grav_from_pos(self,pos1: Iterable[float],pos2: Iterable[float]) -> (Iterable[float],Iterable[float]):
        grav1 = [0]*len(pos1)
        for idx,p1,p2 in zip(range(len(pos1)),pos1,pos2):
            if p1>p2:
                grav1[idx] = -1
            elif p1<p2:
                grav1[idx] = 1
            elif p1==p2:
                grav1[idx] = 0
        grav2 = [x*(-1) for x in grav1]
        
        return grav1,grav2 
    
    
    def calc_energy(self):
        etot = 0
        for pos,vel in zip(self._positions,self._velocities):
            epot = sum([abs(x) for x in pos])
            ekin = sum([abs(x) for x in vel])
            etot += epot*ekin
        return(etot)
        
    def __repr__(self):
        return f"Positions:{self._positions},\nVelocities = {self._velocities}"
    
    @staticmethod
    def read_from_file(inputfile):
        with open(inputfile) as f:
            lines = f.readlines()
        positions = [[int(x) for x in re.findall(r"[\-\d]+", line)] for line in lines]
        return(positions)
        



inputfile = "Input_12.txt"
content = MoonSystem.read_from_file(inputfile)
print(content)
MS = MoonSystem(content)
nstep = 0
energies = []
while nstep<100000:
    energies.append(MS.calc_energy())
    MS._step()
    nstep+=1
plt.plot(energies)

print(f"Solution for puzzle 12.1: {energies[99]}")
