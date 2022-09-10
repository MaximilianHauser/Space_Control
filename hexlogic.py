# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 07:19:00 2022

Will contain all hextile logic, such as distances, neighbors, range

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
from main import TILE_WIDTH, TILE_HEIGHT

# class responsible for handling hexagon specific logic --------------------- #
class HexLogic:
    
    # function return qrs_coords of object ---------------------------------- #
    def get_qrs(obj):
        q = obj.q
        r = obj.r
        s = obj.s
        return (q,r,s)
    
    # function to set qrs_coords of object ---------------------------------- #
    def set_qrs(obj, q, r, s):
        obj.q = q
        obj.r = r
        obj.s = s
    
    # function converts hex_coords to pixel_coords -------------------------- #
    def hex_to_pixel(q,r,s):
        x = TILE_WIDTH * (3 / 2 * q)
        y = TILE_HEIGHT * (3 ** 0.5 / 2 * q  +  3 ** 0.5 * r)
        return x, y
    
    # function converts pixel_coords to hex_coords -------------------------- #    
    def pixel_to_hex(x, y):
        q = ( 2./3 * x ) / TILE_WIDTH
        r = (-1./3 * x  +  3 ** 0.5 /3 * y) / TILE_HEIGHT
        s = -q-r
        return q, r, s
    
    # function return coords of neighboring hexes --------------------------- #
    def nbors(obj):
        (q,r,s) = HexLogic.get_qrs(obj)
        nbors_lst = [(q+1,r,s-1), (q+1,r-1,s), (q,r-1,s+1), (q-1,r,s+1), (q-1,r+1,s), (q,r+1,s-1)]
        return nbors_lst
    
    # function returns distance from one hex to another --------------------- #
    def dist(obj_a, obj_b):
        q_diff, r_diff, s_diff = abs(obj_a.q - obj_b.q), abs(obj_a.r - obj_b.r), abs(obj_a.s - obj_b.s)
        ab_dist = max(q_diff, r_diff, s_diff)
        return ab_dist
    
    # function returns every hex within a distance from a hex --------------- #
    # hex_coords within range n of hex_center ------------------------------- #
    def rnge(obj, n):
        hex_in_range_lst = []
        for q in range(-n, n):
            for r in range(max(-n, -q-n), min(n, -q+n)):
                s = -q-r
                hex_in_range_lst.append((obj.q+q, obj.r+r, obj.s+s))
        return hex_in_range_lst
    
    # function draws a line from one hex to another converted to hexes ------ #
    def line_draw(obj_a, obj_b, t):
        pass
    
    # distance from a hex, factoring in obstacles --------------------------- #
    def dist_lim_flood_fill(start, moves):
        pass
    
    
    
    
    
    
    
    
    