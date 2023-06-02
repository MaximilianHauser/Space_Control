# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 08:00:46 2022

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import json

# define map ---------------------------------------------------------------- #
test_map = [
    
    [[None], [None], ["s", "r_cc"], ["s", None], ["s", None]],
    
    [[None], ["s", None], ["s", None], ["b", None], ["s", None]],
    
    [["s", None], ["a", None], ["b", None], ["a", None], ["s", None]],
    
    [["s", None], ["m", None], ["s", None], ["s", None], [None]],
    
    [["s", None], ["s", None], ["s", "b_cc"], [None], [None]]
    
            ]

# creates json file and writes map to it ------------------------------------ #
with open('test_map.json', 'w') as file:
    json.dump(test_map, file)
    
file.close()