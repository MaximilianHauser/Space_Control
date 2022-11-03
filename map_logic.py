# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 18:30:36 2022

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import json


# MapLogic class ------------------------------------------------------------ #
class MapLogic:
    # open a json-map-file and get the map data ----------------------------- #
    def load_from_json(json_file):
        json_o = open(json_file)
        map_raw = json.load(json_o)
        json_o.close()
        print(map_raw)
        return map_raw

    def get_dim(map_lst):
        rows = len(map_lst)
        colums = len(map_lst[0])
        return colums, rows
    
    def get_center(map_lst):
        columns, rows = MapLogic.get_dim(map_lst)
        r_correct = rows // 2 
        c_correct = columns // 2
        return c_correct, r_correct
    
    def assign_qrs(map_raw):
        map_setup_lst = []
        columns, rows = MapLogic.get_dim(map_raw)
        c_correct, r_correct = MapLogic.get_center(map_raw)
        for col in range(columns):
            for row in range(rows):
                q = col
                r = row
                s = -q-r
                t = map_raw[r][q][0]
                if t is not None:
                    u = map_raw[r][q][1]
                    map_setup_lst.append((q, r, s, t, u))
    
        print(map_setup_lst)
        return map_setup_lst

    


