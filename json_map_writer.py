# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 08:00:46 2022

@author: Maximilian Hauser
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
# wc/lc based on turn limit ------------------------------------------------- #
"wc_roundslimit" : None,
"lc_roundslimit" : None,
# wc/lc based on total health of units -------------------------------------- #
"wc_perc_dest_health" : None,
"lc_perc_dest_health" : None,
# wc/lc based on total max dmg per turn of all units ------------------------ #
"wc_perc_dest_dmgpt" : None,
"lc_perc_dest_dmgpt" : None,
# wc/lc based on specific unit or units ------------------------------------- #
"wc_dest_specific" : None,
"lc_dest_specific" : None,
# wc/lc based on a specific unit reaching a coordinate ---------------------- #
"wc_unit_at_coords" : None,
"lc_unit_at_coords" : None
}


# battle events organized as follows: --------------------------------------- #
# ID : { TRIGGER, TRIGGER_END, DESCRIPTION, OCCURENCES } -------------------- #
battle_events = {
    
    10 :
        {
            "TRIGGER":"start_map",
            "TRIGGER_END":None,
            "DESCRIPTION":"block player input for 15 seconds",
            "OCCURENCE":"block_input, 15000",
            "DONE":False
            },
    100 :
        {
            "TRIGGER":"unit_blufor, r<4 OR s>-6",
            "TRIGGER_END":"turns, 3",
            "DESCRIPTION":"munition from outside map travels to (0,0,0), (-1,1,0), (0,1,-1), (1,0,-1)",
            "OCCURENCE":"block_input, 15000",
            "DONE":False
            }
                    }


# creates json file and writes map to it ------------------------------------ #
with open('map.json', 'w') as file:
    json.dump(test_map, file)
 
# creates json file and writes map to it ------------------------------------ #
with open('battle_events.json', 'w') as file:
    json.dump(battle_events, file)
    
