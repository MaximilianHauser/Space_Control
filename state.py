# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 18:11:43 2023

@author: Maximilian Hauser
"""
# import section ------------------------------------------------------------ #
import pygame as pg
from settings import FONTSIZE_SPLASH, FONTSIZE_BUTTON, FONTSIZE_MENU, FONTSIZE_TEXT

# State class template ------------------------------------------------------ #
class State:
    def __init__(self):
            
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persistent = {}
        self._layer = 0
        
        # shared sprite group ----------------------------------------------- #
        self.all_sprites = pg.sprite.LayeredUpdates()
        
        # fonts ------------------------------------------------------------- #
        self.font_splash = pg.font.Font("img/coalition.ttf", FONTSIZE_SPLASH)
        self.font_button = pg.font.Font("img/coalition.ttf", FONTSIZE_BUTTON)
        self.font_menu = pg.font.Font("img/berlinsmallcaps.ttf", FONTSIZE_MENU)
        self.font_text = pg.font.Font("img/berlinsmallcaps.ttf", FONTSIZE_TEXT)
    
    def leave(self):
        # carry over persistant variables ----------------------------------- #
        for key in list(self.persistent.keys()): #list to force copy instead of view object
            if hasattr(self, key):
                self.persistent.update({key: getattr(self, key)})
            else:
                del self.persistent[key]
                
        # clear observer subscriptions -------------------------------------- #
        self.observer.subscribers_dict.clear()
        self.observer.sub_layers_dict.clear()
                    
        
    
    def startup(self, persistent):
        self.persistent = persistent

    def event(self, event):
        pass

    def update(self, delta):
        pass

    def draw(self, surface):
        pass
    
    def quit(self):
        pass
    
        

