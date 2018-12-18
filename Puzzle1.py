#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 18:00:43 2018

@author: karlchen
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

os.chdir("/home/karlchen/Desktop/AdventOfCode/")


'''
#puzzle1.1

def array_from_csv(inputfile):
    return pd.read_csv(inputfile, header = None).values


inputfile = "puzzle1_input.txt"

def frequency_change(inputfile):
    nums = array_from_csv(inputfile)
    return sum(nums)

fc = frequency_change("puzzle1_input.txt")

#puzzle1.2
def calibrate_frequency(inputfile):
    nums = np.loadtxt(inputfile, dtype=int)
    seq1 = nums.cumsum()
    last_val = seq1[-1]
    val_repos = seq1
    i=0
    while 1 > 0:
        i += 1
        seq = seq1 + (i*last_val)
        for s in seq:
            if s in val_repos:
                return s
        val_repos = np.append(val_repos, seq)

cf = calibrate_frequency(inputfile)

#puzzle 2.1
infile= "puzzle2_input.txt"

    
def count_n_letters(IDs,n):
    count = 0
    for ID in IDs:
        letters = set(ID)
        for l in letters:
            c = ID.count(l)
            if c == n:
                count += 1
                break
    return count

def checksum(IDs):
    x = count_n_letters(IDs,3)
    y = count_n_letters(IDs,2)
    return x*y

with open(infile, "r") as f:
    IDs = f.readlines()
    IDs = [ID.strip() for ID in IDs]
    
cs = checksum(IDs)
    

#puzzle 2.2
def distance_measure(string1, string2):
    l = len(string1)
    D = 0
    for i in range(l):
        if string1[i] != string2[i]:
            D += 1
    return D

def remove_bad_letter(string1,string2):
    l = len(string1)
    for i in range(l):
        if string1[i] != string2[i]:
            return string1[0:i] + string1[i+1:]

def find_special_gadget(IDs):
    candidates = []
    for ID1 in IDs:
        for ID2 in IDs:
            D = distance_measure(ID1,ID2)
            if D == 1:
                candidates.append((ID1,ID2))
    for c in candidates:
        string1 = c[0]
        string2 = c[1]
        result = remove_bad_letter(string1,string2)
    return result

find_special_gadget(IDs)

#puzzle 3.1

infile = "puzzle3_input.txt"

def clean_claims(claims):
    cc = list()
    for c in claims:
        ns = re.split("#|@|,|x|:",c)
        n = [int(x) for x in ns[1:]]
        n = [n[0],n[1],n[2],n[1]+n[3],n[2]+n[4]]
        cc.append(n) 
    return cc

def initial_fabric(claims):
    rights = [x[3] for x in claims]
    downs = [x[4] for x in claims]
    max_r = max(rights)
    max_d = max(downs)
    return np.zeros(shape=(max_r, max_d))

def claim_fabric(fabric,claims):
    for c in claims:
        fabric[c[2]:c[4],c[1]:c[3]] = fabric[c[2]:c[4],c[1]:c[3]] + 1
    return fabric#sum(sum(fabric >=2))
        
    
with open(infile, "r") as f:
    claims = f.readlines()
    claims = [claim.strip() for claim in claims]

cc = clean_claims(claims)

fabric = initial_fabric(cc)

result = claim_fabric(fabric,cc)

#puzzle3.2

def one_d_overlap(edges1,edges2):
    x11 = edges1[0]
    x12 = edges1[1]
    x21 = edges2[0]
    x22 = edges2[1]
    if  (x21 <= x11 <= x22) or (x11 <= x21 <= x12):
        return True
    else:
        return False
            

def two_claims_overlap(c1,c2):
    #horizontal overlap
    if one_d_overlap([c1[1], c1[3]], [c2[1], c2[3]]):
        if one_d_overlap([c1[2], c1[4]], [c2[2], c2[4]]):
            return True
    return False


c1 = cc[906]
c2 = cc[965]
two_claims_overlap(c1,c2)
two_claims_overlap(c2,c1)

d = dict()
for i in itertools.permutations(cc,2):
    ID = i[0][0]
    if ID not in d.keys():
        d[ID]=0
    if two_claims_overlap(i[0],i[1]):
        d[ID] += 1
for k,v in d.items():
    if v == 0:
        print(k)


#puzzle 4.1
infile = "puzzle4_input.txt"

df = pd.read_csv(infile, header =None)
df.sort_values(by=0, axis=0, inplace=True)
l = df[0].tolist()

def extract_all_guards(l):
    guards = []
    for i in l:
        if "Guard" in i:
            guards.append(int(i.split(" ")[3].strip("#")))
    return set(guards)
  
def count_mins_per_guard(l,guard):
    on = False
    mins = 0
    for i in l:
        if str(guard) in i:
            on = True
        if on and ("asleep" in i):
            sleep_mi = int(re.split(":|]",i)[1])
        if on and ("wakes" in i):
            wake_mi = int(re.split(":|]",i)[1])
            sleep_time = wake_mi-sleep_mi
            mins += sleep_time
        if ("Guard" in i) and not (str(guard) in i):
            on = False
    return(mins)

def min_dic_for_guard(l,guard):
    min_d = dict()
    for k,v in zip(range(0,60),itertools.repeat(0,60)):
        min_d[k] = v
    on = False
    for i in l:
        if str(guard) in i:
            on = True
        if on and ("asleep" in i):
            sleep_mi = int(re.split(":|]",i)[1])
        if on and ("wakes" in i):
            wake_mi = int(re.split(":|]",i)[1])
            for mi in range(sleep_mi,wake_mi):
                min_d[mi] += 1
        if ("Guard" in i) and not (str(guard) in i):
            on = False
    return min_d

def find_key_for_max_val(d):
    mv = max(d.values())
    return [k for k,v in d.items() if v == mv][0]

def find_pair_for_max_val(d):
    mv = max(d.values())
    return [(k,v) for k,v in d.items() if v == mv][0]


guards = extract_all_guards(l)
d = dict()
for g in guards:
    d[g] = count_mins_per_guard(l,g)

sleepy_guy = find_key_for_max_val(d)

min_dic_sleepy = min_dic_for_guard(l,sleepy_guy)
best_min = find_key_for_max_val(min_dic_sleepy)
result = sleepy_guy*best_min

#puzzle 4.2

big_d = dict()
for g in guards:
    big_d[g] = min_dic_for_guard(l,g)

sparse_d = dict()
for g in guards:
    sparse_d[g] = find_pair_for_max_val(big_d[g])

mv = max([x[1] for x in sparse_d.values()])
max_min = [x[0] for x in sparse_d.values() if x[1] == mv][0]
max_guard= [k for k,v in sparse_d.items() if v[1] == mv][0]
result = max_guard*max_min

#puzzle 5.1

infile = "puzzle5_input.txt"

def rm_multiple_ixs(l,ixs):
    for i in sorted(ixs,reverse = True):
        del l[i]
    return l

def react(l):
    ixs = []
    ii = 0
    while ii < len(l)-1:
        x = l[ii]
        y = l[ii+1]
        if x.swapcase() == y:
            ixs.extend([ii,ii+1])
            ii+=2
        else:
            ii+=1
    return rm_multiple_ixs(l,ixs)
        
        


with open(infile,"r") as f:
    l = list(f.readline().strip())
old_l = []
while old_l != l:
    old_l = l.copy()
    l = react(l)
result = len(l)

#puzzle 5.2
def len_if_remove(letter,ll):
    l = ll.copy()
    while letter in l:
        l.remove(letter)
    letter = letter.swapcase()
    while letter in l:
        l.remove(letter)
    old_l = []
    while old_l != l:
        old_l = l.copy()
        l = react(l)
    return len(l)

def find_key_for_min_val(d):
    mv = min(d.values())
    return [k for k,v in d.items() if v == mv][0]

all_letters = set(l)

d = dict()
for letter in all_letters:
    print(letter)
    d[letter] = len_if_remove(letter,l)

minkey = find_key_for_min_val(d)


#puzzle 6.1
infile = "puzzle6_input.txt"

def man_dist(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def find_unique_key_for_min_val(d):
    mv = min(d.values())
    ks = [k for k,v in d.items() if v == mv]
    if len(ks)>1:
        return 0
    else:
        return ks[0]

def find_unique_key_for_max_val(d):
    mv = max(d.values())
    ks = [k for k,v in d.items() if v == mv]
    if len(ks)>1:
        return 0
    else:
        return ks[0]

def nearest_point(p1, ps):
    d = dict()
    for p,ix in ps.items():
        d[p] = man_dist(p1,ix)
    return find_unique_key_for_min_val(d)

def fill_grid(grid,seeds):
    g = grid.copy()
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            g[i,j] = nearest_point((i,j), seeds)
    return g

def find_border_cases(grid):
    s = set()
    set1 = set(grid[0,:])
    set2 = set(grid[-1,:])
    set3 = set(grid[:,0])
    set4 = set(grid[:,-1])
    for ss in [set1,set2,set3,set4]:
        s = s.union(ss)
    return s

def find_biggest_area(grid, seeds):
    d = dict()
    outs = find_border_cases(grid)
    s = seeds.copy()
    for k in seeds.keys():
        if k in outs:
            s.pop(k)
    for k in s.keys():
        d[k] = sum(sum(grid == k))
    return [find_unique_key_for_max_val(d), max(d.values())]

seeds = dict()
with open(infile,"r") as f:
    l = f.readlines()
    l = [x.strip().split(",") for x in l]
    l = [(int(x[0]),int(x[1])) for x in l]
for k,v in zip(range(1,len(l)+1), l):
    seeds[k] = v

max_y = max([x[0] for x in seeds.values()])
max_x = max([x[1] for x in seeds.values()])

grid = np.zeros((max_y+10,max_x+10), dtype = np.int16)
fg = fill_grid(grid,seeds)

big_guy = find_biggest_area(fg,seeds)


#puzzle 6.2

def sum_of_all_distances(p1, seeds):
    s = 0
    for p in seeds.values():
        s += man_dist(p1, p)
    return s

def distance_map(grid, seeds):
    g = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            g[i,j] = sum_of_all_distances((i,j), seeds)
    return g
            
g= distance_map(grid,seeds)

size = sum(g.flatten()<10000)

#visualization of points
#for s in seeds.values():
#    g[s[0],s[1]] = 19000


#puzzle 7.1
infile = "puzzle7_input.txt"

def create_out_dic(l):
    d = dict()
    for pair in l:
        if pair[0] not in d.keys():
            d[pair[0]]= [pair[1]]
        else:
            d[pair[0]].append(pair[1])
    return d

def create_in_dic(l):
    d = dict()
    for pair in l:
        if pair[1] not in d.keys():
            d[pair[1]]= [pair[0]]
        else:
            d[pair[1]].append(pair[0])
    return d

def find_starts(d,all_elements):
    s = []
    vs = set([x for v in d.values() for x in v])
    for e in all_elements:
        if e not in vs:
            s.append(e)
    return s

def find_goal(d,all_elements):
    ks = set([x for v in d.keys() for x in v])
    for e in all_elements:
        if e not in ks:
            return e


def find_sequence(d_i, d_out, all_elements):
    d_in = d_i.copy()
    xs = find_starts(d_out, all_elements)
    g = find_goal(d_out, all_elements)
    xs.sort()
    seq = []
    while xs:
        x = xs[0]
        if x == g:
            seq.append(x)
            return ''.join(seq)
        if (x not in d_in.keys() or not d_in[x]):
            seq.append(x)
            affs = d_out[x]
            for a in affs:
                d_in[a].remove(x)
                if not d_in[a]:
                    xs.append(a)
                    d_in.pop(a)
            xs.remove(x)
            xs.sort()
    
    
    

with open(infile, 'r') as f:
    l = f.readlines()
l = [x.strip().split(" ") for x in l]
l = [[x[1],x[7]] for x in l]

all_elements = set([y for x in l for y in x])

d_in = create_in_dic(l)
d_out = create_out_dic(l)
#seq = find_sequence(d_in, d_out, all_elements)

#puzzle 7.2

def find_time_for_sequence(d_in, d_out, td, wd, all_elements):
    t = 0
    xs = find_starts(d_out, all_elements)
    q = {}
    for x in xs:
        q[x] = np.inf
    g = find_goal(d_out, all_elements)
    while 1>0:
        if xs:
            xs.sort()
            for w in wd.keys():
                if wd[w] == 'idle':
                    if len(xs) == 0:
                        break
                    x = xs[0]
                    ts = td[x]
                    q[x] = ts
                    wd[w] = x
                    xs.remove(x)
        shortest_time = min(q.values())
        shortest_job = [k for k,v in q.items() if v == shortest_time] [0] 
        for k,v in q.items():
            q[k] -= shortest_time
        q.pop(shortest_job)
        t += shortest_time
        if shortest_job == g:
            return t
        for w in wd.keys():
            if wd[w] == shortest_job:
                wd[w] = 'idle'
        affs = d_out[shortest_job]
        for a in affs:
            d_in[a].remove(shortest_job)
            if not d_in[a]:
                xs.append(a)
                d_in.pop(a)
            

time_dic = {}
for e,t in zip(sorted(list(all_elements)), range(61,61+len(all_elements))):
    time_dic[e] = t

worker_dic = {}
for w in range(5):
    worker_dic[w]='idle'

t = find_time_for_sequence(d_in, d_out, time_dic, worker_dic, all_elements)

#puzzle8.1
infile = "puzzle8_input.txt"

with open(infile, 'r') as f:
    numbers = [int(x) for x in f.readline().strip().split(' ')]

#numbers = [int(x) for x in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split(' ')]
#numbers = [int(x) for x in "1 1 0 1 99 2".split(' ')]
numbers = [2,12,3,1,0,1,1,0,2,12,12,0,1,13,7,0,3,1,1,1,1,2,3,4,5,6,7,8,9,10,11,12]

sum_meta = 0
def count_metadata(nums):
    global sum_meta
    while nums:
        for i in range(len(nums)):
            #print(nums)
            #print(nums[i])
            if nums[i] == 0:
                n_metadata = nums[i+1]
                if i>= 2:
                    nums[i-2] -= 1
                else:
                    print('bah!')
                
                sum_meta += sum(nums[i+2:i+2+n_metadata])
                length = 2+n_metadata
                nums = [x for y in [nums[:i], nums[i+length:]] for x in y]
                break

        
count_metadata(numbers)
print(sum_meta)

#puzzle8.2

#try nested dictionary
k = 0
d ={}
def make_nodes_dictionary(numbers):
    global d
    global k
    while 1>0:
        n_nodes=numbers[0] 
        n_metadata = numbers[1]
        if n_nodes == 0:
            metadata = numbers[2:2+n_metadata]
            return metadata
        else:
            print('yay')
        k+=1

def get_node_indices(numbers):
    i = 0
    idx = []
    tail = numbers[1]
    while i<len(numbers)-tail:
        idx.append(i)
        if numbers[i] == 0:
            n_metadata=numbers[i+1] 
            i+= 2+n_metadata
        else:
            i+=2
    return idx
    
n_idx = get_node_indices(numbers)
'''

'''
#puzzle 10.1

infile = "puzzle9_input.txt"


with open(infile, "r") as f:
    l = f.readlines()
l = [re.split(">|<", x.strip()) for x in l]

positions = [x[1].split(',') for x in l]
positions = [[int(x[0]), int(x[1])]for x in positions]
xs = [x[0] for x in positions]
ys = [x[1] for x in positions]
speeds = [x[3].split(",") for x in l]
speeds = [[int(x[0]), int(x[1])] for x in speeds]
speedx = [x[0] for x in speeds]
speedy = [x[1] for x in speeds]
i=10330
k=1
while i<10340:
    xxs = [x + i*k*y for x,y in zip(xs,speedx)]
    yys = [x + i*k*y for x,y in zip(ys,speedy)]
    fig = plt.figure(figsize = (5,5), dpi = 300)
    ax = fig.gca()
    ax.scatter(yys, xxs, s=1)
    ax.text(0.2,0.2,str(i*k), transform = ax.transAxes)
    if i == 10330:
        lims = [ax.get_xlim(), ax.get_ylim()]
    else:
        ax.set_xlim(lims[0])
        ax.set_ylim(lims[1])
    fig.savefig("plot"+str(i)+".png", format = 'png')
    i +=1

#puzzle11



gridID = 8979
grid = np.zeros((300,300), dtype="int16")
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        rackid=j+10
        grid[i,j] = int(str((rackid*i+gridID)*rackid)[-3])-5

d = {}
td = {}
for n in range(1,300,1):
    now = datetime.now()
    print(n)
    sumgrid = np.zeros_like(grid)
    xrange = grid.shape[0]
    yrange = grid.shape[1]
    for i in range(xrange):
        if i >= xrange-n:
            print(str(n) + " " + str(i))
            break
        for j in range(yrange):
            if j >= yrange-n:
                break
            sumgrid[i,j] = sum(sum(grid[i:i+n, j:j+n]))
    max_val = sumgrid.max()
    idx = np.unravel_index(np.argmax(sumgrid), sumgrid.shape)
    idx = [idx[1]-1, idx[0]-1]
    d[n] = max_val
    d_t = datetime.now()-now
    d_t = d_t.total_seconds()
    td[n] = d_t
mv = max(d.values())

k = [x for x,v in d.items() if v ==mv][0]
sumgrid=np.zeros_like(grid)
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        sumgrid[i,j] = sum(sum(grid[i:i+k, j:j+k]))
    idx = np.unravel_index(np.argmax(sumgrid), sumgrid.shape)
    idx = [idx[1], idx[0]]

idx.append(k)
'''
    
#puzzle12
'''
infile = "puzzle12_input.txt"


def update_state(state, d):
    new_state = state.copy()
    for ix in range(len(state)-4):
        window = state[ix:ix+5]
        if window in d[1]:
            new_state[ix+2] = 1
        else:
            new_state[ix+2] = 0
    return new_state

with open(infile,"r") as f:
    l = f.readlines()


init_state = l[0].strip().split(": ")[1]
init_state = list(init_state.replace("#","1").replace(".","0"))
init_state = [int(x) for x in init_state]
padding = [0 for i in range(5000)]
state = padding + init_state + padding
#state = np.array(state, dtype = int)
origin = len(padding)
                                     

rules = l[2:]
rules = [x.strip().split(' => ') for x in rules]
rules = [[y.replace("#","1").replace(".","0") for y in x] for x in rules]
rule_dic = {0:[],1:[]}
for rule in rules:
    rule_dic[int(rule[1])].append([int(x) for x in rule[0]])
    #rule_dic[int(rule[1])].append(np.array([int(x) for x in rule[0]], dtype = int))

idx = range(-origin,len(init_state)+origin)
states = np.zeros((1001,len(state)), dtype = np.int)
states[0,:] = state
sum_dic = {}
for gen in range(1001):
    print(gen)
    states[gen,:] = state
    sum_dic[gen] =sum([ix for i,ix in zip(range(len(state)), idx) if state[i]])
    state = update_state(state,rule_dic)
    
gens = list(sum_dic.keys())
sums = list(sum_dic.values())
ss = np.array(sums)
diffs = np.diff(ss)
plt.scatter(gens,sums, s=1)

def sum_from_gen(sum_dic,gen):
    sums = list(sum_dic.values())
    diffs = np.diff(sums)
    for i in range(len(diffs)):
        if diffs[i] == diffs[i+1] == diffs[i+2]:
            print(i)
            break
    g0=i
    s0=sums[i]
    m = diffs[i]
    g = gen-g0
    return m*g+s0
result = sum_from_gen(sum_dic,50000000000)


#puzzle13

class car():
    global matrix
    global cars
    def __init__(self,ID, position, direction, next_turn):
        self.ID = ID
        self.position = position
        self.direction = direction
        self.next_turn = next_turn
        self.next_index = tuple([x+y for x,y in zip(self.position, self.direction)])
        self.affected_tile = matrix[self.next_index]
        self.sitting_on = self.initial_sit()
        self.crashed = False
        
    def __repr__(self):
        return "Car "+str(self.ID)+ ", position "+ str(self.position)+ ", direction "+str(self.direction)+ ", next turn: "+self.next_turn+"\n"
    
    def initial_sit(self):
        if matrix[self.position] in ['>','<']:
            return '-'
        else:
            return '|'
    
    def move(self):
        matrix[self.position] = self.sitting_on
        self.position = self.next_index
        self.sitting_on = self.affected_tile
    
    def remove(self):
        matrix[self.position] = self.sitting_on
        cars.remove(self)
    
    def turn_cross(self):
        if self.next_turn == "left":
            self.next_turn = "straight"
            if self.direction == [0,1]:
                self.direction = [-1,0]
                return
            if self.direction == [-1,0]:
                self.direction = [0,-1]
                return
            if self.direction == [0,-1]:
                self.direction = [1,0]
                return
            if self.direction == [1,0]:
                self.direction = [0,1]
                return
        if self.next_turn == "straight":
            self.next_turn = "right"
            return
        if self.next_turn == "right":
            self.next_turn = "left"
            if self.direction == [0,1]:
                self.direction = [1,0]
                return
            if self.direction == [1,0]:
                self.direction = [0,-1]
                return
            if self.direction == [0,-1]:
                self.direction = [-1,0]
                return
            if self.direction == [-1,0]:
                self.direction = [0,1]
                return
        
    def update(self):
        self.next_index = tuple([x+y for x,y in zip(self.position, self.direction)])
        self.affected_tile = matrix[self.next_index]
        matrix[self.position] = inv_dir_dic[tuple(self.direction)]

    def decide(self):
        global cars
        self.update()
        if self.affected_tile in car_symbols:
            for other_car in cars:
                if other_car.position == self.next_index:
                    other_car.crashed = True
            self.crashed = True
            print("Crash: "+str(tuple(reversed(self.next_index))))
            return(True)
        if self.affected_tile == "+":
            #print("A Crossroad!")
            self.move()
            self.turn_cross()
            self.update()
            return
        elif self.affected_tile == '/':
            self.move()
            #print('A curve!')
            if self.direction == [1,0]:
                self.direction = [0,-1]
            elif self.direction == [-1,0]:
                self.direction = [0,1]
            elif self.direction == [0,1]:
                self.direction = [-1,0]
            elif  self.direction == [0,-1]:
                self.direction = [1,0]
            self.update()
            return
        elif self.affected_tile == '\\':
            self.move()
            #print('A curve!')
            if self.direction == [1,0]:
                self.direction = [0,1]
            elif  self.direction == [-1,0]:
                self.direction = [0,-1]
            elif self.direction == [0,1]:
                self.direction = [1,0]
            elif  self.direction == [0,-1]:
                self.direction = [-1,0]
            self.update()
            return
        if self.affected_tile in ["-","|"]:
            self.move()
            self.update()
            return
        if self.affected_tile == ' ':
            print("SCREAM; ANGER; AGONY; OUT OF TRACK!")
                
def find_vehicle_positions(m, cs):
    idx = np.isin(m,cs)
    return np.where(idx)

def initialize_vehicles(matrix, car_symbols):
    pos = find_vehicle_positions(matrix, car_symbols)
    #car_dic = {}
    cars = [] 
    c = 0
    for y,x in zip(pos[0],pos[1]):
        sign = matrix[y,x]
        #car_dic[c] = car(ID = c, position = [y,x], direction = dir_dic[sign], next_turn = "left")
        cars.append(car(ID = c, position = (y,x), direction = dir_dic[sign], next_turn = "left"))
        c+=1
    return cars#car_dic



    
def find_vehicle_hierarchy(m, cs, cars):#cd):
    pos = find_vehicle_positions(m,cs)
    seq = list()
    for y,x in zip(pos[0],pos[1]):
        #for k,c in cd.items():
        for c in cars:
            if c.position == (y,x):
                seq.append(c.ID)
    return seq
         
                
def move_vehicles(m, vh, cars):#cd):
    #crashes = np.zeros_like(vh)
    i=0
    for active_v in vh:
        for c in cars:
            if c.ID == active_v:
                if c.crashed:
                    c.remove()
                else:
                    c.decide()

def remove_crashes(cars):
    crashfree = False
    while 1>0:
        if crashfree:
            return
        else:
            for c in cars:
                if c.crashed:
                    c.remove()
                    break
            if not any([x.crashed for x in cars]):
                crashfree = True
               
            
infile = "puzzle13_input.txt"
with open(infile,"r") as f:
    l = f.readlines()
l = [list(x.strip("\n")) for x in l]
matrix = np.matrix(l)

car_symbols = ["v", "^", ">", "<"]

dir_dic = {"v":[1,0],">":[0,1], "^":[-1,0], "<":[0,-1]}
inv_dir_dic = {}
for k,v in dir_dic.items():
    inv_dir_dic[tuple(v)] = k

            
cars = initialize_vehicles(matrix, car_symbols)
vh = find_vehicle_hierarchy(matrix, car_symbols, cars)
#crash = False
#i=0
#while not crash:
#    i+=1
#    print(i)
#    crash = move_vehicles(matrix, vh, cars)
#    vh = find_vehicle_hierarchy(matrix, car_symbols, cars)
    #np.savetxt("./arrays/array"+str(i)+".txt", matrix, fmt = '%1.1s',header = str(i))

#puzzle 13.2
i=0
while len(cars) > 1:
    #i+=1
    #print(i)
    move_vehicles(matrix, vh, cars)
    remove_crashes(cars)
    print(len(cars))
    vh = find_vehicle_hierarchy(matrix,car_symbols,cars)
    #np.savetxt("./arrays/array"+str(i)+".txt", matrix, fmt = '%1.1s',header = str(i))
result = tuple(reversed(cars[0].position))


#puzzle14.1

print("started at {}".format(datetime.now()))
inp = 765071
inps = str(inp)
max_len = inp+10

s = "37"
val1 = "3"
pos1 = 0
val2 = "7"
pos2 = 1
l = len(s)
broken = False
while 0 < 1:
    newval= int(val1)+int(val2)
    if l%100000 == 0:
        print("at {} we have {} letters".format(datetime.now(),len(s)))
    nv=str(newval)
    s += nv
    l = len(s)
    pos1 = (pos1+int(val1)+1)%l
    val1 = s[pos1]
    pos2 = (pos2+int(val2)+1)%l
    val2 = s[pos2]
#s.find(inps)

print("finished at {}".format(datetime.now()))

'''
#puzzle 16

infile = "puzzle16_input.txt"

with open(infile, "r") as f:
    l = [x.strip() for x in f.readlines()]


befores = [x.split(": ")[1].strip("[]").split(', ') for x in l if x.startswith("Bef")]
befores = [[int(x) for x in y] for y in befores]
afters = [x.split(":  ")[1].strip("[]").split(', ') for x in l if x.startswith("Aft")]
afters = [[int(x) for x in y] for y in afters]
opcodes = [[int(x) for x in y.split(" ")] for y in l if (y and y[0] in [str(i) for i in range(10)])]

#functions




def addr(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]+r[p[2]]
    return r
def addi(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]+p[2]
    return r
def mulr(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]*r[p[2]]
    return r
def muli(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]*p[2]
    return r
def banr(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]&r[p[2]]
    return r
def bani(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]&p[2]  
    return r
def borr(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]|r[p[2]]
    return r
def bori(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]|p[2]
    return r
def setr(p,rr):
    r = rr.copy()
    r[p[3]]=r[p[1]]
    return r
def seti(p,rr):
    r = rr.copy()
    r[p[3]]=p[1]
    return r
def gtir(p,rr):
    r = rr.copy()
    if p[1]>r[p[2]]:
        r[p[3]] = 1
    else:
        r[p[3]] = 0
    return r
def gtri(p,rr):
    r = rr.copy()
    if r[p[1]]>p[2]:
        r[p[3]] = 1
    else:
        r[p[3]] = 0
    return r
def gtrr(p,rr):
    r = rr.copy()
    if r[p[1]]>r[p[2]]:
        r[p[3]] = 1
    else:
        r[p[3]] = 0
    return r
def eqir(p,rr):
    r = rr.copy()
    if p[1]==r[p[2]]:
        r[p[3]] = 1
    else:
        r[p[3]] = 0
    return r
def eqri(p,rr):
    r = rr.copy()
    if r[p[1]]==p[2]:
        r[p[3]] = 1
    else:
        r[p[3]] = 0
    return r
def eqrr(p,rr):
    r = rr.copy()
    if r[p[1]]==r[p[2]]:
        r[p[3]] = 1
    else:
        r[p[3]] = 0
    return r
    
funs = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

overthree = 0
for b, p, a, in zip(befores, opcodes, afters):
    per_chunk = 0
    for f in funs:
        if f(p, b) == a:
            #print(f)
            #print( str(f(p,b))+"  "+ str(a))
            per_chunk +=1
    if per_chunk ==2:
        print(f)
        print(p[0])
        overthree+=1
print(overthree)

fun_dic={8:eqrr}
