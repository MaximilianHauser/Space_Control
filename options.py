# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 11:57:25 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import pygame as pg

# algorithm objects --------------------------------------------------------- #
from state import State
from observer import Observer

# sprite objects ------------------------------------------------------------ #
from button import Button

# options state ------------------------------------------------------------- #
class Options(State):
    def __init__(self):
        super(Options, self).__init__()
        
        # variable for update, to descern state, the screen is in ----------- #
        self.clicked_on = None
        
        # init Observer ----------------------------------------------------- #
        self.observer = Observer()
        
        # button for returning to menu -------------------------------------- #
        self.menu_button = Button(self, "main menu", 40, 400, "clicked_on", "menu", ["all_sprites"], 
                                  predefined_color_scheme = "transp_white", transparency=255, 
                                  active_font=self.font_smallcaps, font_size=24)
        self.observer.subscribe(pg.MOUSEMOTION, self.menu_button)
        self.observer.subscribe(pg.MOUSEBUTTONDOWN, self.menu_button)
        self.observer.subscribe(pg.MOUSEBUTTONUP, self.menu_button)
        self.observer.subscribe(self.E_IDLE, self.menu_button)
        
    
    def event(self, event, delta):
        # pass events to observer ------------------------------------------- #
        self.observer.event_mngr(event, delta)
        
        
    def update(self, delta):
        # update persistent dict -------------------------------------------- #
        self.all_sprites.update(delta)
        
        # connected states -------------------------------------------------- #
        if self.clicked_on == "menu":
            self.to_menu()
    
    
    def draw(self, surface):
        surface.fill("black") #"gray30" as placeholder if needed
        self.all_sprites.draw(surface)
        
        
    def to_menu(self):
        self.next_state = "MAIN_MENU"
        self.done = True
        
