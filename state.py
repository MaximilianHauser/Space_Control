# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 18:11:43 2023

@author: Maximilian Hauser
"""
# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import pygame as pg

# misc ---------------------------------------------------------------------- #
from settings import DEFAULT_FONTSIZE


# State class template ------------------------------------------------------ #
class State:
    def __init__(self, *, attr_dict:dict=False):
        print("Initialising: " + str(self))
        
        self.total_runtime = 0
            
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persistent = {}
        self._layer = 0
        
        # custom event E_IDLE ----------------------------------------------- #
        self.E_IDLE = 32867
        
        # shared sprite group ----------------------------------------------- #
        self.all_sprites = pg.sprite.LayeredUpdates()
        
        # fonts ------------------------------------------------------------- #
        self.font_coalition = pg.font.Font("img/coalition.ttf", DEFAULT_FONTSIZE)
        self.font_smallcaps = pg.font.Font("img/berlinsmallcaps.ttf", DEFAULT_FONTSIZE)

        if attr_dict:
            self.attr_dict = attr_dict
            for k, v in attr_dict:
                setattr(self, k, None)
                print(k)
    
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
        self.persistent.update(persistent)
        if hasattr(self, "attr_dict"):
            for k, v in self.attr_dict:
                print(k, v)

    def event(self, event, delta):
        pass

    def update(self, delta):
        pass

    def draw(self, surface):
        pass
    
    def quit(self):
        pass
    
        

