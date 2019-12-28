#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:51:36 2019

@author: robinkoch
"""
from Intcoder import IntCoder
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

class TractorBeam(IntCoder):

    #adjust the method writing input into the intcode
    def _in(self,mode1,mode2,mode3):
        idx = self._index(mode1)
        if self._first:
            self._set(idx,self._input_values[0])
            self._first = False
        else:
            self._set(idx,self._input_values[1])
        
        
    def run(self,input_values = (0,0)):
        self._first = True
        self._input_values = input_values
        while not self._done:
            potential_output = self._step()
            if potential_output is not None:
                return(potential_output)

inputfile = "Input_19.txt"
intcode = TractorBeam.read_from_file(inputfile)
TB = TractorBeam(intcode)
ship = np.ones((100,100))
shipmask1 = np.zeros((99,199))
shipmask2 = np.zeros((100,99))
shipmask = np.concatenate((shipmask1, np.concatenate((shipmask2, ship),axis=1)))
shipmask= np.array(shipmask,dtype = "int")



n = 0
outmat = np.zeros((2000,2000))
#the width of the beam in the former yslice
beam_width = 0
#the x-position of the beam start in the former yslice
beam_start = 0
#the value calculated in the position before, initially 1
former_val = 1
for y in range(2000):
    if y == 8:
        print("weird")
    calculating = True
    beam_width_estimate = beam_width - 2
    print(y, beam_start)
    outstrip = outmat[y]
    for x in range(beam_start,2000):
        #print(x)
        #we use the actual intcode to calculate beam/notbeam at the borders
        if calculating:
            outval = TB.run((x,y))
            outstrip[x] = outval
            TB._reset_all()
            if outval != former_val:#boundary between beam/notbeam
                calculating = False
            former_val = outval
        else: #we use the heuristic that the beam is stretching towards right bottom
            if former_val == 0: #beam to notbeam -> fill up until the end with zeros => do nothing for the rest of the line
                former_val = 0
                break
            else:#notbeam to beam
                #beam_start = max([x-1,0])
                if beam_width_estimate > 1: 
                    outstrip[x] = 1
                    beam_width_estimate -= 1
                else:
                    calculating = True
                    outval = TB.run((x,y))
                    outstrip[x] = outval
                    TB._reset_all()
                    if outval != former_val:#boundary between beam/notbeam
                        calculating = False
                    former_val = outval
    beam_idxs = np.argwhere(outstrip)
    if any(beam_idxs):
        beam_start = int(beam_idxs[0])-1
    else:
        beam_start = 0
    beam_width = np.sum(outstrip)


#plt.matshow(outmat)
outmat = np.array(outmat, dtype="int")
#mask = signal.convolve2d(outmat,shipmask)

#outmat[(np.sum(outmat,axis=1)<100),:] = 0
#outmat[:,(np.sum(outmat,axis=0)<100)] = 0
# plt.matshow(mask)


hotspots = np.zeros(outmat.shape)
for y in range(outmat.shape[0]):
    for x in range(outmat.shape[1]):
        if outmat[y,x]:
            if outmat[y+99,x]:
                if outmat[y,x+99]:
                    if outmat[y+99,x+99]:
                        hotspots[y,x]=1




max_idxs = np.argmax(mask)
#diffy = outmat_rep-outmat
np.save("beam2000x2000_heur",outmat)