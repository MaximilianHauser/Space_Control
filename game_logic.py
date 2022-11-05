# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:49:27 2022

will handle game logic, meaning interactions between units in game and tile attributes, etc.

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
from hexlogic import HexLogic as hl
from settings import WIN_WIDTH, WIN_HEIGHT


# class responsible for handling game logic specifics ----------------------- #
class GameLogic:
    
    # get the max or min value along an axis from a tile -------------------- #
    # max_x = right map border, min_x = left map border --------------------- #
    # max_y = bottom map border, min_y = top map border --------------------- #
    def get_map_borders(tile_grp):
        max_x = 0
        min_x = WIN_WIDTH
        max_y = 0
        min_y = WIN_HEIGHT
        
        for tile in tile_grp:
            if tile.x > max_x:
                max_x = tile.x
            if tile.x < min_x:
                min_x = tile.x
            if tile.y > max_y:
                max_y = tile.y
            if tile.y < min_y:
                min_y = tile.y
                
        return max_x, min_x, max_y, min_y
    
    # function determines, wether or not a unit is on the tile -------------- #
    # and if there is, assigns the unit as attribute to the tile ------------ #
    def tile_has_unit(tile, unit_sprite_groups_lst):
        on_tile = None
        for group in unit_sprite_groups_lst:
            for unit in group:
                if unit.q == tile.q:
                    if unit.r == tile.r:
                        if unit.s == tile.s:
                            on_tile = unit
                            
        return on_tile
    
    
    # function determines, if there currently is an activated blufor_unit --- #
    # and if yes, returns it ------------------------------------------------ #
    def is_activated_unit(unit_blufor_grp):
        activated_unit = None
        for unit in unit_blufor_grp:
            if unit.activated:
                activated_unit = unit
        return activated_unit
    
    
    
    # function determines, wether or not tile is within movement range ------ #
    # of an activated blufor unit ------------------------------------------- #
    def in_mov_range(tile, blufor_grp, tile_grp, block_var):
        in_range = False
        
        # determine variables for dist_lim_flood_fill ----------------------- #
        start_obj = GameLogic.is_activated_unit(blufor_grp)
        moves = start_obj.action_points
        obj_lst = tile_grp
        
        # returns list of coords within movement range ---------------------- #
        visited = hl.dist_lim_flood_fill(start_obj, moves, obj_lst, block_var)
        visited.remove((start_obj.q, start_obj.r, start_obj.s))
        
        # check if tile was visited in floodfil ----------------------------- #
        if hl.get_qrs(tile) in visited:
            in_range = True
        
        return in_range
    
    
    
    # handles unit movement, subtraction of action points ------------------- #
    def move_unit(clicked_tile, unit_on_tile):
        distance_movement = hl.distance(unit_on_tile, clicked_tile)
        hl.set_qrs(unit_on_tile, clicked_tile.q, clicked_tile.r, clicked_tile.s)
        unit_on_tile.action_points -= distance_movement
    

    

