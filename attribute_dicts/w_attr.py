# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 20:31:19 2023

Contains a dictionary with all type specific weapon attributes.

@author: Maximilian Hauser
"""


# Weapon attributes for specific weapons ------------------------------------ #
# b : blufor, r : redfor ---------------------------------------------------- #

w_dict = {
 
    # BLUFOR weapons -------------------------------------------------------- #
 
    "b_light_coilgun":
        {
            "type": "projectile",
            "max_range": 3,
            "min_range": 0,
            "armor": 2,
            "dmg": 2,
            "dmg_multiplier": 1
            },
        
    "b_medium_coilgun":
        {
            "type": "projectile",
            "max_range": 4,
            "min_range": 0,
            "armor": 4,
            "dmg": 4,
            "dmg_multiplier": 1
            },
        
    "b_heavy_coilgun":
        {
            "type": "projectile",
            "max_range": 5,
            "min_range": 0,
            "armor": 10,
            "dmg": 10,
            "dmg_multiplier": 1
            },
        
    "b_spinalmount_coilgun":
        {
            "type": "projectile",
            "max_range": 8,
            "min_range": 0,
            "armor": 22,
            "dmg": 22,
            "dmg_multiplier": 2
            },
        
    "b_conventional_missile":
        {
            "type": "guided",
            "max_range": 6,
            "min_range": 0,
            "armor": 1,
            "dmg": 2,
            "dmg_multiplier": 3
            },
        
    "b_shapedcharge_missile":
        {
            "type": "guided",
            "max_range": 6,
            "min_range": 0,
            "armor": 1,
            "dmg": 4,
            "dmg_multiplier": 1
            },
        
    "b_conventional_torpedo":
        {
            "type": "guided",
            "max_range": 8,
            "min_range": 0,
            "armor": 1,
            "dmg": 4,
            "dmg_multiplier": 2
            },
        
    "b_shapedcharge_torpedo":
        {
            "type": "guided",
            "max_range": 8,
            "min_range": 0,
            "armor": 1,
            "dmg": 6,
            "dmg_multiplier": 1
            },
        
    "b_nuclear_torpedo":
        {
            "type": "guided",
            "max_range": 8,
            "min_range": 0,
            "armor": 1,
            "dmg": 30,
            "dmg_multiplier": 3
            },
        
    "b_shapednuclear_torpedo":
        {
            "type": "guided",
            "max_range": 8,
            "min_range": 0,
            "armor": 1,
            "dmg": 40,
            "dmg_multiplier": 1
            },
     
    # REDFOR weapons -------------------------------------------------------- #
    
    "r_light_plasma":
        {
            "type": "projectile",
            "max_range": 2,
            "min_range": 0,
            "armor": 99,
            "dmg": 2,
            "dmg_multiplier": 1
            },
        
    "r_medium_plasma":
        {
            "type": "projectile",
            "max_range": 3,
            "min_range": 0,
            "armor": 99,
            "dmg": 3,
            "dmg_multiplier": 1
            },
        
    "r_heavy_plasma":
        {
            "type": "projectile",
            "max_range": 4,
            "min_range": 0,
            "armor": 99,
            "dmg": 8,
            "dmg_multiplier": 1
            },
        
    "r_spinalmount_plasma":
        {
            "type": "projectile",
            "max_range": 6,
            "min_range": 0,
            "armor": 99,
            "dmg": 16,
            "dmg_multiplier": 1
            },
        
    "r_conventional_missile":
        {
            "type": "guided",
            "max_range": 5,
            "min_range": 0,
            "armor": 1,
            "dmg": 2,
            "dmg_multiplier": 3
            },
        
    "r_shapedcharge_missile":
        {
            "type": "guided",
            "max_range": 5,
            "min_range": 0,
            "armor": 1,
            "dmg": 4,
            "dmg_multiplier": 1
            },
        
    "r_conventional_torpedo":
        {
            "type": "guided",
            "max_range": 7,
            "min_range": 0,
            "armor": 1,
            "dmg": 4,
            "dmg_multiplier": 3
            },
        
    "r_shapedcharge_torpedo":
        {
            "type": "guided",
            "max_range": 7,
            "min_range": 0,
            "armor": 1,
            "dmg": 6,
            "dmg_multiplier": 1
            },
        
    "r_nuclear_torpedo":
        {
            "type": "guided",
            "max_range": 7,
            "min_range": 0,
            "armor": 1,
            "dmg": 30,
            "dmg_multiplier": 3
            },
        
    "r_shapednuclear_torpedo":
        {
            "type": "guided",
            "max_range": 7,
            "min_range": 0,
            "armor": 1,
            "dmg": 40,
            "dmg_multiplier": 1
            }
        }

    