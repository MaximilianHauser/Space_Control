# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 18:45:34 2023

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from state import State
from observer import Observer
from settings import WIN_HEIGHT

# splash screen ------------------------------------------------------------- #
class SplashScreen(State):
    def __init__(self):
        super(SplashScreen, self).__init__()
        
        # game title text --------------------------------------------------- #
        self.title_font = self.font_coalition
        self.title_font.point_size = 38
        self.title = self.font_coalition.render("SPACE CONTROL", True, pg.Color("white"))
        game_title_center = tuple(map(lambda i, j: i + j, self.screen_rect.center, (0, -WIN_HEIGHT*0.25)))
        self.title_rect = self.title.get_rect(center=game_title_center)
        
        # press any key to continue text ------------------------------------ #
        self.continue_font = self.font_smallcaps
        self.continue_font.point_size = 14
        self.any_key = self.font_smallcaps.render("press left mouse to continue", True, pg.Color("white"))
        any_key_center = tuple(map(lambda i, j: i + j, self.screen_rect.center, (0, WIN_HEIGHT*0.4)))
        self.any_key_rect = self.any_key.get_rect(center=any_key_center)
        
        # next state after splash screen ------------------------------------ #
        self.next_state = "MAIN_MENU"

        # observer for event management ------------------------------------- #
        self.observer = Observer()
        self.observer.subscribe(event=pg.MOUSEBUTTONDOWN, subscriber=self)
        
    def event(self, event, delta):
        self.observer.event_mngr(event, delta)

    def update(self, delta):
        pass

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.any_key, self.any_key_rect)
        
    def msbtn_down(self, pos, button):
        return True
        
    def handle_events(self, event, delta):
        self.done = True
        
        
        