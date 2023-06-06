# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 09:57:16 2022

checks if conditions for victory or defeat are met

win_conditions : [turns, blue_unit_reaches_coords(specific, one, multiple), redfor_looses_units(all, %, specific)]
loss_conditions : [turns, red_unit_reaches_coords(specific, one, multiple), redfor_looses_units(all, %, specific)]

@author: Maximilian
"""


# import section ------------------------------------------------------------ #
import gamelogic as gl


# ResolveBattleLogic class -------------------------------------------------- #
class ResolveBattleLogic:
    
    def __init__(self, game, **kwargs):
        
        self.game = game
        
        # wc/lc based on turn limit ----------------------------------------- #
        self.wc_roundslimit = False
        self.lc_roundslimit = True
        # wc/lc based on total health of units ------------------------------ #
        self.wc_perc_dest_health = True
        self.lc_perc_dest_health = False
        # wc/lc based on total max dmg per turn of all units ---------------- #
        self.wc_perc_dest_dmgpt = False
        self.lc_perc_dest_dmgpt = False
        # wc/lc based on specific unit or units ----------------------------- #
        self.wc_dest_specific = False
        self.lc_dest_specific = False
        # wc/lc based on a specific unit reaching a coordinate -------------- #
        self.wc_unit_at_coords = False
        self.lc_unit_at_coords = False
        
        # values wc/lc are based on, on init -------------------------------- #
        # turn number on init ----------------------------------------------- #
        self.turn_limit_blufor = 12
        self.turn_limit_redfor = 999
        
        # total health of units values on init ------------------------------ #
        self.starting_health_blufor = 1
        self.health_blufor = self.starting_health_blufor
        self.blufor_dest_perc = 0
        
        self.starting_health_redfor = 1
        self.health_redfor = self.starting_health_redfor
        self.redfor_dest_perc = 0
        
        # total attack of units values on init ------------------------------ #
        self.starting_dmgpt_blufor = 1
        self.dmgpt_blufor = self.starting_dmgpt_blufor
        self.blufor_crip_perc = 0
        
        self.starting_dmgpt_redfor = 1
        self.dmgpt_redfor = self.starting_dmgpt_redfor
        self.redfor_crip_perc = 0
        
        # lists of specific units to be destroyed for wc/lc ----------------- #
        self.gravity_units_blu = list()
        self.gravity_units_red = list()
        
        # lists of specific units to reach lists of coords for wc/lc -------- #
        self.gravity_units_blu = list()
        self.release_points_blu = list()
        self.gravity_units_red = list()
        self.release_points_red = list()
        
    def update_gamestatus(self):
        # update values from game and sprites ------------------------------- #
        self.health_blufor = gl.get_group_attr_total_num("health", self.game.unit_blufor_grp)
        self.health_redfor = gl.get_group_attr_total_num("health", self.game.unit_redfor_grp)
        
        # check wc/lc and return game status -------------------------------- #
        if self.wc_roundslimit:
            if self.game.round_counter > self.turn_limit_redfor:
                return "victory"
        
        if self.lc_roundslimit:
            if self.game.round_counter > self.turn_limit_blufor:
                return "defeat"
            
        if self.wc_perc_dest_health:
            if self.health_redfor / self.starting_health_redfor <= self.redfor_dest_perc:
                return "victory"
        
        if self.lc_perc_dest_health:
            if self.health_blufor / self.starting_health_blufor <= self.blufor_dest_perc:
                return "victory"
        
        if self.wc_perc_dest_dmgpt:
            if self.dmgpt_redfor / self.starting_dmgpt_redfor <= self.redfor_crip_perc:
                return "victory"
        
        if self.lc_perc_dest_dmgpt:
            if self.dmgpt_blufor / self.starting_dmgpt_blufor <= self.blufor_crip_perc:
                return "defeat"
        
        if self.wc_dest_specific:
            pass
        
        if self.lc_dest_specific:
            pass
        
        if self.wc_unit_at_coords:
            pass
        
        if self.lc_unit_at_coords:
            pass
        
        return "ongoing"

