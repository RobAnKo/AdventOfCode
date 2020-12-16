#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 09:56:57 2020

@author: robinkoch
"""
import re

class TicketChecker:
    
    def __init__(self, input_list):
        #extract rules as dictionary with sets as values
        rules = [l for l in input_list if re.match("^[a-z].*\d$", l)]
        names = [rule.split(": ")[0] for rule in rules]
        ranges = [self.translate_range(rule.split(": ")[1]) for rule in rules]
        self.rule_dict = dict(zip(names,ranges))
        
        #all allowed numbers
        self.overall_range = set.union(*ranges)
        
        #extract my own ticket
        my_ticket_idx = [i+1 for i,l in enumerate(input_list) if l.startswith("your")][0]
        self.my_ticket = [int(num) for num in input_list[my_ticket_idx].split(",")]
        
        #extract all other tickets
        other_ticket_idx = [i+1 for i,l in enumerate(input_list) if l.startswith("nearby")][0]
        other_tickets = input_list[other_ticket_idx:]
        self.other_tickets = [[int(num) for num in ticket.split(",")] for ticket in other_tickets]


    def translate_range(self, rangestring):
        nums = [int(num) for num in re.findall("\d+",rangestring)]
        return set(range(nums[0],nums[1]+1)).union(set(range(nums[2],nums[3]+1)))


    def check_tickets(self):
        invalid_values = []
        for ticket in [self.my_ticket, *self.other_tickets]:
            invalid_values.extend(self.check_ticket(ticket))
        self.invalid_values = invalid_values
        return sum(invalid_values)


    def check_ticket(self, ticket):
        return [number for number in ticket if number not in self.overall_range]



