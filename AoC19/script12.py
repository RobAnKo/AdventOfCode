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
        self._gravities = [np.zeros(len(input_positions[0]),dtype= int) for _ in range(len(input_positions))]
        self._velocities = [np.zeros(len(input_positions[0]),dtype= int) for _ in range(len(input_positions))]
        self._indices =  [x for x in range(len(self._positions))]
    
    def _step(self):
        #all pairs of moons
        for comb in itt.combinations(self._indices,2):
            #calculate gravitations between two moons
            grav = np.sign(self._positions[comb[1]]-self._positions[comb[0]])
            #update velocity
            self._velocities[comb[0]] += grav
            self._velocities[comb[1]] -= grav
        for ix in self._indices:#range(len(self._positions)):
            self._positions[ix] += self._velocities[ix]

        
    
    def calc_energy(self):
        etot = 0
        for pos,vel in zip(self._positions,self._velocities):
            epot = np.sum(np.abs(pos))
            ekin = np.sum(np.abs(pos))
            etot += epot*ekin
        return(etot)
        
    def __repr__(self):
        return f"Positions:{self._positions},\nVelocities = {self._velocities}"
    
    @staticmethod
    def read_from_file(inputfile):
        with open(inputfile) as f:
            lines = f.readlines()
        positions = [np.array([int(x) for x in re.findall(r"[\-\d]+", line)]) for line in lines]
        return(positions)
        



inputfile = "Input_12.txt"
content = MoonSystem.read_from_file(inputfile)
print(content)
MS = MoonSystem(content)
nstep = 0
maxstep = 500000
energies = [0] *maxstep
while nstep<maxstep:
#    energies[nstep] = MS.calc_energy()
    MS._step()
    nstep+=1
#plt.plot(energies)

print(f"Solution for puzzle 12.1: {energies[99]}")


##puzzle 12.2

