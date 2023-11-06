# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 13:33:17 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import json

# eventslogic class --------------------------------------------------------- #
class EventsLogic:
    
    def __init__(self, manager):
        
        self.manager = manager
        self.unit_set = set()
        
        spritegroup_lst = [manager.unit_blufor_group, manager.unit_redfor_group]
        for group in spritegroup_lst:
            for unit in group:
                self.unit_set.add(unit)
        
        # set for events not yet triggered ---------------------------------- #
        self.events_not_done_or_active = set()
        
        # set for currently active events ----------------------------------- #
        self.currently_active_events = set()
        
        # import based on selected mission ---------------------------------- #
        battle_events_dict_path = ".\missions\\" + str(self.manager.persistent["selected_mission"] + "\\battle_events.json")
        
        json_o = open(battle_events_dict_path)
        self.battle_events_dict = json.load(json_o)
        json_o.close()
        
        for key in self.battle_events_dict.keys():
            self.events_not_done_or_active.add(key)

                
    def event_done(self, event_id):
        """
        Remove event_id from self.events_not_done_or_active when TRIGGER_END 
        condition met or is None.
        """
        pass
    
    
    def event_triggered(self, event_id):
        """
        Check if event_id TRIGGER (conditions) met.
        """
        pass
            
    
    def event_occurences(self, event_id):
        """
        Execute event occurences.
        """
        pass
    
    
    class EventLifespan:
        def __int__(self, event_id):
            
            self.c_seconds = 0
            self.c_moves = 0
            self.c_rounds = 0
            
            
        def event_ended(self):
            """
            Check if event has ended and stop occurences if True.
            """
            pass
            
