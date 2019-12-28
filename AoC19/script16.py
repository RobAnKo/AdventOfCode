#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:51:36 2019

@author: robinkoch
"""
import numpy as np
def read_inputfile(inputfile):
    with open(inputfile) as f:
        line = f.readline().strip()
    return([int(x) for x in line])

    
    
def mutate_list(inp_list,patterns):
    out_list = [0] *len(inp_list)
    pos = 1
    for idx in range(0,len(inp_list)):
        pos_pattern = np.repeat(pattern, pos)
        #make pattern at least as long as input
        ratio = int(np.ceil(len(inp_list)/len(pos_pattern)))+1
        pos_pattern = list(pos_pattern) * ratio
        #offset by 1
        pos_pattern = pos_pattern[1:]
        #out = str(sum([i*p for i,p in zip(inp_list, pos_pattern)]))
        #out = sum([i*p for i,p in zip(inp_list, pos_pattern)])
        #out = str(out)
        #out = out.replace("-","")
        #out = int(out[0])
        out = int(str(sum([i*p for i,p in zip(inp_list, pos_pattern)]))[-1])
        out_list[idx] = out
        pos +=1
    return(out_list)


def create_patt_dict(pattern,n):
    patt_dict = {}
    for position in range(1,n+1):
        pos_pattern = np.repeat(pattern,position)
        #ratio = int(np.ceil(len(inp_list)/len(pos_pattern)))+1
        if len(pos_pattern)<=n+1:
            ratio = round(n/len(pos_pattern))+1
            pos_pattern = list(pos_pattern) * ratio
        else:
            pos_pattern = list(pos_pattern)
        patt_dict[position] = pos_pattern[1:n+1]
    return patt_dict


inputfile = "Input_16.txt"
#inputfile = "Input_16test.txt"

inp = read_inputfile(inputfile)*100
#inp = inp[:round(len(inp)/2)]
#inp = [1,2,3,4,5,6,7,8]
pattern = [0,1,0,-1]

patt_dict = create_patt_dict(pattern, len(inp))

                             

# for x in range(10):
    
#     inp = mutate_list(inp, pattern)

# print("".join([str(x) for x in inp[:8]]))


#try with a generator

def mutate_list(inp_list,pattern):
    out_list = [0] *len(inp_list)
    pos = 1
    for idx in range(0,len(inp_list)):
        out_list[idx] = new_val_at_pos(inp_list,pos)
        pos+=1
    return out_list


def new_val_at_pos(inp_list, pos):
    return(sum([i*m for i,m in zip(inp_list, multiply_generator(pos))]))


def multiply_generator(pos):
    internal_index = 0
    




inp = read_inputfile(inputfile)*10000
pattern = [0,1,0,-1]
for _ in range(100):
    inp_list = mutate_list(inp, pattern)