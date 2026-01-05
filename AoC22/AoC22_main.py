#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 22:34:20 2022

@author: karlchen
"""

class FileNavigator():
    
    def __init__(self, path):
        with open(path) as f:
            ls = f.readlines()
        self.input = [l.strip() for l in ls]
        self.filetree = {"/":[]}
        self.position = "/"
        self.parent = None
        self.commands = [(i,line) for i,line in enumerate(self.input) if line.startswith("$")]
    
    def parse_input(self):
        command_idx = 0
        while command_idx < len(self.commands):
            command_pointer = self.commands[command_idx][0]
             
            if command_idx != len(self.commands)-1:
                next_command_pointer = self.commands[command_idx+1][0]
                lines = self.input[command_pointer:next_command_pointer]
            else:
                lines = self.input[command_pointer:]
            
            self.handle_lines(lines)
             
            command_idx+=1
        return
    
    def handle_lines(self,lines):
        command = lines[0].lstrip("$ ")
        print(command)
        if command.startswith("cd"):
            argument = command.split(" ")[-1]
            if argument == "..":
                self.position = self.parent
                self.parent = self.find_parent(self.position)
            else:
                if argument != self.position:
                    self.add_to_tree(self.position, argument)
                    self.parent = self.position
                    self.position = argument
                self.add_to_tree(argument)
        elif command.startswith("ls"):
            to_add = lines[1:]
            self.add_from_lines(to_add)
            
    def find_parent(self, position):
        p = [key for key, val in self.filetree.items() if position in val]
        if p:
            return p[0]
        else:
            return None
        
    def add_from_lines(self, to_add):
        for line in to_add:
            sp = line.split(" ")
            if sp[0] == "dir":
                self.add_to_tree(self.position, sp[1])
            else:
                file = sp[1]
                size = int(sp[0])
                self.add_to_tree(self.position, file)
                self.add_to_tree(file, size)
        return
    
                
    def add_to_tree(self, key, value=None):
        if key not in self.filetree.keys():
            if value==None:
                self.filetree[key] = []
            else:
                self.filetree[key] = [value]
        else:
            if value==None:
                pass
            else:
                if value not in self.filetree[key]:
                    self.filetree[key].append(value)
        return
        
        
    
    
    
    
path = "/home/karlchen/Documents/AdventOfCode/AoC22/input_7.txt"

navi = FileNavigator(path)
navi.parse_input()
navi.calculate_sizes()
