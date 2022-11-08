# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:25:52 2022

@author: Maximilian
"""



# Tile attributes for specific terrain types -------------------------------- #
# space : s, micro-asteroids : m, asteroids : a, big asteroid : b ----------- #

t_dict = {
    "s":
        {
            "original_image" : "game.sprite_space",
            "dmg_to_light" : 0,
            "dmg_to_medium" : 0,
            "dmg_to_heavy" : 0,
            "block_move" : False,
            "block_sight" : False
            },
    "m":
        {
            "original_image" : "game.sprite_micro_roids",
            "dmg_to_light" : 0.25,
            "dmg_to_medium" : 0,
            "dmg_to_heavy" : 0,
            "block_move" : True,
            "block_sight" : True
            
            },
    "a":
        {
            "original_image" : "game.sprite_asteroids",
            "dmg_to_light" : 0,
            "dmg_to_medium" : 0.5,
            "dmg_to_heavy" : 0.05,
            "block_move" : True,
            "block_sight" : True
            
            },
    "b":
        {
            "original_image" : "game.sprite_big_roid",
            "dmg_to_light" : 0,
            "dmg_to_medium" : 0,
            "dmg_to_heavy" : 0,
            "block_move" : True,
            "block_sight" : True
            
            },
    }
