#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 15:34:54 2020

@author: robinkoch
"""
import re

class RuleMatcher:
    
    def __init__(self, rules_and_messages):
        rules = [l for l in rules_and_messages if re.match("^\d+", l)]
        self.rules = dict()
        self.final_rules = dict()
        for rule in rules:
            sp = rule.split(": ")
            key = int(sp[0])
            val = sp[1]
            if val.startswith('"'):
                self.rules[key] = re.search("[a-z]+", val).group()
                self.final_rules[key] = self.rules[key]
            else:
                val_list = val.split(" | ")
                vals = [[int(v) for v in val.split(" ")] for val in val_list]
                self.rules[key] = vals
                
        self.messages = [l for l in rules_and_messages if re.match("^[a-z]+", l)]
        
        
        
    def run(self, ruleID):
        self.number_of_matching_messages = sum([self.match_msg_to_rule(m,ruleID) for m in self.messages])
    
    
    def match_msg_to_rule(self, message, ruleID):
        
        rule = self.rules[ruleID]
        
        
        if all(matches):
            return 1
        else:
            return 0
        