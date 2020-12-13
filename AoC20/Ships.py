#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:59:57 2020

@author: robinkoch
"""
import re
import numpy as np

class Ship:
    
    def __init__(self, instructions,start_position):
        self.instructions = instructions
        self.start_position = np.array(start_position)
        self.position = self.start_position
        self.instr_pointer = 0
        self.n_instructions = len(instructions)
        self.log = np.empty((self.n_instructions+1,2))
        self.log[0] = self.position
        self.facing =np.array([1,0])
        self.direction = np.array([0,0])
        
    
    def run(self):
        for i in range(self.n_instructions):
            self.instruction = self.instructions[i]
            print("position before move: " +str([int(x) for x in np.array(self.position)]));
            self.calculate_direction()
            self.move()
            self.log[i+1] = self.position
            print("position after move: "+str([int(x) for x in np.array(self.position)]));


    def calculate_direction(self):
        print("Instruction: "+self.instruction)
        sp = re.match("([A-Z])(\d+)", self.instruction).groups()
        op = sp[0]
        val = int(sp[1])
        if op == "N":
            self.direction = np.array([0,1])*val
        elif op == "S":
            self.direction = np.array([0,-1])*val
        elif op == "E":
            self.direction = np.array([1,0])*val
        elif op == "W":
            self.direction = np.array([-1,0])*val
        elif op == "F":
            self.direction = np.array(self.facing)*val
        elif op == "R":
            self.rotate_by_degree(-val)
            self.direction = np.array([0,0])
        elif op == "L":
            self.rotate_by_degree(val)
            self.direction = np.array([0,0])
        else:
            print("Attention, this is an invalid option!")
        print("The new move is: "+ str(self.direction))


    def manhattan_dist_from_initial_position(self):
        return(sum(np.abs(self.position-self.start_position)))


    def rotate_by_degree(self, alpha):
        x = int(self.facing[0])
        y = int(self.facing[1])
        self.facing = [round(np.cos(np.deg2rad(alpha))*x - np.sin(np.deg2rad(alpha))*y),\
                       round(np.sin(np.deg2rad(alpha))*x + np.cos(np.deg2rad(alpha))*y)]

    def move(self):
        self.position = [x+y for x,y in zip(self.position, self.direction)]



class Ship2(Ship):
    
    def __init__(self, instructions, start_position, waypoint_direction):
        super(Ship2, self).__init__(instructions, start_position)
        self.facing = np.array(waypoint_direction)

    #overwrite method to calculate the direction
    def calculate_direction(self):
        print("Instruction: "+self.instruction)
        sp = re.match("([A-Z])(\d+)", self.instruction).groups()
        op = sp[0]
        val = int(sp[1])
        if op in "NSWE":
            if op == "N":
                self.facing[1] += val
            elif op == "S":
                self.facing[1] -= val
            elif op == "E":
                self.facing[0] += val
            elif op == "W":
                self.facing[0] -= val
            self.direction = np.array([0,0])
        elif op == "R":
            self.rotate_by_degree(-val)
            self.direction = np.array([0,0])
        elif op == "L":
            self.rotate_by_degree(val)
            self.direction = np.array([0,0])
        elif op == "F":
            self.direction = np.array(self.facing)*val
        else:
            print("Attention, this is an invalid option!")
        print("The new move is: "+ str(self.direction))
