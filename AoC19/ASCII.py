#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 12:05:02 2019

@author: robinkoch
"""

from Intcoder import IntCoder
import numpy as np

class ASCII_writer(IntCoder):
    
    def __init__(self, memory):
        super(ASCII_writer,self).__init__(memory)
        
    
    def run(self):
        outs = super(ASCII_writer, self).run()
        ascii_dic = {46:0,35:1, 94:2,-1:-1}
        line = []
        lines =[]
        for i in outs:
            #print(i)
            if i != 10:
                line.append(ascii_dic[i])
            else:
                if line:
                    lines.append(line)
                    line = []
        return np.array(lines)
                
        
inputfile = "Input_17.txt"
intcode = IntCoder.read_from_file(inputfile)
writer = ASCII_writer(intcode)
coder = IntCoder(intcode)
outs_raw = coder.run()
outs = writer.run()
import matplotlib.pyplot as plt
plt.matshow(outs)

total_sum=0
for y in range(1,outs.shape[0]-1):
    for x in range(1,outs.shape[1]-1):
        if outs[y,x] == 1:
            if outs[y,x+1] == 1:
                if outs[y,x-1] == 1:
                    if outs[y+1,x] == 1:
                        if outs[y-1,x] == 1:
                            total_sum += x*y
