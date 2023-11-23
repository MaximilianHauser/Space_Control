# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 18:46:34 2022

'AI' to handle enemy movement during battle

@author: Maximilian Hauser
"""



# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import pygame as pg
import math
from collections import Counter

# custom functions ---------------------------------------------------------- #
import hexlogic as hl
import gamelogic as gl

# sprite objects ------------------------------------------------------------ #
from munition import Munition


# skynet class -------------------------------------------------------------- #
class Skynet:
    
    def __init__(self, manager):
        
        self.manager = manager
        self.unit_set = set()
        
        spritegroup_lst = [manager.unit_blufor_group, manager.unit_redfor_group]
        for group in spritegroup_lst:
            for unit in group:
                self.unit_set.add(unit)
        
        # relative strength of forces --------------------------------------- #
        self.health_blufor = gl.get_group_attr_total_num("health", self.manager.unit_blufor_group)
        self.health_redfor = gl.get_group_attr_total_num("health", self.manager.unit_redfor_group)
        self.relative_health = round(self.health_blufor / self.health_redfor, 2)
        self.attack_blufor = gl.get_group_total_munition_dmg(self.manager.unit_blufor_group)
        self.attack_redfor = gl.get_group_total_munition_dmg(self.manager.unit_redfor_group)
        self.relative_attack = round(self.attack_blufor / self.attack_redfor, 2)
        self.num_blufor = len(self.manager.unit_blufor_group)
        self.num_redfor = len(self.manager.unit_redfor_group)
        self.relative_numbers = round(self.num_blufor / self.num_redfor, 2)
        # map objective ----------------------------------------------------- #
        self.map_objective = None
        self.obj_coords_a = None
        self.obj_coords_b = None
        
        # choke points between objectives ----------------------------------- #
        self.chokepoints = list()
        
        # units that cannot escape (%?) damage the next blue turn ----------- #
        self.commited_units = 0
        
        # relative positions of units (red_active, red, blue) --------------- #
        self.activated_red = None
        self.red_units = list()
        self.blu_units = list()
        
        # current situation for redfor -------------------------------------- #
        self.situation = None

    # get the relative strength of red / blu -------------------------------- #
    def relative_strength(self):
        
        self.health_blufor = gl.get_group_attr_total_num("health", self.manager.unit_blufor_group)
        self.health_redfor = gl.get_group_attr_total_num("health", self.manager.unit_redfor_group)
        self.relative_health = round(self.health_blufor / self.health_redfor, 2)
        self.attack_blufor = gl.get_group_total_munition_dmg(self.manager.unit_blufor_group)
        self.attack_redfor = gl.get_group_total_munition_dmg(self.manager.unit_redfor_group)
        self.relative_attack = round(self.attack_blufor / self.attack_redfor, 2)
        self.num_blufor = len(self.manager.unit_blufor_group)
        self.num_redfor = len(self.manager.unit_redfor_group)
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
        if self.manager.resolver.wc_roundslimit >= self.manager.resolver.lc_roundslimit:
            # lc_dest_specific, lc_unit_at_coords --------------------------- #
            if self.manager.resolver.lc_dest_specific or self.manager.resolver.lc_unit_at_coords:
                self.situation = "attack_move"
            # lc_perc_dest_health, lc_perc_dest_dmgpt ----------------------- #
            elif self.manager.resolver.lc_perc_dest_health or self.manager.resolver.lc_perc_dest_dmgpt:
                self.situation = "attack_move"
        
        # time is favouring redfor ------------------------------------------ #
        else:
            # wc_dest_specific, wc_unit_at_coords --------------------------- #
            if self.manager.resolver.wc_dest_specific or self.manager.resolver.wc_unit_at_coords:
                self.situation = "hold_chokepoints"
            # wc_perc_dest_health, wc_perc_dest_dmgpt ----------------------- #
            elif self.manager.resolver.wc_perc_dest_health or self.manager.resolver.wc_perc_dest_dmgpt:
                self.situation = "delay"
        
    
    # get number of chokepoints --------------------------------------------- #
    def get_chokepoints(self):
        """
        Chokepoints defined as top 5% most traveled tiles if any possible route 
        is traveled once, meaning from any tile to any other possible tile.
        """
        stepped_on_tile_lst = list()
        
        for coords_from in self.manager.map_graph_matrix.matrix_coords:
            for coords_to in self.manager.map_graph_matrix.matrix_coords:
                stepped_on = self.manager.map_graph_matrix.a_star_algorithm(coords_from, coords_to)
                for stepped in stepped_on:
                    stepped_on_tile_lst.append(stepped)
        
        chokepoints_dict = Counter(stepped_on_tile_lst) 
        
        top_5_perc = int(math.ceil(len(self.manager.map_graph_matrix.matrix_coords) * 0.05))
        self.chokepoints = chokepoints_dict.most_common(top_5_perc)

    
    # get units commited to engagement -------------------------------------- #
    def get_commited_red(self):
        pass
    
    def red_active_next_action(self):
        if self.activated_red != None:
            print(self.situation)
            Munition(self.manager, "r_nuclear_torpedo", next(u for u in self.manager.unit_redfor_group if u.activated == True), gl.get_coords_occupancy((2, 4, -6), self.manager))
        
