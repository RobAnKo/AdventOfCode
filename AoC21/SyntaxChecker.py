#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 15:12:26 2021

@author: karlchen
"""
from collections import Counter
class SyntaxChecker():
    def __init__(self,line):
        self.line = line
        
        self.valid_openings = '([{<'
        self.valid_closings = ')]}>'
        
        self.points_per_error = dict(zip(self.valid_closings, [3,57,1197,25137]))
        
        self.is_complete = self.check_if_complete()
        #self.is_corrupt = self.check_if_corrupt
        
        
    def check_if_complete(self):
        char_count = Counter(self.line)
        res = True
        for o,c in zip(self.valid_openings, self.valid_closings):
            print(f"Opening: {o}, closing: {c}")
            print(f"counts: {char_count[o]}, {char_count[c]}")
            if char_count[o] != char_count[c]:
                res = False
                break
        return res
        
        
        