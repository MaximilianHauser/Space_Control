# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:25:52 2022

Contains a dictionary with all type specific terrain attributes.

@author: Maximilian Hauser
"""



# Tile attributes for specific terrain types -------------------------------- #
# space : s, micro-asteroids : m, asteroids : a, big asteroid : b ----------- #

t_dict = {
    "s":
        {
            "original_image" : "manager.sprite_space",
            "movement_cost" : 1,
            "dmg_to_light" : 0,
            "dmg_to_medium" : 0,
            "dmg_to_heavy" : 0,
            "perc_to_negate" : 0,
            "block_sight" : False,
            "animation_state" : None
            
            },
    "m":
        {
            "original_image" : "manager.sprite_micro_roids",
            "movement_cost" : 1,
            "dmg_to_light" : 0.25,
            "dmg_to_medium" : 0,
            "dmg_to_heavy" : 0,
            "perc_to_negate" : 0.25,
            "block_sight" : True,
            "animation_state" : None
            
            },
    "a":
        {
            "original_image" : "manager.sprite_asteroids",
            "movement_cost" : 0,
            "dmg_to_light" : 0,
            "dmg_to_medium" : 0.5,
            "dmg_to_heavy" : 0.05,
            "perc_to_negate" : 0.5,
            "block_sight" : True,
            "animation_state" : None
            
            },
    "b":
        {
            "original_image" : "manager.sprite_big_roid",
            "movement_cost" : 0,
            "dmg_to_light" : 0,
            "dmg_to_medium" : 0,
            "dmg_to_heavy" : 0,
            "perc_to_negate" : 1,
            "block_sight" : True,
            "animation_state" : None
            
            },
    }
