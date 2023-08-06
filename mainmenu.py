# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 08:49:27 2023

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import sys
import itertools
import pygame as pg
from state import State
from observer import Observer
from settings import WIN_WIDTH, WIN_HEIGHT, FONTSIZE_MENU

# main menu ----------------------------------------------------------------- #
class MainMenu(State):
    def __init__(self):
        super(MainMenu, self).__init__()
        
        # define custom_events ---------------------------------------------- #
        self.E_IDLE = pg.event.custom_type() + 0
        
        # init Observer ----------------------------------------------------- #
        self.observer = Observer()
        
        # game title text --------------------------------------------------- #
        self.title = self.font_splash.render("SPACE CONTROL", True, pg.Color("white"))
        game_title_center = tuple(map(lambda i, j: i + j, self.screen_rect.center, (0, -WIN_HEIGHT*0.25)))
        self.title_rect = self.title.get_rect(center=game_title_center)
        
        self.menu = pg.sprite.Group(
            MenuEntry("new campaign", "me_newcampaign", menu_state=self),
            MenuEntry("mission select", "me_selectmission", menu_state=self),
            MenuEntry("options", "me_options", menu_state=self),
            MenuEntry("credits", "me_credits", menu_state=self),
            MenuEntry("exit game", "me_exit", menu_state=self)
        )
 
        centerx = WIN_WIDTH * 0.5
        uppery_menu = self.screen_rect.centery - WIN_HEIGHT*0.05
        y = itertools.count(uppery_menu, FONTSIZE_MENU+2)
        for sprite in self.menu:
            sprite.rect.centerx = centerx
            sprite.rect.y = next(y)
 
        self.clicked_on = None
        
    def event(self, event):
        # pass events to observer ------------------------------------------- #
        self.observer.event_mngr(event)
        
    def update(self, delta):
        if self.clicked_on == "me_newcampaign":
            self.me_newcampaign()
        elif self.clicked_on == "me_selectmission":
            self.me_selectmission()
        elif self.clicked_on == "me_options":
            self.me_options()
        elif self.clicked_on == "me_credits":
            self.me_credits()
        elif self.clicked_on == "me_exit":
            self.me_exit()
 
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
        self.menu.draw(surface)
        
    
    # menu entry specific functions ----------------------------------------- #
    def me_newcampaign(self):
        self.next_state = "BRIEFING"
        self.done = True
    
    def me_selectmission(self):
        self.next_state = "MISSION_SELECT"
        self.done = True
    
    def me_options(self):
        self.next_state = "OPTIONS"
        self.done = True
    
    def me_credits(self):
        self.next_state = "CREDITS"
        self.done = True
    
    def me_exit(self):
        pg.quit()
        sys.exit()


class MenuEntry(pg.sprite.Sprite):
    identity = 0
 
    def __init__(self, text, callback, menu_state):
        pg.sprite.Sprite.__init__(self)
        self.menu_state = menu_state
        
        self._layer = 0
        
        # observer subscription --------------------------------------------- #
        self.menu_state.observer.subscribe(event=pg.MOUSEMOTION, subscriber=self)
        self.menu_state.observer.subscribe(event=pg.MOUSEBUTTONDOWN, subscriber=self)
        self.menu_state.observer.subscribe(event=pg.MOUSEBUTTONUP, subscriber=self)
        self.menu_state.observer.subscribe(event=self.menu_state.E_IDLE, subscriber=self)
        
        self.text = text
        self.hover = False
        self.callback = callback
        
        self.state = "unpressed"
        
        # prerendered images for each state --------------------------------- #
        self.unpressed_image = self.menu_state.font_menu.render(self.text, True, "white")
        self.hover_image = self.menu_state.font_menu.render(self.text, True, "darkslategray1")
        self.pressed_image = self.menu_state.font_menu.render(self.text, True, "darkslategray3")
        
        self.rect = self.image.get_rect()
        self.identity = MenuEntry.identity
        MenuEntry.identity += 1
        
    @property
    def image(self) -> pg.Surface:
        if self.state == "hover":
            return self.hover_image
        elif self.state == "pressed":
            return self.pressed_image
        else:
            return self.unpressed_image
        
    def update(self):
        pass
        
    def msbtn_down(self, pos, button):
        touching = self.rect.collidepoint(pos)
        return touching
        
    def handle_events(self, event):
        
        # menu entry is initially unpressed --------------------------------- #
        if self.state == "unpressed":
            if event.type == pg.MOUSEMOTION or event.type == self.menu_state.E_IDLE:
                if self.msbtn_down(event.pos, "key not needed"):
                    self.state = "hover"
                
        # menu entry is initially hovered on -------------------------------- #
        elif self.state == "hover":
            if event.type == pg.MOUSEMOTION or event.type == self.menu_state.E_IDLE:
                if not self.msbtn_down(event.pos, "key not needed"):
                    self.state = "unpressed"
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
        
        # menu entry is initially pressed ----------------------------------- #
        elif self.state == "pressed":
            if event.type == pg.MOUSEBUTTONUP:
                self.menu_state.clicked_on = self.callback
    
 

