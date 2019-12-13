#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 17:47:27 2019

@author: robinkoch
"""

import os
import numpy as np
from array import array
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sn
import re
from sortedcontainers import SortedSet
import scipy
from scipy import signal
from datetime import datetime
import copy
os.chdir("/home/karlchen/Desktop/AdventOfCode/AoC19")


def array_from_csv(inputfile):
    return pd.read_csv(inputfile, header = None).values

'''
#puzzle1.1

def calculate_fuel_from_mass(mass):
    return sum(np.floor(mass/3)-2)

inputfile = "Input_1.txt"

masses = array_from_csv(inputfile)
fuel = calculate_fuel_from_mass(masses)
print("Solution 1.1:", fuel)


#puzzle1.2

def calculate_fuel_from_mass_recursive(mass):
    f = 0
    m = mass
    while m>0:
        req_f = max(0,np.floor(m/3)-2) #0 if negative
        #print(req_f)
        f+= req_f
        m = req_f
    return f


fuels = np.zeros(masses.shape)
calculate_fuel_from_mass_recursive(100756)
for i in range(len(masses)):
    m = masses[i]
    fuels[i] = calculate_fuel_from_mass_recursive(m)


print("Solution 1.2:", sum(fuels))

#puzzle2.1



inputfile = "Input_2.txt"

def read_intcode_from_csv(inputfile):
    intcode_array = array_from_csv(inputfile)
    return intcode_array[0]
    

def intcode_run(intcode):
    n = len(intcode)
    for ii in range(0,n,4):
        #print("oc_position",ii)
        optcode = intcode[ii]
        #print("optcode:", optcode)
        if optcode == 1:
            intcode = optcode_add(intcode,ii)
        elif optcode == 2:
            intcode == optcode_mult(intcode,ii)
        elif optcode == 99:
            return intcode
        else:
            print("oh shizzl")
            return None
        #print(intcode)

def optcode_add(intcode,pointer_idx):
    n1 = intcode[intcode[pointer_idx+1]]
    n2 = intcode[intcode[pointer_idx+2]]
    ix = intcode[pointer_idx+3]
    intcode[ix] = n1 + n2
    return(intcode)
    
def optcode_mult(intcode,pointer_idx):
    n1 = intcode[intcode[pointer_idx+1]]
    n2 = intcode[intcode[pointer_idx+2]]
    ix = intcode[pointer_idx+3]
    intcode[ix] = n1 * n2
    return(intcode)

intcode = read_intcode_from_csv(inputfile)

 
intcode[1] = 12
intcode[2] = 2

intcode = intcode_run(intcode)
#print(intcode)
print("Solution to puzzle 2.1:", intcode[0])
#testcode1 = [1,1,1,4,99,5,6,0,99]
#print(intcode_run(testcode1))

#puzzle 2.2

def test_inputs(inputfile):
    desired = 19690720
    for noun in range(100):
        print(noun)
        for verb in range(100):
            intcode = read_intcode_from_csv(inputfile)
            intcode[1]=noun
            intcode[2]=verb
            run_ic = intcode_run(intcode)
            res = run_ic[0]
            if res == desired:
                return(100*noun+verb)
            
            
print("Solution for puzzle 2.2:", test_inputs(inputfile))

#puzzle 3.1

def getwires(inputfile):
    with open(inputfile,"r") as f:
        l = list(f.readlines())
        w1 = l[0]
        wire1 = w1.strip().split(",")
        w2 = l[1]
        wire2 = w2.strip().split(",")
        return wire1,wire2


def wire_to_idx(wire):
    xpos = 0
    ypos = 0
    idx_set = []
    for walk in wire:
        direction = walk[0]
        length = int(walk[1:]) 
        steps = length+1
        
        if direction=="L":
            new_idx_set = [(i,ypos) for i in range(xpos-1,xpos-steps,-1)]
            xpos -= length
        elif direction=="R":
            new_idx_set = [(i,ypos) for i in range(xpos+1,xpos+steps,1)]
            xpos += length
        elif direction=="D":
            new_idx_set = [(xpos,i) for i in range(ypos-1,ypos-steps,-1)]
            ypos -= length
        elif direction=="U":
            new_idx_set = [(xpos,i) for i in range(ypos+1,ypos+steps,1)]
            ypos += length
        idx_set.extend(new_idx_set)
    return idx_set


inputfile = "Input_3.txt"
wire1,wire2 = getwires(inputfile)

#wire1 = ["R8","U5","L5","D3"]
#wire2 = ["U7","R6","D4","L4"]

#wire1=["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
#wire2=["U62","R66","U55","R34","D71","R55","D58","R83"]


#wire1=["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
#wire2=["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]


set1 = set(wire_to_idx(wire1))
set2 = set(wire_to_idx(wire2))
crossings = set1.intersection(set2)
distances = [sum(np.absolute(x)) for x in crossings]
print(distances)
print("Solution to puzzle 3.1:", min(distances))

#puzzle3.2

idx1 = wire_to_idx(wire1)
idx2 = wire_to_idx(wire2)
set1 = set(idx1)
set2 = set(idx2)
crossings = set1.intersection(set2)

distances = np.zeros(len(crossings))
cc=0
for c in crossings.__iter__():
    steps1 = idx1.index(c)+1
    steps2 = idx2.index(c)+1
    distances[cc] = steps1+steps2
    cc+=1

print("Solution to puzzle 3.2:", min(distances))


#puzzle4.1

inp_range = range(172930,683082)


possible_sols = 0



def test_double(num_as_list):
    for i in range(len(num_as_list)-1):
        if num_as_list[i]==num_as_list[i+1]:
            return True
    return False

def test_increase(num_as_list):
    for i in range(len(num_as_list)-1):
        if num_as_list[i]>num_as_list[i+1]:
            return False
    return True


for num in inp_range:
    n = list(str(num))
    if test_increase(n) & test_double(n):
        possible_sols+=1
        
print("Solution for puzzle 4.1:", possible_sols)
 
    

#puzzle4.2

def test_double_extended(num_as_list):
    num_as_list.append("$")
    for kk in range(len(num_as_list)-2):
        elem1 = num_as_list[kk]
        elem2 = num_as_list[kk+1]
        elem3 = num_as_list[kk+2]
        if elem1 == elem2 != elem3:
            if kk>0:
                elem0 = num_as_list[kk-1]
                if elem1 != elem0:
                    return True
            else:
                return True
    return False
    
    
test_double_extended(list(str(11222)))

    
possible_sols = 0
for num in inp_range:
    n = list(str(num))
    if test_increase(n) & test_double_extended(n):
        possible_sols+=1

print("Solution for puzzle 4.2:", possible_sols)

#puzzle 5.1

def read_intcode_from_csv(inputfile):
    intcode_array = array_from_csv(inputfile)
    return intcode_array[0]
    

def intcode_run(intcode):
    output_values = list()
    ii=0
    instruction = intcode[ii]
    optcode,pm1,pm2,pm3 = parameters_from_instruction(instruction)
    #print(instruction)
    print(intcode)
    print("OC:", optcode,"pm1:",pm1,"pm2",pm2,"pm3",pm3)
    while optcode != 99:
        intcode,step,possible_additional_output = optcode_run(intcode,optcode,ii,pm1,pm2,pm3)
        output_values.append(possible_additional_output)
        ii+=step
        instruction = intcode[ii]
        optcode,pm1,pm2,pm3 = parameters_from_instruction(instruction)
        #print(instruction)
        print(intcode)
        print("OC:", optcode,"pm1:",pm1,"pm2",pm2,"pm3",pm3)
    return intcode,output_values
        #print(intcode)


def parameters_from_instruction(instruction):
    opcode = instruction%100
    pm1 = ((instruction-opcode)%1000)
    pm2 = (instruction-opcode)%10000 -pm1
    pm3 = (instruction-opcode)%100000 -pm2 -pm1
    
    pm1 = int(round(pm1/100))
    pm2 = int(round(pm2/1000))
    pm3 = int(round(pm3/10000))
    
    return opcode,pm1,pm2,pm3
    
    


def optcode_run(intcode,oc,pointer_idx,pm1,pm2,pm3):
    
    #3-parametered optcodes
    if oc==1 or oc==2:
        
        step = 4
        
        if pm1 == 1:
            n1 = intcode[pointer_idx+1]
        else:
            n1 = intcode[intcode[pointer_idx+1]]
            
        if pm2 == 1:
            n2 = intcode[pointer_idx+2]
        else:
            n2 = intcode[intcode[pointer_idx+2]]
        
        ix = intcode[pointer_idx+3]
        
    #1-parametered optcodes
    elif oc==3 or oc==4:
        
        step = 2
        
        ix = intcode[pointer_idx+1]
        
    #invalid optcode    
    else:
        print("invalid optcode")
        return None
    
    
    if oc==1:
        intcode[ix] = n1 + n2
    elif oc==2:
        intcode[ix] = n1 * n2
    elif oc==3:
        intcode[ix] = 1
    elif oc==4:
        return intcode,step,intcode[ix]
    
    return intcode,step, None
    
       
    
    # if oc==1 or oc==2:
    #     step=4
    # elif oc==3 or oc==4:
    #     step=2
    # else:
    #     print("invalid optcode")
    #     return None
    
    
    # #check parameter mode: 1 takes the value x directly, 0 takes the value at position x
    # if pm1 == 1:
    #     n1 = intcode[pointer_idx+1]
    # else:
    #     n1 = intcode[intcode[pointer_idx+1]]
        
    # if pm2 == 1:
    #     n2 = intcode[pointer_idx+2]
    # else:
    #     n2 = intcode[intcode[pointer_idx+2]]
    
    # if pm3 == 1:
    #     print("AHA")
    # else:
    #     ix = intcode[pointer_idx+3]
    #     #ix = intcode[intcode[pointer_idx+3]]
    
    
    # if oc==1:
    #     intcode[ix] = n1 + n2
    # elif oc==2:
    #     intcode[ix] = n1 * n2
    # elif oc==3:
    #     intcode[n1] = 1
    # elif oc==4:
    #     return intcode,step,intcode[n1]
    
    # return intcode,step, None


inputfile = "Input_5.txt"
intcode = read_intcode_from_csv(inputfile)
#intcode = [1002,4,3,4,33]
intcode, output = intcode_run((intcode))


#puzzle 5.2

def optcode_run(intcode,oc,pointer_idx,pm1,pm2,pm3):
    
    #3-parametered optcodes add() and multiply()
    if oc==1 or oc==2:
        
        step = 4
        
        if pm1 == 1:
            n1 = intcode[pointer_idx+1]
        else:
            n1 = intcode[intcode[pointer_idx+1]]
            
        if pm2 == 1:
            n2 = intcode[pointer_idx+2]
        else:
            n2 = intcode[intcode[pointer_idx+2]]
        
        ix = intcode[pointer_idx+3]
        
    #1-parametered optcodes set() and return()
    elif oc==3:
        
        step = 2
        
        ix = intcode[pointer_idx+1]
        
    elif oc==4:
        
        step = 2
        
        if pm1 == 1:#immediate mode
            n1 = intcode[pointer_idx+1]
            
        else:#position mode
            n1 = intcode[intcode[pointer_idx+1]]
        
    #2-parametered optcode to jump the pointer to second parameter depending on first parameter
    elif oc==5 or oc==6:
        
        if pm1 == 1:#immediate mode
            n1 = intcode[pointer_idx+1]
        else:#position mode
            n1 = intcode[intcode[pointer_idx+1]]
            
        if pm2 == 1:
            n2 = intcode[pointer_idx+2]
        else:
            n2 = intcode[intcode[pointer_idx+2]]
        
        
        if oc==5:
            if n1:
                step = n2-pointer_idx
            else:
                step = 3
        
        if oc==6:
            if n1:
                step = 3
            else:
                step = n2-pointer_idx
        
    #less than / equals
    elif oc==7 or oc==8:
        
        step = 4
        
        if pm1 == 1:
            n1 = intcode[pointer_idx+1]
        else:
            n1 = intcode[intcode[pointer_idx+1]]
            
        if pm2 == 1:
            n2 = intcode[pointer_idx+2]
        else:
            n2 = intcode[intcode[pointer_idx+2]]
        
        ix = intcode[pointer_idx+3]
        
        
    #invalid optcode    
    else:
        print("invalid optcode")
        return None
    
    
    if oc==1:
        intcode[ix] = n1 + n2
    elif oc==2:
        intcode[ix] = n1 * n2
    elif oc==3:
        intcode[ix] = 5
    elif oc==4:
        return intcode,step,n1
    elif oc==7:
        if n1<n2:
            intcode[ix]=1
        else:
            intcode[ix]=0
    elif oc==8:
        if n1==n2:
            intcode[ix]=1
        else:
            intcode[ix]=0
    
    return intcode,step, None


# intcode = [3,9,8,9,10,9,4,9,99,-1,8]
# intcode = [3,9,7,9,10,9,4,9,99,-1,8]
# intcode = [3,3,1108,-1,8,3,4,3,99]
# intcode = [3,3,1107,-1,8,3,4,3,99]
# intcode = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
# intcode = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
# intcode = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
#            1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
#            999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
inputfile = "Input_5.txt"
intcode = read_intcode_from_csv(inputfile)
intcode2, output = intcode_run((intcode))



#puzzle 6.1

from graph import Graph

def graph_dict_from_file(inputfile):
    with open(inputfile, "r") as f:
        l = f.readlines()
        ls = [x.strip().split(")") for x in l]
    g_dict = {}
    for l in ls:
        orbited = l[0]
        orbitant = l[1]
        if not orbitant in g_dict.keys():
            g_dict[orbitant]=[orbited]
        else:
            g_dict[orbitant].append(orbited)
        if not orbited in g_dict.keys():
            g_dict[orbited]=[orbitant]
        else:
            g_dict[orbited].append(orbitant)
        
    g = Graph(g_dict)
        
    return g


inputfile = "Input_6.txt"
G = graph_dict_from_file(inputfile)

verts = G.vertices()

num_of_orbits = 0
for v in verts:
    n = len(G.find_path(v,"COM"))-1
    num_of_orbits += n

print("Solution for puzzle 6.1:",num_of_orbits)

#puzzle 6.2

start = G._Graph__graph_dict["YOU"]
end = G._Graph__graph_dict["SAN"]

transfers = len(G.find_path(start[0],end[0]))-1


#puzzle 7.2


#get initial intcode
def read_intcode_from_csv(inputfile):
    intcode_array = array_from_csv(inputfile)
    return intcode_array[0]
    


#get optcode ID and parameter modes from the instruction
def parameters_from_instruction(instruction):
    opcode = instruction%100
    pm1 = ((instruction-opcode)%1000)
    pm2 = (instruction-opcode)%10000 -pm1
    pm3 = (instruction-opcode)%100000 -pm2 -pm1
    
    pm1 = int(round(pm1/100))
    pm2 = int(round(pm2/1000))
    pm3 = int(round(pm3/10000))
    
    return opcode,pm1,pm2,pm3

#run optcode on intcode
def optcode_run(intcode,pointer_idx,instruction,initial_input):
    
    #extract optcode and parameter modes
    oc,pm1,pm2,pm3 = parameters_from_instruction(instruction)
    
    #3-parametered optcodes add() and multiply()
    if oc==1 or oc==2:
        
        step = 4
        
        if pm1 == 1:
            n1 = intcode[pointer_idx+1]
        else:
            n1 = intcode[intcode[pointer_idx+1]]
            
        if pm2 == 1:
            n2 = intcode[pointer_idx+2]
        else:
            n2 = intcode[intcode[pointer_idx+2]]
        
        ix = intcode[pointer_idx+3]
        
    #1-parametered optcodes set() and return()
    elif oc==3:
        
        step = 2
        
        ix = intcode[pointer_idx+1]
        
    elif oc==4:
        
        step = 2
        
        if pm1 == 1:#immediate mode
            n1 = intcode[pointer_idx+1]
            
        else:#position mode
            n1 = intcode[intcode[pointer_idx+1]]
        
    #2-parametered optcode to jump the pointer to second parameter depending on first parameter
    elif oc==5 or oc==6:
        
        if pm1 == 1:#immediate mode
            n1 = intcode[pointer_idx+1]
        else:#position mode
            n1 = intcode[intcode[pointer_idx+1]]
            
        if pm2 == 1:
            n2 = intcode[pointer_idx+2]
        else:
            n2 = intcode[intcode[pointer_idx+2]]
        
        
        if oc==5:
            if n1:
                step = n2-pointer_idx
            else:
                step = 3
        
        if oc==6:
            if n1:
                step = 3
            else:
                step = n2-pointer_idx
        
    #less than / equals
    elif oc==7 or oc==8:
        
        step = 4
        
        if pm1 == 1:
            n1 = intcode[pointer_idx+1]
        else:
            n1 = intcode[intcode[pointer_idx+1]]
            
        if pm2 == 1:
            n2 = intcode[pointer_idx+2]
        else:
            n2 = intcode[intcode[pointer_idx+2]]
        
        ix = intcode[pointer_idx+3]
        
        
    #invalid optcode    
    else:
        print("invalid optcode")
        return None
    
    
    if oc==1:
        intcode[ix] = n1 + n2
    elif oc==2:
        intcode[ix] = n1 * n2
    elif oc==3:
        intcode[ix] = initial_input
    elif oc==4:
        return intcode,step,n1 #n1 is the awesome output
    elif oc==7:
        if n1<n2:
            intcode[ix]=1
        else:
            intcode[ix]=0
    elif oc==8:
        if n1==n2:
            intcode[ix]=1
        else:
            intcode[ix]=0
    
    return intcode,step, None

#main function morphing the intcode
def thruster_intcode_run(intcode,phase_setting,input_value):
    phasing = True
    output_values = list()
    pointer=0
    instruction = intcode[pointer]
    #print(intcode)
   #print("Pointer:",pointer,"Instruction:",instruction)
    while instruction%100 != 99:
        if phasing:
            intcode,step,output_val = optcode_run(intcode,pointer,instruction,phase_setting)
            phasing = False
        else:
            intcode,step,output_val = optcode_run(intcode,pointer,instruction,input_value)
        output_values.append(output_val)
        pointer+=step
        instruction = intcode[pointer]
        #print(intcode)
        #print("Pointer:",pointer,"Instruction:",instruction)
    return output_val
        #print(intcode)

inputfile = "Input_7.txt"
orig_intcode = read_intcode_from_csv(inputfile)
#orig_intcode = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
#create all phase_state_combinations of inputs
phase_state_combinations = itertools.permutations([0,1,2,3,4], 5)
outputs = []
for p in phase_state_combinations:
    #first input always 0
    input_val = 0
    for phase_setting in p:
        intcode = copy.deepcopy(orig_intcode)
        output_val = thruster_intcode_run(intcode,phase_setting,input_val)
        #input for next amplifier is output of earlier amplifier
        input_val = output_val
    outputs.append(output_val)

print(max(outputs))

#puzzle7.2


def feedback_thruster_intcode_run(intcode,pointer,phase_setting,input_value,first):
    output_val = None
    
    instruction = intcode[pointer]
    
    while instruction%100 != 99:
        if first:
            intcode,step,output_val = optcode_run(intcode,pointer,instruction,phase_setting)
            first = False
        else:
            intcode,step,output_val = optcode_run(intcode,pointer,instruction,input_value)
        
        pointer+=step
        
        if instruction%100 ==4:
            return intcode,pointer,output_val,True
        else:
            instruction = intcode[pointer]
        
    return intcode,pointer,output_val,False
        

phase_state_combinations = itertools.permutations([5,6,7,8,9], 5)
#phase_state_combinations = [[9,8,7,6,5]]

inputfile = "Input_7.txt"
orig_intcode = read_intcode_from_csv(inputfile)
#orig_intcode = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
outputs = []
for phase_states in phase_state_combinations:
    #a flag indicating whether we are still in the loop
    still_running = True
    #flags indicating whether amplifiers are still in their first round
    firsts = [True]*len(phase_states)
    #container for the intcode states of all 5 amplifiers
    running_codes = [copy.deepcopy(orig_intcode) for x in range(5)]
    #container for pointers
    pointers = [0]*len(phase_states)
    #first input always 0
    input_val = 0
    while still_running:
        for amp_idx in range(len(phase_states)):
            #running codes are modified, output_values are returned and fed into the next amplifier and a flag indicates whether the loop ended
            running_codes[amp_idx], pointers[amp_idx],output_val,still_running = feedback_thruster_intcode_run(running_codes[amp_idx],
                                                                                                               pointers[amp_idx],
                                                                                                               phase_states[amp_idx],
                                                                                                               input_val,
                                                                                                               firsts[amp_idx])
            firsts[amp_idx] = False
            #input for next amplifier is output of earlier amplifier
            input_val = output_val
            if amp_idx == len(phase_states)-1 and still_running:
                current_end_output = output_val
               
    outputs.append(current_end_output)
print(max(outputs))


#puzzle8.1

def read_image_from_csv(inputfile, width, height):
    with open(inputfile) as f:
        data = f.readlines()
        data = data[0].strip()
        numbers = np.array([int(x) for x in data])
    depth = int(len(numbers)/width/height)
    #image = np.reshape(numbers, (height,width,-1), order = "C")
    image = np.zeros((height,width,depth))
    idx = 0
    for d in range(depth):
        for h in range(height):
            for w in range(width):
                image[h,w,d] = numbers[idx]
                idx+=1
    return(image)

def checksum(image):
    n_layers = image.shape[-1]
    n_zeros = np.zeros(n_layers)
    n_ones = np.zeros(n_layers)
    n_twos = np.zeros(n_layers)
    for l in range(n_layers):
        layer = image[:,:,l]
        n_zeros[l] = np.sum(layer==0)
        n_ones[l] = np.sum(layer==1)
        n_twos[l] = np.sum(layer==2)
    min_layer = np.argmin(n_zeros)
    out = n_ones[min_layer]*n_twos[min_layer]
    return int(out)


inputfile = "Input_8.txt"
width = 25
height = 6
im = read_image_from_csv(inputfile,width,height)
cs = checksum(im)

print("Solution for puzzle 8.1:", cs)



#puttle 8.2


def render_image(image):
    height = image.shape[0]
    width = image.shape[1]
    depth = image.shape[2]
    resulting_img = np.zeros((height,width))
    for h in range(height):
        for w in range(width):
            for d in range(depth):
                if image[h,w,d] != 2:
                    resulting_img[h,w] = image[h,w,d]
                    break
    return resulting_img
	
res_img = render_image(im)

sn.heatmap(res_img)



'''
#puzzle9.1

#get initial intcode
def read_intcode_from_csv(inputfile):
    intcode_array = array_from_csv(inputfile)
    return intcode_array[0]
    


#get optcode ID and parameter modes from the instruction
def parameters_from_instruction(instruction):
    opcode = instruction%100
    pm1 = ((instruction-opcode)%1000)
    pm2 = (instruction-opcode)%10000 -pm1
    pm3 = (instruction-opcode)%100000 -pm2 -pm1
    
    pm1 = int(round(pm1/100))
    pm2 = int(round(pm2/1000))
    pm3 = int(round(pm3/10000))
    
    return opcode,pm1,pm2,pm3

#run optcode on intcode
def optcode_run(intcode,pointer_idx,rel_base, instruction,initial_input):

    #extract optcode and parameter modes
    oc,pm1,pm2,pm3 = parameters_from_instruction(instruction)
    try:
        #3-parametered optcodes add() and multiply()
        if oc==1 or oc==2:
            
            step = 4
            
            if pm1 == 0:        
            	n1 = intcode[intcode[pointer_idx+1]]
            elif pm1 == 1:
                n1 = intcode[pointer_idx+1]
            elif pm1 == 2:
            	n1 = intcode[rel_base+intcode[pointer_idx+1]]
                
                
            if pm2 == 0:        
            	n2 = intcode[intcode[pointer_idx+2]]
            elif pm2 == 1:
                n2 = intcode[pointer_idx+2]
            elif pm2 == 2:
            	n1 = intcode[rel_base+intcode[pointer_idx+2]]
            
            
            ix = intcode[pointer_idx+3]
            
        #1-parametered optcodes set() and return()
        elif oc==3:
            
            step = 2
            
            ix = intcode[pointer_idx+1]
            
        elif oc==4:
            
            step = 2
            
            if pm1 == 0:#position mode
                n1 = intcode[intcode[pointer_idx+1]]
            elif pm1 == 1:#immediate mode
                n1 = intcode[pointer_idx+1]
            elif pm1 ==2:#relative mode
                n1 = intcode[rel_base + intcode[pointer_idx+1]]
                
            
        #2-parametered optcode to jump the pointer to second parameter depending on first parameter
        elif oc==5 or oc==6:
            
            if pm1 == 0:#position mode
                n1 = intcode[intcode[pointer_idx+1]]
            elif pm1 == 1:#immediate mode
                n1 = intcode[pointer_idx+1]
            elif pm1 ==2:
                n1 = intcode[rel_base+intcode[pointer_idx+1]]
                
            if pm2 == 0:#position mode
                n2 = intcode[intcode[pointer_idx+2]]
            elif pm2 == 1:#immediate mode
                n2 = intcode[pointer_idx+2]
            elif pm1 == 2:
                n2 = intcode[rel_base+intcode[pointer_idx+2]]
                
            
            if oc==5:
                if n1:
                    step = n2-pointer_idx
                else:
                    step = 3
            
            if oc==6:
                if n1:
                    step = 3
                else:
                    step = n2-pointer_idx
            
        #less than / equals
        elif oc==7 or oc==8:
            
            step = 4
            
            if pm1 == 0:        
            	n1 = intcode[intcode[pointer_idx+1]]
            elif pm1 == 1:
                n1 = intcode[pointer_idx+1]
            elif pm1 == 2:
            	n1 = intcode[rel_base+intcode[pointer_idx+1]]
                
            if pm2 == 0:        
            	n2 = intcode[intcode[pointer_idx+2]]
            elif pm2 == 1:
                n2 = intcode[pointer_idx+2]
            elif pm2 == 2:
            	n1 = intcode[rel_base+intcode[pointer_idx+2]]
            
            ix = intcode[pointer_idx+3]
            
            
            
        elif oc == 9:
            step = 2
            
            if pm1 == 0:#position mode
                n1 = intcode[intcode[pointer_idx+1]]
            elif pm1 == 1:#immediate mode
                n1 = intcode[pointer_idx+1]
            elif pm1 == 2:#relative mode
                n1 = intcode[rel_base + intcode[pointer_idx+1]]
        
        #invalid optcode
        else:
            print("invalid optcode")
            return None
    except IndexError:
        print("aha")
    
    if oc==1:
        intcode[ix] = n1 + n2
    elif oc==2:
        intcode[ix] = n1 * n2
    elif oc==3:
        intcode[ix] = initial_input
    elif oc==4:
        return intcode,step,rel_base,n1 #n1 is the awesome output
    elif oc==7:
        if n1<n2:
            intcode[ix]=1
        else:
            intcode[ix]=0
    elif oc==8:
        if n1==n2:
            intcode[ix]=1
        else:
            intcode[ix]=0
    elif oc==9:
        rel_base += n1
    
    return intcode,step, rel_base, None

#main function morphing the intcode
def boost_intcode_run(intcode,input_value):
    output_values = []
    pointer=0
    instruction = intcode[pointer]
    rel_base = 0
    #print(intcode)
   #print("Pointer:",pointer,"Instruction:",instruction)
    while instruction%100 != 99:
        intcode,step,rel_base,output_val = optcode_run(intcode,
                                                       pointer,
                                                       rel_base,
                                                       instruction,
                                                       input_value)
        output_values.append(output_val)
        pointer+=step
        instruction = intcode[pointer]
        #print(intcode)
        #print("Pointer:",pointer,"Instruction:",instruction)
    return intcode, output_values
        #print(intcode)

inputfile = "Input_9.txt"
intcode = read_intcode_from_csv(inputfile)
intcode =[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
outcode, value = boost_intcode_run(intcode, 100)
print(outcode)
print(value)
