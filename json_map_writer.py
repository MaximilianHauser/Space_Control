# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 08:00:46 2022

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import json

# define map ---------------------------------------------------------------- #
# format is as follows: ----------------------------------------------------- #
# [terrain, unit] ----------------------------------------------------------- #
test_map = [
    
    [[None], [None], ["s", "r_cc"], ["s", None], ["s", None]],
    
    [[None], ["s", None], ["s", None], ["b", None], ["s", None]],
    
    [["s", None], ["a", None], ["b", None], ["a", None], ["s", None]],
    
    [["s", None], ["m", None], ["s", None], ["s", None], [None]],
    
    [["s", None], ["s", None], ["s", "b_cc"], [None], [None]]
    
            ]

# set victory conditons ----------------------------------------------------- #
victory_conditions_dict = {
# wc/lc grouping ------------------------------------------------------------ #
# within group is AND, otherwise OR ----------------------------------------- #
"c_groups":None,
# wc/lc based on turn limit ----------------------------------------- #
"wc_roundslimit" : None,
"lc_roundslimit" : None,
# wc/lc based on total health of units ------------------------------ #
"wc_perc_dest_health" : None,
"lc_perc_dest_health" : None,
# wc/lc based on total max dmg per turn of all units ---------------- #
"wc_perc_dest_dmgpt" : None,
"lc_perc_dest_dmgpt" : None,
# wc/lc based on specific unit or units ----------------------------- #
"wc_dest_specific" : None,
"lc_dest_specific" : None,
# wc/lc based on a specific unit reaching a coordinate -------------- #
"wc_unit_at_coords" : None,
"lc_unit_at_coords" : None
}


# set mission stages and events --------------------------------------------- #
mission_stage_dict = {
    
}


# creates json file and writes map to it ------------------------------------ #
with open('map.json', 'w') as file:
    json.dump(test_map, file)
    
file.close()