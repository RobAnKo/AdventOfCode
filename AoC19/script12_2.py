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
import math
import itertools
from functools import reduce


def lcm(a,b):
    return((a*b)//math.gcd(a,b))


class Body():
    
    def __init__(self,pos,vel):
        self.p = pos
        self.v = vel



def step(bodies):
    for m1, m2 in itertools.combinations(range(len(bodies)), 2):
        for i in range(len(bodies[0].p)):
            if bodies[m1].p[i]<bodies[m2].p[i]:
                bodies[m1].v[i] += 1
                bodies[m2].v[i] -= 1
            elif bodies[m1].p[i]>bodies[m2].p[i]:
                bodies[m1].v[i] -= 1
                bodies[m2].v[i] += 1

    for b in bodies:
        for i in range(len(bodies[0].p)):
            b.p[i] += b.v[i]


#solution 1
            
inputfile = "Input_12.txt"
moons = []
for l in open(inputfile):
    pos = [int(x[2:]) for x in l.strip('<>\n').split(', ')]
    vel = [0, 0, 0]
    moons.append(Body(pos,vel))

n = 1000
nn = 0
while nn<n:
    step(moons)
    nn+=1
total=0
for m in moons:
    pot, kin = sum([abs(x) for x in m.p]), sum([abs(x) for x in m.v])
    total += pot * kin
print(f"Solution 12.1: {total}")

#solution 2


inputfile = "Input_12.txt"
moons = []
for l in open(inputfile):
    pos = [int(x[2:]) for x in l.strip('<>\n').split(', ')]
    vel = [0, 0, 0]
    moons.append(Body(pos,vel))


#keep track of steps
steps = 0

'''
We will capture the orbital periods (https://en.wikipedia.org/wiki/Orbital_period) for each axis here:
{
  0: step at which all 4 moons are at their starting x-position and x-velocity
  1: step at which all 4 moons are at their starting y-position and y-velocity
  2: step at which all 4 moons are at their starting z-position and z-velocity
}
'''
period =  dict()

'''
Save starting values grouped by axis:
0: (position_x, velocity_x) * (4 moons)
1: (position_y, velocity_y) * (4 moons)
2: (position_z, velocity_z) * (4 moons)
'''
start = [[(m.p[axis], m.v[axis]) for m in moons] for axis in range(3)]

while len(period) < 3:
    steps += 1
    print(steps)
    step(moons)
    
    #See if current (pos_axis, vel_axis) for all moons match their starting values:
    for axis in range(3):
        if axis not in period and start[axis] == [(m.p[axis], m.v[axis]) for m in moons]:
            period[axis] = steps

print('After', steps, 'steps:')
print('ans:', reduce(lcm, period.values()))
