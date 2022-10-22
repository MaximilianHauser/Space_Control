# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:49:27 2022

will handle game logic, meaning interactions between units in game and tile attributes, etc.

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
from hexlogic import HexLogic as hl




# class responsible for handling game logic specifics ----------------------- #
class GameLogic:
    
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
    def unit_move():
        pass
    



