#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:00:38 2024

@author: karlchen
"""

class LinkedNode:
    def __init__(self,val = None, next_ = None):
        self.val = val
        self.next = next_
        
    def __repr__(self):
        res = ""
        current = self
        while current is not None:
            add = str(current.val)+"->" 
            res += add
            current = current.next
        res = res.rstrip("->")
        return res
        
    def __len__(self):
        length = 0
        current = self
        while current is not None:
            length += 1
            current = current.next
        return length


def list_to_linked(list_: list):
    base = LinkedNode()
    current = base
    if list_:
        for i in list_:
            current.next = LinkedNode(i)
            current = current.next
    return base.next

def linked_to_list(linked: LinkedNode):
    l = [None for _ in range(len(linked))]
    i = 0
    current = linked
    while current is not None:
        l[i] = current.val
        i+=1
        current = current.next
    return l
    

def linked_to_dict(linked: LinkedNode):
    d = {}
    current = linked
    while current is not None:
        d[current.val] = current.next.val
        current = current.next
    return d


'''def dict_to_linked(dict_: dict):
    base = LinkedNode()
    current = base
    
    dic = deepcopy(dict_)
    if dic:
        key, val = dic.popitem()
    else:
        val = None
    
    while val:
        current.next = LinkedNode(key)
        key = val
        current = current.next
        if key in dic:
            val = dic[key]
        else:
            val = None
    return base.next
'''