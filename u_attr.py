# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:41:16 2022

@author: Maximilian
"""



# Unit attributes for specific unit types ----------------------------------- #
# b : blufor, r : redfor ---------------------------------------------------- #
# cc : command cruiser ------------------------------------------------------ #
# bc : battle cruiser ------------------------------------------------------- #
# ac : assault carrier ------------------------------------------------------ #
# dd : destroyer ------------------------------------------------------------ #
# ff : frigate -------------------------------------------------------------- #
# cv : corvette ------------------------------------------------------------- #
# gs : gunship -------------------------------------------------------------- #
# tt : tender --------------------------------------------------------------- #

u_dict = {
 
    # BLUFOR ships ---------------------------------------------------------- #
 
    "b_cc":
        {
            "image" : "game.sprite_blufor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            
            "max_health" : 10,
            "health" : 10,
            "dmg_per_shot" : 6,
            "starting_ap" : 2,
            "action_points" : 2,
            },
        
    "b_bc":
        {
            "image" : "game.sprite_blufor_BC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            
            "max_health" : 8,
            "health" : 8,
            "dmg_per_shot" : 6,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "b_ac":
        {
            "image" : "game.sprite_blufor_AC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            
            "max_health" : 6,
            "health" : 6,
            "dmg_per_shot" : 1,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "b_dd":
        {
            "image" : "game.sprite_blufor_DD",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            
            "max_health" : 5,
            "health" : 5,
            "dmg_per_shot" : 3,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "b_ff":
        {
            "image" : "game.sprite_blufor_FF",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            
            "max_health" : 4,
            "health" : 4,
            "dmg_per_shot" : 2,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "b_cv":
        {
            "image" : "game.sprite_blufor_CC",
            "ship_size_light" : True,
            "ship_size_medium" : False,
            "ship_size_heavy" : False,
            
            "max_health" : 3,
            "health" : 3,
            "dmg_per_shot" : 2,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "b_gs":
        {
            "image" : "game.sprite_blufor_GS",
            "ship_size_light" : True,  # adjust ship size for armor?
            "ship_size_medium" : False,
            "ship_size_heavy" : False,
            
            "max_health" : 2,
            "health" : 2,
            "dmg_per_shot" : 3,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "b_tt":
        {
            "image" : "game.sprite_blufor_TT",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            
            "max_health" : 3,
            "health" : 3,
            "dmg_per_shot" : 0,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    # REDFOR ships ---------------------------------------------------------- #
 
    "r_cc":
        {
            "image" : "game.sprite_blufor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            
            "max_health" : 10,
            "health" : 10,
            "dmg_per_shot" : 6,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "r_bc":
        {
            "image" : "game.sprite_blufor_BC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            
            "max_health" : 8,
            "health" : 8,
            "dmg_per_shot" : 6,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "r_ac":
        {
            "image" : "game.sprite_blufor_AC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            
            "max_health" : 6,
            "health" : 6,
            "dmg_per_shot" : 1,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "r_dd":
        {
            "image" : "game.sprite_blufor_DD",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            
            "max_health" : 5,
            "health" : 5,
            "dmg_per_shot" : 3,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "r_ff":
        {
            "image" : "game.sprite_blufor_FF",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            
            "max_health" : 4,
            "health" : 4,
            "dmg_per_shot" : 2,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "r_cv":
        {
            "image" : "game.sprite_blufor_CC",
            "ship_size_light" : True,
            "ship_size_medium" : False,
            "ship_size_heavy" : False,
            
            "max_health" : 3,
            "health" : 3,
            "dmg_per_shot" : 2,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "r_gs":
        {
            "image" : "game.sprite_blufor_GS",
            "ship_size_light" : True,  # adjust ship size for armor?
            "ship_size_medium" : False,
            "ship_size_heavy" : False,
            
            "max_health" : 2,
            "health" : 2,
            "dmg_per_shot" : 3,
            "starting_ap" : 1,
            "action_points" : 1,
            },
        
    "r_tt":
        {
            "image" : "game.sprite_blufor_TT",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            
            "max_health" : 3,
            "health" : 3,
            "dmg_per_shot" : 0,
            "starting_ap" : 1,
            "action_points" : 1,
            }
    
    }
