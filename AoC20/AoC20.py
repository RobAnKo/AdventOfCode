d#!/usr/bin/env python3
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
import time
#from math import comb as mathcomb
from functools import reduce
os.chdir("/home/robinkoch/Documents/AdventOfCode/AoC20")
#os.chdir("/home/karlchen/Documents/AdventOfCode/AoC20")



def lines_from_txt(inputfile, form = "string"):
    with open(inputfile, 'r') as in_f:
        lines = (line.rstrip('\n') for line in in_f.readlines())
    if form == "string":
        return list(lines)
    elif form == "float":
        return list(float(x) for x in lines)
    elif form == "int":
        return list(int(x) for x in lines)
    else:
        print('form has to be one of ["string", "float", "int"]')
        return None

#helper function for multiplication of all elements in an iterable
def mult(args):
    prod = 1
    for a in args:
        prod *=a
    return prod


# # puzzle 1.1 & 1.2 together
# inputfile = "input_1.txt"
# numbers = lines_from_txt(inputfile, 'int')

# def multiply_2020_sum(numbers,n):
#     combs = list(itertools.combinations(numbers, n))
#     #generator because only used once
#     sums = [sum(x) for x in combs]
#     mults = np.array([mult(x) if y==2020 else 0 for x,y in zip(combs,sums)])
#     return(int(mults[mults.nonzero()]))



# print(multiply_2020_sum(numbers,2))
# print(multiply_2020_sum(numbers,3))

# ####
#         #We learned here that itertools might be faster than for-loops, but doesn't have to be. 
#         #It depends on size of problem and location of solution.
# ####


# # puzzle 2
# inputfile = "input_2.txt"
# pws = lines_from_txt(inputfile)


# # puzzle 2.1
# def number_of_valid_pws(pws):
#     n = 0
#     for pw in pws:
#         parts = pw.split()
#         range_ = parts[0]
#         range_ = range_.split('-')
#         mini = int(range_[0])
#         maxi = int(range_[1])
#         letter = parts[1][0]
#         password = parts[2]
#         if mini <= password.count(letter) <= maxi:
#             n+=1
#     return n


# print(number_of_valid_pws(pws))
        
# # puzzle 2.2
# def number_of_valid_pws_2(pws):
#     n = 0
#     for pw in pws:
#         parts = pw.split()
#         indices = parts[0]
#         indices = indices.split('-')
#         i1 = int(indices[0])
#         i2 = int(indices[1])
#         letter = parts[1][0]
#         password = parts[2]
#         i1b = password[i1-1]==letter
#         i2b = password[i2-1]==letter
#         if i1b + i2b == 1:
#             n+=1
#     return n

# print(number_of_valid_pws_2(pws))


# # puzzle 3
# inputfile = "input_3.txt"
# mountain = lines_from_txt(inputfile)
# directions = [[1,1],[3,1],[5,1],[7,1],[1,2]]

# # puzzle 3.1
# def tree_encounters(mountain, direction):
#     h = len(mountain)
#     w = len(mountain[0])
#     posx = direction[0]
#     posy = direction[1]
#     path = ""
#     while posy < h:
#         path += mountain[posy][posx]
#         posx += direction[0]
#         posy += direction[1]
#         if posx >= w:
#             posx -= w
#     print(path.count("#"))
#     return path.count("#")

# print(tree_encounters(mountain, directions[1]))


# # puzzle 3.2
# def multiple_tree_encounters(mountain, directions):
#     tree_mult = 1
#     for i in range(len(directions)):
#         tree_mult *= tree_encounters(mountain, directions[i]);
#     return tree_mult

# print(multiple_tree_encounters(mountain, directions))


# # # puzzle 4
# # inputfile = "input_4.txt"
# # passport_data = lines_from_txt(inputfile).astype('str')


# # # puzzle 4.1
# # def valid_passports(passport_data):
# #     return num_valid

# # print(valid_passports(passport_data))


# # # puzzle 4.2
# # def fun_4_2(passport_data):
# #     return 0

# # print(fun_4_2(passport_data))


# puzzle 5
# inputfile = "input_5.txt"
# binary_IDs = lines_from_txt(inputfile)


# def n_from_code(b):
#     mini = 0
#     maxi = 2**len(b) - 1
#     ii=0
#     pos = np.floor((maxi+mini)/2)
#     while (maxi>mini) & (ii<len(b)):
#         if (b[ii]=="F") | (b[ii] == "L"):
#             maxi = pos
#         elif (b[ii] == "B") | (b[ii] == "R"):
#             mini = pos+1
#         pos = np.floor((maxi+mini)/2)
#         ii+=1
#     return int(pos)

# def ID_from_bID(b):
#     str1 = b[0:7]
#     str2 = b[7:]
#     return int(n_from_code(str1)* 8 + n_from_code(str2))


# # puzzle 5.1
# def greatest_ID_from_bIDs(binary_IDs):
#     IDs = np.zeros((len(binary_IDs),1))
#     for ii in range(len(IDs)):
#         IDs[ii] = ID_from_bID(binary_IDs[ii])    
#     return int((max(IDs)))

# print(greatest_ID_from_bIDs(binary_IDs))

# # puzzle 5.2
# def seat_ID(binary_IDs):
#     IDs = np.zeros((len(binary_IDs)))
#     for ii in range(len(binary_IDs)):
#         IDs[ii] = ID_from_bID(binary_IDs[ii])    
#     IDs.sort()
#     not_there = np.where(np.diff(IDs) != 1)[0]
#     return(int(IDs[not_there]))

# print(seat_ID(binary_IDs))




# puzzle 7
# inputfile = "input_7.txt"
# bag_data = lines_from_txt(inputfile)



# def bag_dict_from_bag_data(bag_data, with_number = False):
#     bag_dict = dict()
#     for line in bag_data:
#         sp = line.split(" contain ")
#         k = "".join(sp[0].split(" ")[0:2])
#         if not with_number:
#             content = re.sub('[ .]|\d|bags|bag', '', sp[1]).split(",")
#         else:
#             contents = re.sub('[ .]|bags|bag', '', sp[1]).split(",")
#             colors = [re.search('([a-z]+)', bag).group() for bag in contents]
#             if colors[0] == "noother":
#                 content = None
#             else:
#                 numbers = [int(re.search('(\d)', bag).group()) for bag in contents]
#                 content = dict(zip(colors, numbers))
#         bag_dict[k] = content
#     return bag_dict



# # puzzle 7.1
# bag_dict = bag_dict_from_bag_data(bag_data, with_number = False)
# all_bags = list(bag_dict.keys())

# def contains_bag_of_interest(motherbags, bag_of_interest, bag_dict):
#     if isinstance(motherbags, set):
#         motherbags = set([x for x in motherbags if not x=='noother'])
#         subbags = set([bag for motherbag in motherbags for bag in bag_dict[motherbag]])
#     else:
#         subbags = set(bag_dict[motherbags])
        
#     #base case 1: we found the bag
#     if bag_of_interest in subbags:
#         return 1
#     #base case 2: there are no subbags anymore
#     if not subbags:
#         return 0
#     #recursive case: go deeper
#     else:
#         return contains_bag_of_interest(subbags, bag_of_interest, bag_dict)


# print(sum((contains_bag_of_interest(bag, "shinygold", bag_dict) for bag in all_bags)))

# # puzzle 7.2

# bag_dict = bag_dict_from_bag_data(bag_data, with_number = True)

# def number_of_subbags(motherbag, bag_dict):
#     subbags = bag_dict[motherbag]
#     #base case: no bags inside
#     if subbags == None:
#         return 1
#     else:
#         return 1+ sum((v*number_of_subbags(k, bag_dict) for k,v in subbags.items()))


# print(number_of_subbags("shinygold", bag_dict)-1) #should be 


# # puzzle 8
# inputfile = "input_8.txt"
# instructions = lines_from_txt(inputfile)
# instructions_visited = [0]*len(instructions)
# accumulator = 0


# #puzzle 8.1
# def follow_instruction(pointer = 0):
#     global instructions
#     global instructions_visited
#     global accumulator
    
#     if instructions_visited[pointer]:
#         return accumulator
#     else:
#         instructions_visited[pointer] = 1
#         instruction = instructions[pointer]
#         typ = instruction[0:3]
#         if typ == "nop":
#             return follow_instruction(pointer+1)
#         elif typ == "acc":
#             accumulator+= int(instruction[4:])
#             return follow_instruction(pointer+1)
#         elif typ == "jmp":
#             return follow_instruction(pointer+int(instruction[4:]))
        

# print(follow_instruction())

# #puzzle 8.2

# def follow_instruction_2(instructions, pointer=0):
#     global instructions_visited
#     global accumulator
    
#     if pointer==len(instructions):
#         return accumulator
#     elif instructions_visited[pointer]:
#         return None
#     else:
#         instructions_visited[pointer] = 1
#         instruction = instructions[pointer]
#         typ = instruction[0:3]
#         if typ == "nop":
#             return follow_instruction_2(instructions,pointer+1)
#         elif typ == "acc":
#             accumulator+= int(instruction[4:])
#             return follow_instruction_2(instructions,pointer+1)
#         elif typ == "jmp":
#             return follow_instruction_2(instructions,pointer+int(instruction[4:]))


# def mutate_instructions(instructions):
#     idxs = np.where([True if (x.startswith("nop") or x.startswith("jmp")) else False for x in instructions])[0]
#     n = len(idxs)
#     list_of_mutated_instructions = [None] * n
#     for i in range(n):
#         list_of_mutated_instructions[i] = mutate_instruction(instructions, idxs[i])
#     return list_of_mutated_instructions

# def mutate_instruction(instructions, i):
#     instructions_copy = copy.copy(instructions)
#     if instructions[i].startswith("jmp"):
#         instructions_copy[i] = re.sub("jmp", "nop", instructions[i])
#     elif instructions[i].startswith("nop"):
#         instructions_copy[i] = re.sub("nop", "jmp", instructions[i])
#     else:
#         print("Here should be either a 'jmp' or a 'nop' statement, but neither is here!")
#     return instructions_copy

# list_of_mutated_instructions = mutate_instructions(instructions)

# res = [None]*len(list_of_mutated_instructions)

# for i in range(len(list_of_mutated_instructions)):
#     instructions_visited = [0]*len(instructions)
#     accumulator = 0
#     res[i] = follow_instruction_2(list_of_mutated_instructions[i])

# print(res[np.where(res)[0][0]])



# puzzle 9
#inputfile = "input_9.txt"
#numbers = lines_from_txt(inputfile, form = "int")
#
## puzzle 9.1
#def check_number(numbers,index,preambel_length):
#    if index < preambel_length:
#        return False
#    
#    num = numbers[index]
#    preambel = numbers[index-preambel_length:index]
#    combs = itertools.combinations(preambel, 2);
#    sums = set((sum(x) for x in combs))
#    if num in sums:
#        return False
#    else:
#        return True
#
#preambel_length = 25
#idx = np.array([check_number(numbers, i, preambel_length) for i in range(len(numbers))]).nonzero()[0][0]
#print(numbers[idx])
#
## puzzle 9.2
#target = numbers[idx];
#
#def contiguous_sum_from_end(numbers, start, target):
#    s = 0
#    ixs = iter(range(start, 0, -1))
#    while s<target:
#        ix = ixs.__next__()
#        s+= numbers[ix]
#    if s == target:
#        return ix
#    else:
#        return None
#
#
#
#possible_idxs = range(idx-1,0,-1);
#
#for upper in possible_idxs:
#    lower = contiguous_sum_from_end(numbers, upper, target)
#    if lower:
#        print(max(numbers[lower:upper+1])+min(numbers[lower:upper+1]))
#        break
    

# puzzle 10
# inputfile = "input_10.txt"
# numbers = lines_from_txt(inputfile, form = "int")
# #add outlet and charging
# numbers.extend([0,max(numbers)+3])

# # puzzle 10.1
# def sorted_diffs(numbers):
#     s = sorted(numbers)
#     diffs = np.diff(s)
#     return diffs

# out = sorted_diffs(numbers)
# print(sum(out==1)*sum(out==3))


# #puzzle 10.2
# def find_poppable_idxs(numbers):
#     s = sorted(numbers)
#     diffs = np.diff(s)
#     pop_idxs = [0]*len(s)
#     for ix in range(1,len(s)):
#         if all(diffs[ix-1:ix+1] == 1):
#             pop_idxs[ix] = 1
#     return pop_idxs


# def number_of_options(n):
#     n_all_options = sum((mathcomb(n,k) for k in range(n,-1,-1)))
#     n_invalid_options = invalid_options(n)
#     return(n_all_options-n_invalid_options)


# def invalid_options(l):
#     return sum(range(1,l-1))

# def find_mutable_sections(numbers):
#     idxs = find_poppable_idxs(numbers)
#     section_dict = dict()
#     i=0
#     while i < len(idxs):
#         if idxs[i]:
#             k=i;
#             n = 1
#             i+=1
#             while idxs[i]:
#                 n+=1
#                 i+=1
#             section_dict[k] = n
#         else:
#             i+=1
#     return section_dict



# sec_dict = find_mutable_sections(numbers)

# noo = [number_of_options(v) for v in sec_dict.values()]

# res = mult(noo)

#puzzle 12
# from Ships import Ship
# inputfile = "input_12.txt"
# instructions = lines_from_txt(inputfile)
# starting_point = np.array([0,0]);

# #puzzle 12.1
# ship = Ship(instructions = instructions, start_position = starting_point)
# ship.run()
# print(ship.manhattan_dist_from_initial_position())

# #puzzle 12.2
# from Ships import Ship2
# relative_waypoint_pos = np.array([10,1])
# ship2 = Ship2(instructions = instructions,\
#               start_position = starting_point,\
#               waypoint_direction = relative_waypoint_pos)
# ship2.run()
# print(ship2.manhattan_dist_from_initial_position())


# puzzle 13

# inputfile = "input_13.txt"
# depart_time_and_busses = lines_from_txt(inputfile)

# # puzzle 13.1
# def find_closest_bus(input_info):
#     depart_t = int(input_info[0]);
#     busses = [int(x) for x in re.findall("(\d+)", input_info[1])]
#     hit = 0
#     t = depart_t
#     while not hit:
#         t += 1
#         resids = [t % x for x in busses]
#         if 0 in resids:
#             hit = 1
#             for i,r in enumerate(resids):
#                 if not r:
#                     bus_of_choice = busses[i]
#     return bus_of_choice*(t-depart_t)

# print(find_closest_bus(depart_time_and_busses))


# puzzle 13.2

# def find_timestamp(input_info):
#     #extract busses
#     busses = input_info[1].split(',')
#     #extract valid busses from busses
#     valid_busses = [int(valid_bus) for valid_bus in list(filter(lambda bus: bus != 'x', busses))]
#     #extract time differences needed between busses
#     bus_idxs = [idx if re.match("\d+", bus) else None for idx,bus in enumerate(busses)]
#     time_diffs = list(filter(lambda x: x != None, bus_idxs))
#     t = 0
#     step = valid_busses[0]
#     for i in range(1,len(valid_busses)):
#         next_bus = valid_busses[i]
#         t, step = find_time(t,step, next_bus, time_diffs[i])
#         n1 = t
#     return t
    
    


# def find_time(start_time, step, next_bus, offset):
#     found = 0
#     i= 0
#     while not found:
#         t = start_time + step*i
#         if not (t+offset) % next_bus:
#             found = 1
#         else:
#             i+=1
#     return t, step*next_bus

# print(find_timestamp(depart_time_and_busses))


# puzzle 14
# inputfile = "input_14.txt"
# mask_instructions = lines_from_txt(inputfile)
# mask_size = 36

# from BitmaskSystem import BitmaskSystem

# bmsys = BitmaskSystem(mask_instructions,mask_size)

# # puzzle 14.1
# bmsys.run1()
# print(bmsys.memory_sum())

# # puzzle 14.2
# bmsys.memory_reset()
# bmsys.run2()
# print(bmsys.memory_sum())

# puzzle 15

# inputfile = "input_15.txt"
# start_numbers = [int(x) for x in lines_from_txt(inputfile)[0].split(",")]
# n = 30000000
# # puzzle 15.1
# from MemoryGame import MemoryGame

# tic = time.perf_counter()
# mg = MemoryGame(start_numbers)
# mg.run(n)
# res1 = mg.last_spoken
# toc = time.perf_counter()
# print("Time for first MemoryGame version: "+ str(toc-tic))

# # puzzle 15.2
# from MemoryGame import MemoryGameEfficient
# tic2 = time.perf_counter()
# mg2 = MemoryGameEfficient(start_numbers)
# mg2.run(n)
# res2 = mg2.last_spoken
# toc2 = time.perf_counter()
# print("Time for second MemoryGame version: "+ str(toc2-tic2))


# from MemoryGame import MemoryGameBare
# tic3 = time.perf_counter()
# mg3 = MemoryGameBare(start_numbers)
# mg3.run(n)
# res3 = mg3.last_spoken
# toc3 = time.perf_counter()
# print("Time for third MemoryGame version: "+ str(toc3-tic3))


# puzzle 16
inputfile = "input_16.txt"
rules_and_tickets = lines_from_txt(inputfile)

from TicketChecker import TicketChecker


tc = TicketChecker(rules_and_tickets)

# puzzle 16.1
print(tc.check_tickets())

# puzzle 16.2
#tc.filter_valid_tickets()
print(tc.multiplied_departure_fields())