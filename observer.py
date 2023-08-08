# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 06:49:29 2022

Observer is a design pattern in which an object, named the subject, 
maintains a list of its dependents, called observers, 
and notifies them automatically of any state changes, 
usually by calling one of their methods.
This variant is intended for event management of pygame-ce events and has an
added functionality for handling multiple overlaping sprites being subscribed to
pg.MOUSEBUTTONDOWN or pg.MOUSEBUTTONUP, so only the sprite with the topmost 
layer gets clicked.

Dependencies:
-------------
pygame - Community Edition
    pip install pygame-ce

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg

# Observer class ------------------------------------------------------------ #
class Observer:
    """
    Creates an object holding 2 dictionaries, with which the pygame event queque
    can be managed.
    
    Attributes:
    -----------
    self.subscribers_dict = dict()
        {event_type : list(subscribers)}
        
    self.sub_layers_dict = dict()
        {subscriber : subscriber._layer}
        
    Methods:
    --------
    get_subscribers(self, event_type:int) -> list:
        Returns a list containing all objects subscribed to an event_type.
        
    subscribe(self, event:int, subscriber:object) -> None:
        Subscribes an object or a function to an event.
        
    unsubscribe(self, event:int, subscriber:object) -> None:
        Unsubscribe (remove) an object or function from the subscribers_dict value_lst.
        
    event_mngr(self, events:list) -> None:
        Takes in the events from the pygame event queque stored in a list
        and executes a function if subscribed to the event. Passes the event to 
        the click_mngr in case of a pg.MOUSEBUTTONDOWN or a pg.MOUSEBUTTONUP
        event, or forwards it directly to the subscribed objects handle_events
        method.
        
    click_mngr(self, event:int) -> None:
        Checks beginning by the object with the topmost _layer all objects, which
        are subscribed to the event and passes the event to the first object
        it where the event.pos overlaps with the objects hitbox.
    """
    def __init__(self):
        self.subscribers_dict = dict()
        self.sub_layers_dict = dict()
        
        
    def get_subscribers(self, event_type:int) -> list:
        """
        Returns a list containing all objects subscribed to an event_type.
        
        Parameters:
        -----------
        event_type : Integer
            The integer of the event type. Event.type evaluates to an integer.
        
        Raises:
        -------
        TypeError: If the input is not an integer or event.type for event_type.
        
        Returns:
        --------
        subscibers(list): A list containing all objects subscribed to an event_type or an empty list.
        """
        subscribers = self.subscribers_dict.get(event_type)
        if subscribers == None:
            return list()
        else:
            return subscribers
        
        
    def subscribe(self, event:int, subscriber:object) -> None:
        """
        Subscribes an object or a function to an event.
        
        Parameters:
        -----------
        event : Integer
            The integer of the event type. Event.type evaluates to an integer.
        
        subscriber : Object, Function
            An object having a handle_events and in case of a mouse event a 
            msbtn_down method. A function can be used instead of an object.
        
        Raises:
        -------
        TypeError: If event is not an integer or subscriber is not an object.
        
        Returns:
        --------
        None
        """
        if not type(event) is int:
            raise TypeError
        
        subscribers = self.subscribers_dict.get(event)
        
        # if subscriber is an obj and not a func, add to layers_dict -------- #
        if isinstance(subscriber, object):
            if hasattr(subscriber, "_layer"):
                self.sub_layers_dict.update({subscriber:subscriber._layer})
        
        # making sure a list is appended as value to the dict --------------- #
        if not subscribers:
            subscribers = list()
            
        subscribers.append(subscriber)
            
        self.subscribers_dict.update({event:subscribers})
        print(str(subscriber) + " is now subscribed to " + str(event))
            
            
    def unsubscribe(self, event:int, subscriber:object) -> None:
        """
        Unsubscribe (remove) an object or function from the subscribers_dict value_lst.
        
        Parameters:
        -----------
        event : Integer
            The integer of the event type. Event.type evaluates to an integer.
        
        subscriber : Object, Function
            An object having a handle_events and in case of a mouse event a 
            msbtn_down method. A function can be used instead of an object.
        
        Raises:
        -------
        TypeError: If event is not an integer or subscriber is not an object.
        
        Returns:
        --------
        None
        """
        subscribers = self.subscribers_dict.get(event)
        for sub in subscribers:
            if sub is subscriber:
                subscribers.remove(subscriber)
            
        self.subscribers_dict.update({event:subscribers})
            
          
    def event_mngr(self, event:int) -> None:
        """
        Takes in the events from the pygame event queque stored in a list
        and executes a function if subscribed to the event. Passes the event to 
        the click_mngr in case of a pg.MOUSEBUTTONDOWN or a pg.MOUSEBUTTONUP
        event, or forwards it directly to the subscribed objects handle_events
        method.
        
        Parameters:
        -----------
        events : List
            A list containing pygame events returned by pygame.event.get from
            the event queque.
        
        Raises:
        -------
        TypeError: If the input is not a list.
        
        Returns:
        --------
        None
        """
        # subscribed = list of subscribers to event (or empty) ---------- #
        subscribed = self.get_subscribers(event.type)
        for subscriber in subscribed:
            # calls functions subscribed to event ----------------------- #
            if callable(subscriber):
                    subscriber()
            # handles objects (methods) subscribed to event ------------- #
            elif isinstance(subscriber, object):
                # seperate logic for msbtn down ------------------------- #
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.click_mngr(event)
                elif event.type == pg.MOUSEBUTTONUP:
                    self.click_mngr(event)
                else:
                    subscriber.handle_events(event)
            
            
    def click_mngr(self, event:int) -> None:
        """
        Checks beginning by the object with the topmost _layer all objects, which
        are subscribed to the event and passes the event to the first object
        it where the event.pos overlaps with the objects hitbox.
        
        Parameters:
        -----------
        event : Integer
            The integer of the event type. Event.type evaluates to an integer.
        
        Raises:
        -------
        TypeError: If the input is not an integer.
        
        Returns:
        --------
        None
        """
        # get subscribers to event ------------------------------------------ #
        subscribers = self.get_subscribers(event.type)
        l_start = max(self.sub_layers_dict.values())
        l_stop = min(self.sub_layers_dict.values()) - 1
            
        # from top layer starts checking subs if clicked, if yes: end loop -- #
        for l in range(l_start, l_stop, -1):
            for subscriber in subscribers:
                if isinstance(subscriber, object):
                    if subscriber._layer == l:
                        if subscriber.msbtn_down(event.pos, event.button):
                            subscriber.handle_events(event)
                            return
            
        
