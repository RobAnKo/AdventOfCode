#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 17:03:03 2021

@author: robinkoch
"""

import numpy as np
import copy
class Lanternfish_brute():
    def __init__(self,inputfile):
        with open(inputfile, "r") as f:
            self.initial_fish = np.array([int(n) for n in f.readline().rstrip().split(",")])
            self.n_fish = len(self.initial_fish)
            self.n_fish_over_time = []
            
    def run(self,n):
        self.fish = copy.deepcopy(self.initial_fish)
        for i in range(n):
            ripe = self.fish == 0
            n_ripe = sum(ripe)
            self.fish[ripe] = 7
            self.fish -=1
            self.fish = np.concatenate((self.fish, np.ones(n_ripe, dtype = "int")*8), axis = 0)
            # print("Fish")
            # print(self.fish)
            # print("Initial fish")
            # print(self.initial_fish)
            self.n_fish_over_time.append(len(self.fish))
        
        self.n_fish = self.n_fish_over_time[-1]
            
            
            
            
class Lanternfish_smart():
    def __init__(self,inputfile):
        with open(inputfile, "r") as f:
            self.initial_fish = np.array([int(n) for n in f.readline().rstrip().split(",")])
            self.ages = range(9)
            age_count = [sum(self.initial_fish==age) for age in self.ages]
            self.age_dict = dict(zip(self.ages,age_count))
            
            former_age = [[1],[2],[3],[4],[5],[6],[0,7],[8],[0]]
            self.age_mapping =dict(zip(self.ages, former_age))
            
            self.n_fish_over_time = []
            self.intermediate_dict = {}
            
    def run(self,n):
        self.n_fish_over_time.append(sum(self.age_dict.values()))
        for i in range(n):
            for age in self.ages:
                self.intermediate_dict[age] = sum([self.age_dict[former] for former in self.age_mapping[age]])
            self.age_dict = copy.deepcopy(self.intermediate_dict)
            self.n_fish_over_time.append(sum(self.age_dict.values()))
            
        self.n_fish = self.n_fish_over_time[-1]

