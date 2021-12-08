#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:55:51 2020

@author: robinkoch
"""

import re
import numpy as np
class MathEquationEvaluator:
    
    def __init__(self, expression,ruleset):
        self.expression = [x if x in "()*+" else int(x)\
                           for x in re.findall("\d+|[\(\)\+\*]", expression)]
        self.ruleset = ruleset
        self.find_lbs()
        self.find_rbs()

    def find_lbs(self):
        self.lb_pos = [i for i,x in enumerate(self.expression) if x=="("]

    def find_rbs(self):
        self.rb_pos = [i for i,x in enumerate(self.expression) if x==")"]


    def calculate(self):
        print("start calculating")
        while self.rb_pos:
            self.update()
        self.result = self.evaluate_subexpression(self.expression)



    def update(self):
        for il, lb in enumerate(self.lb_pos):
            if il+1 < len(self.lb_pos):
                dist_to_next_lb = self.lb_pos[il+1]-lb
            else:
                dist_to_next_lb = np.inf
            next_rb = [rb for rb in self.rb_pos if rb > lb][0]
            if (next_rb-lb) < dist_to_next_lb:
                subexpression = self.expression[lb+1:next_rb]
                res = self.evaluate_subexpression(subexpression)
                self.expression = self.expression[:lb] + [res] + self.expression[next_rb+1:]
                self.find_lbs()
                self.find_rbs()
                break
    
    def evaluate_subexpression(self, subexpression):
        while len(subexpression)>3:
            if self.ruleset == 2:
                add_idxs = [i for i,x in enumerate(subexpression) if x=="+"]
                if add_idxs:
                    add_idx = add_idxs[0]
                    subexpression =  subexpression[:add_idx-1]\
                        + [self.evaluate_subexpression(subexpression[add_idx-1:add_idx+2])]\
                        + subexpression[add_idx+2:]
                else:
                    subexpression =  [self.evaluate_subexpression(subexpression[:-2])]\
                        + subexpression[-2:]
            else:
                subexpression =  [self.evaluate_subexpression(subexpression[:-2])]\
                    + subexpression[-2:]
        
        if subexpression[1] == "*":
            return subexpression[0] * subexpression[2]
        elif subexpression[1] == "+":
            return subexpression[0] + subexpression[2]

