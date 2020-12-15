#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 08:51:21 2020

@author: karlchen
"""

class MemoryGame:
    
    def __init__(self, start_numbers):
        self.start_numbers = start_numbers
        self.n_start_numbers = len(start_numbers)
        self.number_dict = dict()
        self.multiple_mention = dict()
        self.round_dict = dict()
        self.last_spoken = None
    
    
    def run(self):
        for n in range(2020):
            if n < self.n_start_numbers:
                number = self.start_numbers[n]
                self.round_dict[n] = number
                self.multiple_mention[number] = False
                self.number_dict[number] = n
                self.last_spoken = number
            else:
                if self.multiple_mention[self.last_spoken]:
                    number = n - self.number_dict[self.last_spoken]
                else:
                    number = 0
                self.round_dict[n] = number
                if number in self.number_dict:
                    self.multiple_mention[number] = True
                self.number_dict[number] = n
                self.last_spoken = number
