#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 17:11:04 2021

@author: robinkoch
"""
import numpy as np

class FuelOptimizer():
    def __init__(self, inputfile):
        with open(inputfile, "r") as f:
            self.initial_positions = [int(x) for x  in f.read().strip().split(",")]
            
    
    
    def calculate_fuel_at_position(self, pos):
        distances = [abs(p - pos) for p in self.initial_positions]
        return sum([sum(range(d+1)) for d in distances])
    
    
    def find_min_fuel(self):
        self.fuels = [self.calculate_fuel_at_position(pos) 
                      for pos in range(min(self.initial_positions), max(self.initial_positions))]
        
        self.best_position = np.argmin(self.fuels)
        self.min_fuel = min(self.fuels)
        return self.min_fuel