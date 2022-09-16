# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 06:49:29 2022

prototype observer algorythm, 
need to add layers, so map logic is only executed if the same event hasn't called an ui-button

@author: Maximilian
"""

class Observer:
    def __init__(self):
        self.subscribers_dict = dict()
        self.sub_layers_dict = dict()
        
    # helper function to ensure a list is appended to an event(key) --------- #
    def get_subscribers(self, event_type):
        subscribers = self.subscribers_dict.get(event_type)
        if subscribers == None:
            return list()
        else:
            return subscribers
        
    # subscribe an object(method) or a function to an event ----------------- #
    def subscribe(self, event, subscriber):
        # get subscribers assigned to event from subscribers_dict ----------- #
        subscribers = self.subscribers_dict.get(event)
        # if subscribers list is assigned as key to value, append subscriber  #
        if subscribers:
            subscribers.append(subscriber)
        # add new key : value pair to subscribers_dict ---------------------- #
        else:
            self.subscribers_dict.update({event:subscriber})
            
    # unsubscribe (remove) an object or function from the s..._dict value_lst #
    def unsubscribe(self, event, subscriber):
        subscribers = self.get_subscribers(event)
        if subscribers:
            subscribers.remove(subscriber)
          
    # passes events to subscribers ------------------------------------------ #
    def event_mngr(self, events):
        for event in events:
            # subscribed = list of subscribers to event (or empty) ---------- #
            subscribed = self.get_subscribers(event)
            for subscriber in subscribed:
                # calls functions subscribed to event ----------------------- #
                if callable(subscriber):
                    subscriber()
                # handles objects (methods) subscribed to event ------------- #
                elif isinstance(subscriber, object):
                    subscriber.handle_events(event)
            
            
            
            
            