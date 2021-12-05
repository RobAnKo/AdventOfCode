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
    
    
    def run(self,end_time):
        for n in range(end_time):
            if n < self.n_start_numbers:
                number = self.start_numbers[n]
                self.round_dict[n] = number
                self.multiple_mention[number] = False
                self.number_dict[number] = [n]
                self.last_spoken = number
            else:
                if self.multiple_mention[self.last_spoken]:
                    number = self.number_dict[self.last_spoken][-1] - self.number_dict[self.last_spoken][-2]
                else:
                    number = 0
                self.round_dict[n] = number
                if number in self.number_dict:
                    self.multiple_mention[number] = True
                    self.number_dict[number].append(n)
                else:
                    self.number_dict[number] = [n]
                    self.multiple_mention[number] = False
                self.last_spoken = number



class MemoryGameEfficient:
    
    def __init__(self, start_numbers):
        self.start_numbers = start_numbers
        self.n_start_numbers = len(start_numbers)
        self.number_dict_last = dict()
        self.number_dict_second_to_last = dict()
        self.round_dict = dict()
        self.last_spoken = None
    
    
    def run(self,end_time):
        for n in range(end_time):
            if n < self.n_start_numbers:
                number = self.start_numbers[n]
                self.round_dict[n] = number
            else:
                if self.last_spoken in self.number_dict_second_to_last:
                    number = self.number_dict_last[self.last_spoken] - self.number_dict_second_to_last[self.last_spoken]
                else:
                    number = 0
            if number in self.number_dict_last:
                    self.number_dict_second_to_last[number] = self.number_dict_last[number]
            self.number_dict_last[number] = n
            self.round_dict[n] = number
            self.last_spoken = number



class MemoryGameBare:

    def __init__(self, start_numbers):
        self.n_start_numbers = len(start_numbers)
        self.number_dict_last = dict(zip(start_numbers, range(len(start_numbers))))
        self.number_dict_second_to_last = dict()
        self.last_spoken = start_numbers[-1]


    def run(self,end_time):
        for n in range(self.n_start_numbers, end_time):
            if self.last_spoken in self.number_dict_second_to_last:
                number = self.number_dict_last[self.last_spoken] - self.number_dict_second_to_last[self.last_spoken]
            else:
                number = 0
            if number in self.number_dict_last:
                self.number_dict_second_to_last[number] = self.number_dict_last[number]
            self.number_dict_last[number] = n
            self.last_spoken = number