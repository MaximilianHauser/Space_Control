# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:41:16 2022

Contains a dictionary with all type specific unit attributes.

@author: Maximilian Hauser
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
            "faction" : '"blufor"',
            
            "max_health" : 24,
            "health" : 24,
            "armor" : 18,
            "initiative" : 8,
            "ciws_dmg" : 20,
            "ciws_range" : 2,
            "starting_ciws_charge" : 8,
            "ciws_charge" : 8,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "b_light_coilgun": 99,
            "b_medium_coilgun": 0,
            "b_heavy_coilgun": 36,
            "b_spinalmount_coilgun": 0,
            "b_conventional_missile": 0,
            "b_shapedcharge_missile": 0,
            "b_conventional_torpedo": 8,
            "b_shapedcharge_torpedo": 8,
            "b_nuclear_torpedo": 8,
            "b_shapednuclear_torpedo": 8
                }
            },
        
    "b_bc":
        {
            "image" : "game.sprite_blufor_BC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            "faction" : '"blufor"',
            
            "max_health" : 20,
            "health" : 20,
            "armor" : 20,
            "initiative" : 7,
            "ciws_dmg" : 14,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "b_light_coilgun": 99,
            "b_medium_coilgun": 0,
            "b_heavy_coilgun": 36,
            "b_spinalmount_coilgun": 24,
            "b_conventional_missile": 0,
            "b_shapedcharge_missile": 0,
            "b_conventional_torpedo": 2,
            "b_shapedcharge_torpedo": 2,
            "b_nuclear_torpedo": 2,
            "b_shapednuclear_torpedo": 2
                }
            },
        
    "b_ac":
        {
            "image" : "game.sprite_blufor_AC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            "faction" : '"blufor"',
            
            "max_health" : 12,
            "health" : 12,
            "armor" : 10,
            "initiative" : 6,
            "ciws_dmg" : 12,
            "ciws_range" : 1,
            "starting_ciws_charge" : 4,
            "ciws_charge" : 4,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "b_light_coilgun": 99,
            "b_medium_coilgun": 32,
            "b_heavy_coilgun": 0,
            "b_spinalmount_coilgun": 0,
            "b_conventional_missile": 0,
            "b_shapedcharge_missile": 0,
            "b_conventional_torpedo": 2,
            "b_shapedcharge_torpedo": 2,
            "b_nuclear_torpedo": 2,
            "b_shapednuclear_torpedo": 2
                }
            },
        
    "b_dd":
        {
            "image" : "game.sprite_blufor_DD",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            "faction" : '"blufor"',
            
            "max_health" : 10,
            "health" : 10,
            "armor" : 10,
            "initiative" : 5,
            "ciws_dmg" : 6,
            "ciws_range" : 1,
            "starting_ciws_charge" : 4,
            "ciws_charge" : 4,
            "evasion": 0.15,
            "starting_ap" : 2,
            "action_points" : 2,
            
            "ammunition" : {
            "b_light_coilgun": 99,
            "b_medium_coilgun": 16,
            "b_heavy_coilgun": 12,
            "b_spinalmount_coilgun": 0,
            "b_conventional_missile": 2,
            "b_shapedcharge_missile": 2,
            "b_conventional_torpedo": 2,
            "b_shapedcharge_torpedo": 2,
            "b_nuclear_torpedo": 0,
            "b_shapednuclear_torpedo": 0
                }
            },
        
    "b_ff":
        {
            "image" : "game.sprite_blufor_FF",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            "faction" : '"blufor"',
            
            "max_health" : 8,
            "health" : 8,
            "armor" : 8,
            "initiative" : 6,
            "ciws_dmg" : 10,
            "ciws_range" : 2,
            "starting_ciws_charge" : 6,
            "ciws_charge" : 6,
            "evasion": 0.15,
            "starting_ap" : 2,
            "action_points" : 2,
            
            "ammunition" : {
            "b_light_coilgun": 99,
            "b_medium_coilgun": 16,
            "b_heavy_coilgun": 0,
            "b_spinalmount_coilgun": 0,
            "b_conventional_missile": 4,
            "b_shapedcharge_missile": 12,
            "b_conventional_torpedo": 2,
            "b_shapedcharge_torpedo": 2,
            "b_nuclear_torpedo": 0,
            "b_shapednuclear_torpedo": 0
                }
            },
        
    "b_cv":
        {
            "image" : "game.sprite_blufor_CV",
            "ship_size_light" : True,
            "ship_size_medium" : False,
            "ship_size_heavy" : False,
            "faction" : '"blufor"',
            
            "max_health" : 6,
            "health" : 6,
            "armor" : 4,
            "initiative" : 3,
            "ciws_dmg" : 2,
            "ciws_range" : 1,
            "starting_ciws_charge" : 3,
            "ciws_charge" : 3,
            "evasion": 0.35,
            "starting_ap" : 5,
            "action_points" : 5,
            
            "ammunition" : {
            "b_light_coilgun": 99,
            "b_medium_coilgun": 12,
            "b_heavy_coilgun": 0,
            "b_spinalmount_coilgun": 0,
            "b_conventional_missile": 6,
            "b_shapedcharge_missile": 6,
            "b_conventional_torpedo": 0,
            "b_shapedcharge_torpedo": 0,
            "b_nuclear_torpedo": 0,
            "b_shapednuclear_torpedo": 0
                }
            },
        
    "b_gs":
        {
            "image" : "game.sprite_blufor_GS",
            "ship_size_light" : True,
            "ship_size_medium" : False,
            "ship_size_heavy" : False,
            "faction" : '"blufor"',
            
            "max_health" : 4,
            "health" : 4,
            "armor" : 8,
            "initiative" : 2,
            "ciws_dmg" : 1,
            "ciws_range" : 0,
            "starting_ciws_charge" : 2,
            "ciws_charge" : 2,
            "evasion": 0.25,
            "starting_ap" : 4,
            "action_points" : 4,
            
            "ammunition" : {
            "b_light_coilgun": 99,
            "b_medium_coilgun": 0,
            "b_heavy_coilgun": 16,
            "b_spinalmount_coilgun": 0,
            "b_conventional_missile": 0,
            "b_shapedcharge_missile": 0,
            "b_conventional_torpedo": 0,
            "b_shapedcharge_torpedo": 0,
            "b_nuclear_torpedo": 0,
            "b_shapednuclear_torpedo": 0
                }
            },
        
    "b_tt":
        {
            "image" : "game.sprite_blufor_TT",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            "faction" : '"blufor"',
            
            "max_health" : 6,
            "health" : 6,
            "armor" : 2,
            "initiative" : 2,
            "ciws_dmg" : 1,
            "ciws_range" : 0,
            "starting_ciws_charge" : 1,
            "ciws_charge" : 1,
            "evasion": 0.2,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "b_light_coilgun": 99,
            "b_medium_coilgun": 0,
            "b_heavy_coilgun": 0,
            "b_spinalmount_coilgun": 0,
            "b_conventional_missile": 0,
            "b_shapedcharge_missile": 0,
            "b_conventional_torpedo": 0,
            "b_shapedcharge_torpedo": 0,
            "b_nuclear_torpedo": 0,
            "b_shapednuclear_torpedo": 0
                }
            },
        
    # REDFOR ships ---------------------------------------------------------- #
 
    "r_cc":
        {
            "image" : "game.sprite_redfor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            "faction" : '"redfor"',
            
            "max_health" : 10,
            "health" : 10,
            "armor" : 1,
            "initiative" : 7,
            "ciws_dmg" : 1,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "r_light_plasma": 2,
            "r_medium_plasma": 1,
            "r_heavy_plasma": 3,
            "r_spinalmount_plasma": 1,
            "r_conventional_missile": 2,
            "r_shapedcharge_missile": 3,
            "r_conventional_torpedo": 1,
            "r_shapedcharge_torpedo": 1,
            "r_nuclear_torpedo": 2,
            "r_shapednuclear_torpedo": 1
                }
            },
        
    "r_bc":
        {
            "image" : "game.sprite_redfor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            "faction" : '"redfor"',
            
            "max_health" : 8,
            "health" : 8,
            "armor" : 1,
            "initiative" : 6,
            "ciws_dmg" : 14,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "r_light_plasma": 2,
            "r_medium_plasma": 1,
            "r_heavy_plasma": 3,
            "r_spinalmount_plasma": 1,
            "r_conventional_missile": 2,
            "r_shapedcharge_missile": 3,
            "r_conventional_torpedo": 1,
            "r_shapedcharge_torpedo": 1,
            "r_nuclear_torpedo": 2,
            "r_shapednuclear_torpedo": 1
                }
            },
        
    "r_ac":
        {
            "image" : "game.sprite_redfor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : False,
            "ship_size_heavy" : True,
            "faction" : '"redfor"',
            
            "max_health" : 6,
            "health" : 6,
            "armor" : 1,
            "initiative" : 5,
            "ciws_dmg" : 14,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "r_light_plasma": 2,
            "r_medium_plasma": 1,
            "r_heavy_plasma": 3,
            "r_spinalmount_plasma": 1,
            "r_conventional_missile": 2,
            "r_shapedcharge_missile": 3,
            "r_conventional_torpedo": 1,
            "r_shapedcharge_torpedo": 1,
            "r_nuclear_torpedo": 2,
            "r_shapednuclear_torpedo": 1
                }
            },
        
    "r_dd":
        {
            "image" : "game.sprite_redfor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            "faction" : '"redfor"',
            
            "max_health" : 5,
            "health" : 5,
            "armor" : 1,
            "initiative" : 4,
            "ciws_dmg" : 14,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "r_light_plasma": 2,
            "r_medium_plasma": 1,
            "r_heavy_plasma": 3,
            "r_spinalmount_plasma": 1,
            "r_conventional_missile": 2,
            "r_shapedcharge_missile": 3,
            "r_conventional_torpedo": 1,
            "r_shapedcharge_torpedo": 1,
            "r_nuclear_torpedo": 2,
            "r_shapednuclear_torpedo": 1
                }
            },
        
    "r_ff":
        {
            "image" : "game.sprite_redfor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            "faction" : '"redfor"',
            
            "max_health" : 4,
            "health" : 4,
            "armor" : 1,
            "initiative" : 5,
            "ciws_dmg" : 14,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "r_light_plasma": 2,
            "r_medium_plasma": 1,
            "r_heavy_plasma": 3,
            "r_spinalmount_plasma": 1,
            "r_conventional_missile": 2,
            "r_shapedcharge_missile": 3,
            "r_conventional_torpedo": 1,
            "r_shapedcharge_torpedo": 1,
            "r_nuclear_torpedo": 2,
            "r_shapednuclear_torpedo": 1
                }
            },
        
    "r_cv":
        {
            "image" : "game.sprite_redfor_CC",
            "ship_size_light" : True,
            "ship_size_medium" : False,
            "ship_size_heavy" : False,
            "faction" : '"redfor"',
            
            "max_health" : 3,
            "health" : 3,
            "armor" : 1,
            "initiative" : 2,
            "ciws_dmg" : 14,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "r_light_plasma": 2,
            "r_medium_plasma": 1,
            "r_heavy_plasma": 3,
            "r_spinalmount_plasma": 1,
            "r_conventional_missile": 2,
            "r_shapedcharge_missile": 3,
            "r_conventional_torpedo": 1,
            "r_shapedcharge_torpedo": 1,
            "r_nuclear_torpedo": 2,
            "r_shapednuclear_torpedo": 1
                }
            },
        
    "r_gs":
        {
            "image" : "game.sprite_redfor_CC",
            "ship_size_light" : True,
            "ship_size_medium" : False,
            "ship_size_heavy" : False,
            "faction" : '"redfor"',
            
            "max_health" : 2,
            "health" : 2,
            "armor" : 1,
            "initiative" : 1,
            "ciws_dmg" : 14,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "r_light_plasma": 2,
            "r_medium_plasma": 1,
            "r_heavy_plasma": 3,
            "r_spinalmount_plasma": 1,
            "r_conventional_missile": 2,
            "r_shapedcharge_missile": 3,
            "r_conventional_torpedo": 1,
            "r_shapedcharge_torpedo": 1,
            "r_nuclear_torpedo": 2,
            "r_shapednuclear_torpedo": 1
                }
            },
        
    "r_tt":
        {
            "image" : "game.sprite_redfor_CC",
            "ship_size_light" : False,
            "ship_size_medium" : True,
            "ship_size_heavy" : False,
            "faction" : '"redfor"',
            
            "max_health" : 3,
            "health" : 3,
            "armor" : 1,
            "initiative" : 1,
            "ciws_dmg" : 14,
            "ciws_range" : 2,
            "starting_ciws_charge" : 5,
            "ciws_charge" : 5,
            "evasion": 0,
            "starting_ap" : 1,
            "action_points" : 1,
            
            "ammunition" : {
            "r_light_plasma": 2,
            "r_medium_plasma": 1,
            "r_heavy_plasma": 3,
            "r_spinalmount_plasma": 1,
            "r_conventional_missile": 2,
            "r_shapedcharge_missile": 3,
            "r_conventional_torpedo": 1,
            "r_shapedcharge_torpedo": 1,
            "r_nuclear_torpedo": 2,
            "r_shapednuclear_torpedo": 1
                }
            }
    
    }
