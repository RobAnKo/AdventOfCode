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
    
    
    def filter_valid_tickets(self):
        self.valid_tickets = [ticket for ticket in self.other_tickets  if not self.check_ticket(ticket)]
        
        
    def multiplied_departure_fields(self):
        if not hasattr(self, "valid_tickets"):
            self.filter_valid_tickets()
        
        self.position_dict = dict()
        
        n_fields = len(self.rule_dict)
        #n_valid_tickets = len(self.valid_tickets)
        
        for fieldname, value_range in self.rule_dict.items():
            self.position_dict[fieldname] = []
            for field_idx in range(n_fields):
                values = [t[field_idx] for t in self.valid_tickets]
                if all([v in value_range for v in values]):
                    self.position_dict[fieldname].append(field_idx)
        
        self.filter_position_dict()
        
        dep_idxs = [idx for name, idx in self.position_dict.items() if name.startswith("departure")]
        dep_values = [self.my_ticket[i] for i in dep_idxs]
        
        
        return(self.mult(dep_values))

    def filter_position_dict(self):
        new_filter_dict = dict(zip(self.position_dict.keys(), [None]*len(self.position_dict)))
        val_lengths = [len(vs) for vs in self.position_dict.values()]
        while any((v >= 1 for v in val_lengths)):
            single_field_pairs = [(field,self.position_dict[field][0]) for l,field in zip(val_lengths, self.position_dict) if l==1]
            for single_field, single_value in single_field_pairs:
                new_filter_dict[single_field] = single_value
                for fieldkey in self.position_dict:
                    if single_value in self.position_dict[fieldkey]:
                        self.position_dict[fieldkey].remove(single_value)
            val_lengths = [len(vs) for vs in self.position_dict.values()]
        self.position_dict = new_filter_dict
            
            
            

    def mult(self,args):
        prod = 1
        for a in args:
            prod *=a
        return prod


