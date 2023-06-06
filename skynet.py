# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 18:46:34 2022

'AI' to handle enemy movement during battle

@author: Maximilian Hauser
"""



# import section ------------------------------------------------------------ #
import pygame as pg
import hexlogic as hl
import gamelogic as gl


# skynet class -------------------------------------------------------------- #
class Skynet:
    
    def __init__(self, game):
        
        self.game = game
        self.unit_set = set()
        
        spritegroup_lst = [self.game.unit_blufor_grp, self.game.unit_redfor_grp]
        for group in spritegroup_lst:
            for unit in group:
                self.unit_set.add(unit)
        
        # relative strength of forces --------------------------------------- #
        self.health_blufor = gl.get_group_attr_total_num("health", self.game.unit_blufor_grp)
        self.health_redfor = gl.get_group_attr_total_num("health", self.game.unit_redfor_grp)
        self.relative_health = round(self.health_blufor / self.health_redfor, 2)
        self.attack_blufor = gl.get_group_total_munition_dmg(self.game.unit_blufor_grp)
        self.attack_redfor = gl.get_group_total_munition_dmg(self.game.unit_redfor_grp)
        self.relative_attack = round(self.attack_blufor / self.attack_redfor, 2)
        self.num_blufor = len(self.game.unit_blufor_grp)
        self.num_redfor = len(self.game.unit_redfor_grp)
        self.relative_numbers = round(self.num_blufor / self.num_redfor, 2)
        # map objective ----------------------------------------------------- #
        self.map_objective = None
        self.obj_coords_a = None
        self.obj_coords_b = None
        
        # choke points between objectives ----------------------------------- #
        self.no_chokepoints_soft = 0
        self.no_chokepoints_hard = 0
        # units that cannot escape (%?) damage the next blue turn ----------- #
        self.commited_units = 0
        
        # relative positions of units (red_active, red, blue) --------------- #
        self.activated_red = None
        self.red_units = list()
        self.blu_units = list()

    # get the relative strength of red / blu -------------------------------- #
    def relative_strength(self):
        
        self.health_blufor = gl.get_group_attr_total_num("health", self.game.unit_blufor_grp)
        self.health_redfor = gl.get_group_attr_total_num("health", self.game.unit_redfor_grp)
        self.relative_health = round(self.health_blufor / self.health_redfor, 2)
        self.attack_blufor = gl.get_group_total_munition_dmg(self.game.unit_blufor_grp)
        self.attack_redfor = gl.get_group_total_munition_dmg(self.game.unit_redfor_grp)
        self.relative_attack = round(self.attack_blufor / self.attack_redfor, 2)
        self.num_blufor = len(self.game.unit_blufor_grp)
        self.num_redfor = len(self.game.unit_redfor_grp)
        self.relative_numbers = round(self.num_blufor / self.num_redfor, 2)
        
        self.relative_health = round(self.health_redfor / self.health_blufor, 2)
        self.relative_attack = round(self.attack_redfor / self.attack_blufor, 2)
        self.relative_numbers = round(self.num_redfor / self.num_blufor, 2)
        
    # get map objective ----------------------------------------------------- #
    def get_situation(self):
        self.activated_red = None
        
        for unit in self.unit_set:
            if unit.faction == "redfor":
                if unit.activated == True:
                    self.activated_red = unit
                    
        
        # set tactic based on situation ------------------------------------- #
        # time is favouring blufor ------------------------------------------ #
        if self.game.resolver.wc_roundslimit >= self.game.resolver.lc_roundslimit:
            # lc_dest_specific, lc_unit_at_coords --------------------------- #
            if self.game.resolver.lc_dest_specific or self.game.resolver.lc_unit_at_coords:
                return "attack_move"
            # lc_perc_dest_health, lc_perc_dest_dmgpt ----------------------- #
            elif self.game.resolver.lc_perc_dest_health or self.game.resolver.lc_perc_dest_dmgpt:
                return "attack_move"
        
        # time is favouring redfor ------------------------------------------ #
        else:
            # wc_dest_specific, wc_unit_at_coords --------------------------- #
            if self.game.resolver.wc_dest_specific or self.game.resolver.wc_unit_at_coords:
                return "hold_chokepoints"
            # wc_perc_dest_health, wc_perc_dest_dmgpt ----------------------- #
            elif self.game.resolver.wc_perc_dest_health or self.game.resolver.wc_perc_dest_dmgpt:
                return "delay"
        
        
    
    # get number of chokepoints --------------------------------------------- #
    def get_chokepoints(self):
        pass
    
    # get units commited to engagement -------------------------------------- #
    def get_commited_red(self):
        pass
        
