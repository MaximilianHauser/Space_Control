# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 17:48:33 2022

@author: Maximilian Hauser
"""


# Last In First Out Linear Data Structure ----------------------------------- #
class Stack:
    def __init__(self):
        self.items = list()
        
    def is_empty(self):
        return self.items == []
    
    def push(self, item):
        self.items.extend([item])
        
    def pop(self):
        return self.items.pop()
    
    def print_stack(self):
        print(self.items)
        
        
# First In First Out Linear Data Structure ---------------------------------- #
class Queque:
    def __init__(self):
        self.items = list()
    
    def is_empty(self):
        return self.items == []
    
    def enqueque(self, item):
        self.items.insert(0, item)
        
    def insert_past_value(self, item, value, is_dict=True, dict_key="Current_INI"):
        if is_dict:
            res = next((x for x, val in enumerate(self.items) if val[dict_key] > value), len(self.items))
        else:
            res = next((x for x, val in enumerate(self.items) if val > value), len(self.items))
        self.items.insert(res, item)
        
    def dict_val_add(self, key, value):
        for item in self.items:
            item[key] += value
        
    def dequeque(self):
        return self.items.pop()
    
    def print_stack(self):
        print(self.items)
        
        
# Linked List Linear Data Structure ----------------------------------------- #
class Node:
    def __init__(self, data, pointer):
        self.data = data
        self.pointer = pointer
        
class LinkedList:
    def __init__(self):
        self.head = None
        
    def add_at_front(self, data):
        self.head = Node(data, self.head)
        
    def add_at_end(self, data):
        if not self.head:
            self.head = Node(data, None)
            return
        curr = self.head
        while curr.pointer:
            curr = curr.pointer
        curr.pointer = Node(data, None)
    
    def get_last_node(self):
        n = self.head
        while n != None:
            print(n.data, end = " => ")
            n = n.pointer
        print()
        
        
# Graph Non-Linear Data Structure ------------------------------------------- #
class Graph:
    def __init__(self, size):
        self.size = size
        self.adj = [[0] * size for i in range(size)]
        
    def add_edge(self, orig, dest):
        if orig > self.size or dest > self.size or orig < 0 or dest < 0:
            raise IndexError
        else:
            self.adj[orig-1][dest-1] = 1
            self.adj[dest-1][orig-1] = 1
            
    def remove_edge(self, orig, dest):
        if orig > self.size or dest > self.size or orig < 0 or dest < 0:
            raise IndexError
        else:
            self.adj[orig-1][dest-1] = 0
            self.adj[dest-1][orig-1] = 0
            
    def display(self):
        for row in self.adj:
            print()
            for val in row:
                print("{:4}".format(val), end="")


