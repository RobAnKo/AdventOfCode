#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:50:43 2020

@author: robinkoch
"""
import numpy as np
import re
import itertools
class BitmaskSystem:
    
    def __init__(self,instructions,mask_size):
        self.instructions = instructions
        self.mask_size = mask_size
        self.memory = dict()
        self.mask_idxs = [idx for idx,l in enumerate(self.instructions) if l.startswith("mask")]
        self.masks = [l.split(" = ")[1] for l in self.instructions if l.startswith("mask")]
       
        #store values in dictionary with mask as key
        self.mask_value_dict = dict()
        for m,mi,mi_next in zip(self.masks, self.mask_idxs,self.mask_idxs[1:]+[None]):
            vs = [self.pad_string(np.base_repr(number = int(instr.split(" = ")[1]),\
                                            base = 2,\
                                            padding = 0),\
                               self.mask_size)\
                  for instr in self.instructions[mi+1:mi_next]]
            self.mask_value_dict[m] = vs
        
        #store indices in dictionary with mask as key
        self.mask_address_dict = dict()
        for m,mi,mi_next in zip(self.masks, self.mask_idxs,self.mask_idxs[1:]+[None]):
            addresses = [self.pad_string(np.base_repr(number = int(re.search("(\d+)", instr).group()),\
                                                      base = 2,\
                                                      padding = 0),\
                                         self.mask_size)\
                         for instr in self.instructions[mi+1:mi_next]]
            self.mask_address_dict[m] = addresses

    def pad_string(self, string, length):
        return "".join(["0"] *(length-len(string))) + string

    def run1(self):
        for m, values in self.mask_value_dict.items():
            addresses = self.mask_address_dict[m]
            translated_masked_values = (int(self.apply_mask_to_write_value(v,m),2) for v in values)    
            for address,v in zip(addresses,translated_masked_values):
                self.memory[address] = v

    def run2(self):
        for m, addresses in self.mask_address_dict.items():
            values = self.mask_value_dict[m]
            translated_values = (int(v,2) for v in values)
            masked_addresses = [self.apply_mask_to_address(a,m) for a in addresses]
            expanded_addresses = (self.expand_address(address) for address in masked_addresses)
            
            for addresses,value in zip(expanded_addresses,translated_values):
                for address in addresses:
                    self.memory[address] = value

    def apply_mask_to_write_value(self,val, mask):
        val_l = list(val)
        for i,mask_v in enumerate(mask):
            if mask_v in "10":
                val_l[i] = mask_v
        return "".join(val_l)
    
    def apply_mask_to_address(self, address,mask):
        address_l = list(address)
        for i, mask_v in enumerate(mask):
            if mask_v in "1X":
                address_l[i] = mask_v
        return address_l
    
    
    def expand_address(self,address):
        address = np.array(address)
        float_idxs = [i for i,a in enumerate(address) if a=="X"]
        possibilities = itertools.product(*[[0,1]]*len(float_idxs))
        expanded_addresses = [None]*(2**len(float_idxs))
        for i,p in enumerate(possibilities):
            address[float_idxs] = p
            expanded_addresses[i] = "".join(address)
        return expanded_addresses

    def memory_sum(self):
        return sum(self.memory.values())
    
    def memory_reset(self):
        self.memory = dict()



'''
# puzzle 14.2

def apply_instructions_address_values(mask_instructions, mask_size):
    mem = dict()
    mask_idxs = [idx for idx,l in enumerate(mask_instructions) if l.startswith("mask")]
    
    for mi, next_mi in zip(mask_idxs, mask_idxs[1:] + [None]):
        mask = mask_instructions[mi].split(" = ")[1]
        write_values = [int(instr.split(" = ")[-1])    for instr in mask_instructions[mi+1:next_mi]]
        idxs_unpadded = [np.base_repr(number = int(re.search("(\d+)", instr).group()),\
                                      base = 2,\
                                      padding = 0)\
                         for instr in mask_instructions[mi+1:next_mi]]
        idxs_padded = [pad_str(idx,mask_size) for idx in idxs_unpadded]
        idxs_translated = [apply_mask_to_address(address,mask) for address in idxs_padded]
        for idxs,v in zip(idxs_translated,write_values):
            for i in idxs:
                mem[i] = v

    return sum(mem.values())

def apply_mask_to_address(address, mask):
    address_l = list(address)
    for i,mask_v in enumerate(mask):
        if mask_v in "1X":
            address_l[i] = mask_v
    return expand_masked_address(address_l)

def expand_masked_address(address_list):
    float_idxs = [i for i,a in enumerate(address_list) if a=="X"]
    address_list = [None]*(2**len(float_idxs))
    
    return address_list
'''