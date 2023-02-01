# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:19:15 2023

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import custom_data_types as cdt

# InitiativeQueque class ---------------------------------------------------- #
class InitiativeQueque:
    
    def __init__(self, game):
        self.game = game
        self.unit_set = set()
        
        spritegroup_lst = [self.game.unit_blufor_grp, self.game.unit_redfor_grp]
        for group in spritegroup_lst:
            for unit in group:
                self.unit_set.add(unit)
        
        temp_lst = list()
        self.initiative_queque = cdt.Queque()
        self.high_ini = list()
        self.low_ini_index = None
        self.sorted_lst = None

        for unit in self.unit_set:
            temp_lst.append((unit.id, unit.initiative))
    
        self.sorted_lst = sorted(temp_lst, key=lambda x:x[1])

        for item in self.sorted_lst:
            if item[1] > 15:
                self.high_ini.append(item)

        for i in range(len(self.sorted_lst)):
            if self.sorted_lst[i][1] < 5:
                self.low_ini_index = i
                break

        if self.low_ini_index != None:
            for i in range(len(self.high_ini)-1, -1, -1):
                self.sorted_lst.insert(self.low_ini_index, self.high_ini[i])

        for i in range(len(self.sorted_lst)):
            item = self.sorted_lst.pop(0)
            self.initiative_queque.enqueque(item)

    def set_unit_attr(self, **kwargs):
        for k in kwargs:
            unit = next((unit for unit in self.unit_set if unit.id == self.initiative_queque.items[0][0]), None)
            if unit != None:
                setattr(unit, k, kwargs[k])
    
    def move_unit_to_end_of_queque(self):
        unit = self.initiative_queque.dequeque()
        self.initiative_queque.enqueque(unit)
        
    def check_unit_ap(self):
        active_unit = next((unit for unit in self.unit_set if unit.activated == True), None)
        if active_unit.action_points <= 0:
            active_unit.activated = False
            active_unit.action_points = active_unit.starting_ap
            self.move_unit_to_end_of_queque()
            self.set_unit_attr(activated=True)





