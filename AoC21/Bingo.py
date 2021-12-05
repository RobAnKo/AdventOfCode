#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:01:56 2021

@author: karlchen
"""
import numpy as np
import re

class Bingo():
    def __init__(self,inputfile):
        self.inputfile = inputfile
        self.n_fields = None
        self.numbers = None
        self.fields = None
        self.markers = None
        self.win = None
        self.last_hits = None
        self.number_just_called = None
        
    def initiate(self):
        self.numbers, self.fields = self.read_bingo(self.inputfile)
        self.n_numbers = len(self.numbers)
        self.n_fields = len(self.fields)
        self.markers = {k:np.zeros_like(v, dtype = np.bool) for k,v in self.fields.items()}
        self.win = {k:False for k in self.fields.keys()}
        
    def read_bingo(self, inputfile):
        fields = dict()
        with open(inputfile, "r") as f:
            lines = f.read()
        sp = lines.split("\n")
        numbers = sp.pop(0)
        numbers = [int(x) for x in numbers.split(",")]
        k_field = 0
        for i,line in enumerate(sp):
            if not line:
                if i<(len(sp)-1):
                    k_field+=1
                    fields[k_field] = np.zeros([5,5,])
                    k_line = 0
                else:
                    return numbers, fields
            else:
                fields[k_field][k_line] = [int(x) for x in re.findall("\d+",line)]
                k_line += 1
        
            
        
    def _get_hit_idxs_(self,number):
        self.last_hits = {idx:field==number for idx,field in self.fields.items()}
    
    def _mark_hits_(self):
        for idx,hits in self.last_hits.items():
            self.markers[idx][hits] = True
            
    def _check_win_(self):
        for idx,marker in self.markers.items():
            if np.any(np.all(marker, axis=0)) or np.any(np.all(marker, axis=1)):
                self.win[idx] = True
            else:
                pass
    
    def report_win_result(self):
        win_idx = [idx for idx,win in self.win.items() if win][0]
        s = np.sum(self.fields[win_idx][~self.markers[win_idx]])
        self.res = int(s*self.number_just_called)
        print(f"The result is {self.res}")
        
    def report_last_result(self):
        s = np.sum(self.fields[self.last_candidate][~self.markers[self.last_candidate]])
        self.res = int(s*self.number_just_called)
        print(f"The result is {self.res}")
        
        
    def run(self, typ):
        if typ == "first":
            for n in self.numbers:
                self.number_just_called = n
                #print(n)
                self._get_hit_idxs_(n)
                self._mark_hits_()
                self._check_win_()
                if any(self.win.values()):
                    break
            self.report_win_result()
        elif typ == "last":
            for n in self.numbers:
                if sum(self.win.values()) == self.n_fields-1:
                    self.last_candidate = [k for k,v in self.win.items() if not v][0]
                self.number_just_called = n
                #print(n)
                self._get_hit_idxs_(n)
                self._mark_hits_()
                self._check_win_()
                if all(self.win.values()):
                    break
            self.report_last_result()
            
    
    
            
        