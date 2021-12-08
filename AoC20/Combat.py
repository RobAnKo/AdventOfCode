#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 12:44:45 2020

@author: robinkoch
"""
import re
import numpy as np
class Combat:
    
    def __init__(self, cards):
        pix = [i for i,l in enumerate(cards) if l.startswith("Player")]
        self.Player_stacks = [[int(c) for c in cards[pix[0]:pix[1]] if re.match("\d+", c)],\
                              [int(c) for c in cards[pix[1]:] if re.match("\d+", c)]]
        
        
    def run(self):
        n_updates = 0
        while all(self.Player_stacks):
            vals = [x.pop(0) for x in self.Player_stacks]
            windex = np.argmax(vals)
            if windex:
                self.Player_stacks[windex].extend(reversed(vals))
            else:
                self.Player_stacks[windex].extend(vals)
            n_updates += 1
        self.Winner = windex
        self.n_updates = n_updates
    
    def evaluate(self):
        return sum(((i+1)*val for i,val in enumerate(reversed(self.Player_stacks[self.Winner]))))
        