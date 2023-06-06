# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 10:54:04 2022

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg

# event logic class handles posting of user events to eventqueque ----------- #
class EventLogic:
    
    def __init__(self):
        # running count to ensure unique event_id --------------------------- #
        self.custom_event_nr = 0
        self.custom_event_list = list()
    
    # create a new user_event (custom_event) with condition ----------------- #
    def new_custom_event(self, name, condition):
        
        e_name = eval(name)
        # create new event and assign event_id ------------------------------ #
        e_name = pg.event.custom_type()  + (self.custom_event_nr + 1)
        self.custom_event_nr += 1

        # append new event to event_list ------------------------------------ #
        self.custom_event_list.append((new_event, condition))
        
        return
    
    # creates custom_events based on condition ------------------------------ #
    def post_custom_events(self):
        
        for (e, c) in self.custom_event_list:
            if eval(c):
                pg.event.post(e)
                
        return


