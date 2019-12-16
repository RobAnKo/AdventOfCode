#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 01:59:19 2019

@author: karlchen
"""

import os
import pandas as pd
import copy
from typing import List,Dict,Iterable
os.chdir("/home/karlchen/Desktop/AdventOfCode/AoC19")

class IntCoder:
    
    def __init__(self,memory: List[int]) -> None:
        self._memory = memory
        self._original_memory = copy.deepcopy(memory)
        self._pointer: int = 0
        self._relative_base: int = 0
        self._extended_memory: Dict[int:int] = {}
        self._opcodes = {1:self._add,
                         2:self._mul,
                         3:self._in,
                         4:self._return,
                         5:self._jump_if_true,
                         6:self._jump_if_false,
                         7:self._less_than,
                         8:self._equals,
                         9:self._change_base,
                         99:self._halt}
        self._done = False


    #basic access functions
    def _fetch(self) -> int:
        value = self._get(self._pointer)
        self._pointer += 1
        return(value)

    def _get(self, index):
        if index < len(self._memory):
            return self._memory[index]
        elif index not in self._extended_memory.keys():
            self._extended_memory[index] = 0
        return self._extended_memory[index]
    
    def _set(self,index,value):
        if index < len(self._memory):
            self._memory[index] = value
        else:
            self._extended_memory[index] = value

    def _val(self, mode):
        index = self._fetch()
        if mode == 0:
            return self._get(index)
        if mode == 1:
            return index
        if mode == 2:
            index = index + self._relative_base
            return self._get(index)
        raise ValueError(f"Unknown parameter mode {mode}")

    def _index(self, mode):
        index = self._fetch()
        if mode in [0,1]:
            return index
        elif mode == 2:
            return index + self._relative_base
        raise ValueError('Got mode {} for index only type param'.format(mode))

    #method implementing the process of fulfilling one instruction
    def _step(self) -> None:
        instruction = self._fetch()
        oc = instruction%100
        mode1: int = int(instruction/100)%10
        mode2: int = int(instruction/1000)%10
        mode3: int = int(instruction/10000)%10
        
        return(self._opcodes[oc](mode1,mode2,mode3))
        
            
    #the optcodes
    def _add(self, mode1,mode2,mode3):
        val1 = self._val(mode1)
        val2 = self._val(mode2)
        idx = self._index(mode3)
        self._set(idx, val1+val2)

    def _mul(self, mode1,mode2,mode3):
        val1 = self._val(mode1)
        val2 = self._val(mode2)
        idx = self._index(mode3)
        self._set(idx, val1*val2)

    def _in(self,mode1,mode2,mode3):
        idx = self._index(mode1)
        self._set(idx,self._input_value)
    
    def _return(self,mode1,mode2,mode3):
        return(self._val(mode1))
    
    def _jump_if_true(self,mode1,mode2,mode3):
        val1 = self._val(mode1)
        val2 = self._val(mode2)
        if val1:
            self._pointer = val2

    def _jump_if_false(self,mode1,mode2,mode3):
        val1 = self._val(mode1)
        val2 = self._val(mode2)
        if not val1:
            self._pointer = val2

    def _less_than(self,mode1,mode2,mode3):
        val1 = self._val(mode1)
        val2 = self._val(mode2)
        idx = self._index(mode3)
        if val1 < val2:
            self._set(idx, 1)
        else:
            self._set(idx, 0)

    def _equals(self,mode1,mode2,mode3):
        val1 = self._val(mode1)
        val2 = self._val(mode2)
        idx = self._index(mode3)
        if val1 == val2:
            self._set(idx, 1)
        else:
            self._set(idx, 0)
    
    def _change_base(self,mode1,mode2,mode3):
        val1 = self._val(mode1)
        self._relative_base += val1
        
    def _halt(self, mode1,mode2,mode3):
        self._done = True
        
    
    def _reset_memory(self):
        self._memory = copy.deepcopy(self._original_memory)
        self._extended_memory = {}
        self._done = False
        
    def _reset_pointer(self):
        self._pointer = 0
        self._relative_base = 0
        self._done = False
    
    #resetting the memory, pointer and base values
    def _reset_all(self):
        self._reset_memory()
        self._reset_pointer()
    
    
    
    #running the intcode until we halt
    def run(self,input_value = 0):
        self._input_value = input_value
        self._n_steps =0
        self._pointer_idxs = []
        self._pointer_values = []
        self._rel_bases = []
        outs = []
        while not self._done:
            self._pointer_idxs.append(self._pointer)
            self._pointer_values.append(self._memory[self._pointer])
            self._rel_bases.append(self._relative_base)
            potential_output = self._step()
            self._n_steps +=1
            if potential_output is not None:
                outs.append(potential_output)
        return(outs)
                
    
    def __repr__(self) -> str:
        return f"Code: {self._memory},\nPointer: {self._pointer}\nRelBase: {self._relative_base}"
       
    @staticmethod
    def read_from_file(inputfile):
        intcode_array = pd.read_csv(inputfile, header = None).values
        return intcode_array[0]
    
    @staticmethod
    def extend_memory(memory, size):
        ext_mem = [0]*size
        ext_mem[0:len(memory)] = memory
        return(ext_mem)


class IntCoderWithIo(IntCoder):
    def __init__(self, memory, input_values: Iterable[int]=[0]):
        super(IntCoderWithIo, self).__init__(memory)
        self._input_values = iter(input_values)
        self._output_values = []

    def run(self):
        for n in self._input_values:
            out = super(IntCoderWithIo, self).run(n)
            self._output_values.append(out)
            self._reset_all()
        return(self._output_values)




# inputfile = "Input_9.txt"
# #intcode = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# #intcode = [1102,34915192,34915192,7,4,7,99,0]
# #intcode = [104,1125899906842624,99]
# intcode = IntCoder.read_from_file(inputfile)
# intcode = IntCoder.extend_memory(intcode, 10**5)
# ICComputer = IntCoderWithIo(intcode, [2])
# out = ICComputer.run()

# # for p, v, r in zip(ICComputer._pointer_idxs,ICComputer._pointer_values, ICComputer._rel_bases):
# #     print(p,v,r)

