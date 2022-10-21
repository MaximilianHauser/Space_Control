# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 07:19:00 2022

Will contain all hextile logic, such as distances, neighbors, range, etc.

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
from settings import TILE_WIDTH, TILE_HEIGHT

# class responsible for handling hexagon specific logic --------------------- #
class HexLogic:
    
    # helper functions ------------------------------------------------------ #
    # linear interpolation returns point at t of distance between a and b --- #
    def linint(a, b, t):
        return a + (b - a) * t

    # linint for cube coords ------------------------------------------------ #
    def cube_linint(obj_a, obj_b, t):
        q = HexLogic.linint(obj_a.q, obj_b.q, t)
        r = HexLogic.linint(obj_a.r, obj_b.r, t)
        s = HexLogic.linint(obj_a.s, obj_b.s, t)
        return q,r,s

    # returns the nearest full hex coordinate in case of float(qrs) --------- #
    def round_hex(q_f,r_f,s_f):
        q = round(q_f)
        r = round(r_f)
        s = round(s_f)

        q_diff = abs(q - q_f)
        r_diff = abs(r - r_f)
        s_diff = abs(s - s_f)

        if q_diff > r_diff and q_diff > s_diff:
            q = -r-s
        elif r_diff > s_diff:
            r = -q-s
        else:
            s = -q-r

        return (q, r, s)
    
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
        x = ((4/3)*q - (2/3)*r - (2/3)*s) * TILE_WIDTH * 0.375
        y = (r - s) * TILE_HEIGHT * 0.5
        return x, y
    
    # function converts pixel_coords to hex_coords -------------------------- #
    def pixel_to_hex(x, y):
        q = (x / 2) / TILE_WIDTH * (8 / 3)
        r = (y / 2 - x / 4) / TILE_HEIGHT * 2
        s = -q-r
        return q, r, s
    
    # function return coords of neighboring hexes --------------------------- #
    def neighbors(q,r,s):
        nbors_lst = [(q+1,r,s-1), (q+1,r-1,s), (q,r-1,s+1), (q-1,r,s+1), (q-1,r+1,s), (q,r+1,s-1)]
        return nbors_lst
    
    # function returns distance from one hex to another --------------------- #
    def distance(obj_a, obj_b):
        q_diff = abs(obj_a.q - obj_b.q)
        r_diff = abs(obj_a.r - obj_b.r)
        s_diff = abs(obj_a.s - obj_b.s)
        ab_dist = max(q_diff, r_diff, s_diff)
        return ab_dist
    
    # function returns every hex within a distance from a hex --------------- #
    # hex_coords within range n of hex_center ------------------------------- #
    def in_range(obj, n):
        hex_in_range_lst = []
        for q in range(-n, n):
            for r in range(max(-n, -q-n), min(n, -q+n)):
                s = -q-r
                hex_in_range_lst.append((obj.q+q, obj.r+r, obj.s+s))
        return hex_in_range_lst
    
    # function draws a line from one hex to another converted to hexes ------ #
    def line_draw(obj_a, obj_b):
        ab_dist = HexLogic.distance(obj_a, obj_b)
        line_hexes_coords_lst = []
        for i in range(0, ab_dist):
            item = HexLogic.round_hex(HexLogic.cube_linint(obj_a, obj_b, 1.0/ab_dist * i))
            line_hexes_coords_lst.append(item)
        return line_hexes_coords_lst
    
    # distance from a hex, factoring in obstacles --------------------------- #
    def dist_lim_flood_fill(start_obj, moves, obj_lst, block_var):
        start =  (start_obj.q, start_obj.r, start_obj.s)
        visited = set() # set, so duplicate values are ignored
        visited.add(start)
        fringes = []
        fringes.append([start])
        
        print("Start coord: " + str(start))

        for k in range(1, moves + 1):
            fringes.append([])
            for t_coords in fringes[k-1]:
                for d in range(0,6): # 6 neighbors per hex => 6 items in nbors_lst
                    
                    neighbor = HexLogic.neighbors(t_coords[0], t_coords[1], t_coords[2])[d]
                    for obj in obj_lst:
                        if (obj.q, obj.r, obj.s) == t_coords:
                            blocked = getattr(obj, block_var)
                    if not blocked:
                        visited.add(t_coords)
                        fringes[k].append(neighbor)
                        print("Not blocked added to visited " + str(t_coords))

        return visited
    
    
    
    
    
    
    
    
    