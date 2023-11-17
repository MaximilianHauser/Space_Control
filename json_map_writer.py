# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 08:00:46 2022

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import json

# define map ---------------------------------------------------------------- #
# format is as follows: ----------------------------------------------------- #
# [terrain, unit, event_id (if unit is used as trigger)] -------------------- #
test_map = [
    
    [[None], [None], ["s", "r_cc"], ["s", None], ["s", None]],
    
    [[None], ["s", None], ["s", None], ["b", None], ["s", None]],
    
    [["s", None], ["a", None], ["b", None], ["a", None], ["s", None]],
    
    [["s", None], ["m", None], ["s", None], ["s", None], [None]],
    
    [["s", None], ["s", None], ["s", "b_cc", "100"], [None], [None]]
    
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
"""
The format for TRIGGER is as follows:
    condition_1 AND condition_2
    condition_1 OR condition_2
    
    Conditions need to be seperated by whitespace, more than one condition,
    need to be connected by AND or OR.
    
The format for a condition with TRIGGER is as follows:
    trigger_type:trigger_subject:specific_value
    
Valid trigger_types and trigger_subjects in relation:
    unit_blufor, unit_redfor: coordinates, health_rel, health_abs
    countdown: ticks, moves, rounds
    
Specific_value needs to be entered as Integer, Float or Set.

"""


battle_events = {
    
   "10" :
        {
            "TRIGGER":"countdown:ticks:20",
            "DESCRIPTION":"block player input for 15 seconds",
            "OCCURENCE":"block_input",
            "DONE":"countdown:ticks:25"
            },
   "100" :
        {
            "TRIGGER":"unit_blufor:coordinates:((4,2,-6),(4,1,-5))",
            "DESCRIPTION":"munition fired from (0,2,-2) to (4,2,-6), type nuclear torpedo",
            "OCCURENCE":"spawn_munition(r_nuclear_torpedo,0|2|-2,4|2|-6)",
            "DONE":"countdown:ticks:0"
            }
                    }


# creates json file and writes map to it ------------------------------------ #
with open('map.json', 'w') as file:
    json.dump(test_map, file)
 
# creates json file and writes map to it ------------------------------------ #
with open('battle_events.json', 'w') as file:
    json.dump(battle_events, file)
    
