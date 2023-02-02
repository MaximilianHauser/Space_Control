# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 18:46:34 2022

'AI' to handle enemy movement during battle

@author: Maximilian
"""



# import section ------------------------------------------------------------ #
import pygame as pg
from game_logic import GameLogic as gl

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
        self.relative_health = 0
        self.relative_attack = 0
        self.relative_numbers = 0
        # map objective ----------------------------------------------------- #
        self.map_objective = 0
        self.obj_coords_a = 0
        self.obj_coords_b = 0
        # choke points between objectives ----------------------------------- #
        self.no_chokepoints_soft = 0
        self.no_chokepoints_hard = 0
        # units that cannot escape (%?) damage the next blue turn ----------- #
        self.commited_units = 0

    # get the relative strength of red / blu -------------------------------- #
    def relative_strength(self):
        
        redfor_health = 0
        redfor_attack = 0
        redfor_numbers = 0
        blufor_health = 0
        blufor_attack = 0
        blufor_numbers = 0
        '''
        for red in self.game.unit_redfor_grp:
            redfor_health += red.health
            redfor_attack += red.attack
            redfor_numbers += 1
        
        for blu in self.game.unit_blufor_grp:
            blufor_health += blu.health
            blufor_attack += blu.attack
            blufor_numbers += 1
        '''
        self.relative_health = round(redfor_health / blufor_health, 2)
        self.relative_attack = round(redfor_attack / blufor_attack, 2)
        self.relative_numbers = round(redfor_numbers / blufor_numbers, 2)
        
    # get map objective ----------------------------------------------------- #
    def get_situation(self):
        for unit in self.unit_set:
            if unit.faction == "redfor":
                if unit.activated == True:
                    unit.action_points = 0
    
    # get number of chokepoints --------------------------------------------- #
    def get_chokepoints(self):
        pass
    
    # get units commited to engagement -------------------------------------- #
    def get_commited_red(self):
        pass
        
        
