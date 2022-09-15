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
    "b_cc":
        {
            "image" : "game.sprite_blufor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            
            "max_health" : 10,
            "health" : 10,
            "dmg_per_shot" : 10,
            "starting_ap" : 1,
            "action_points" : 1,
            }
    
    }
