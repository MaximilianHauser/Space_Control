# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:54:56 2022

will contain animation logic

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from hexlogic import HexLogic as hl
from game_logic import GameLogic as gl


# Animations class contains animation functions ----------------------------- #
class Animations:
    
    # tinting a sprite in a certain colorshade ------------------------------ #
    def tint_image(image, color):
        colored_image = pg.Surface(image.get_size())
        colored_image.fill(color)
        
        tinted_image = image.copy()
        
        tinted_image.blit(colored_image, (0, 0), special_flags = pg.BLEND_MULT)
        colorkey = tinted_image.get_at((0,0))
        tinted_image.set_colorkey(colorkey)
        
        return tinted_image
    
    # set animation_state for tiles ----------------------------------------- #
    def set_animation_state_tiles(tile_grp, unit_sprite_groups_lst):
        
        activated_unit = None
        for units_grp in unit_sprite_groups_lst:
            for unit in units_grp:
                if unit.activated == True:
                    activated_unit = unit
        
        if activated_unit is not None and activated_unit.faction == "blufor":
            
        # limit potentially affected tiles ---------------------------------- #        
            for tile in tile_grp:

                distance_to_activated = hl.distance(activated_unit, tile)
                active_unit_reach = activated_unit.action_points - 1 + gl.get_max_weapon_range(activated_unit)
                
                if distance_to_activated <= active_unit_reach:
                    if tile.unit != None:
                        if tile.unit.activated is True:
                            tile.animation_state = "activated_unit_on_tile" 
                        elif tile.unit.faction == "redfor":
                            if tile.fog_of_war is False:
                                tile.animation_state = "enemy_unit_in_range"
                            elif tile.fog_of_war is True and gl.in_mov_range(tile, activated_unit, tile_grp, "block_move"):
                                tile.animation_state = "in_movement_range"
                            else:
                                tile.animation_state = None     
                        else:
                            tile.animation_state = None     
                    elif gl.in_mov_range(tile, activated_unit, tile_grp, "block_move"):
                        tile.animation_state = "in_movement_range"
                    else:
                        tile.animation_state = None     
                else:
                    tile.animation_state = None
        else:
            for tile in tile_grp:
                tile.animation_state = None




