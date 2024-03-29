# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 15:29:31 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import pygame as pg

# algorithm objects --------------------------------------------------------- #
from state import State
from observer import Observer

# sprite objects ------------------------------------------------------------ #
from typewritercrawl import TypewriterCrawl
from button import Button

# misc ---------------------------------------------------------------------- #
from settings import WIN_WIDTH


# mission briefing state ---------------------------------------------------- #
class Briefing(State):
    def __init__(self):
        super(Briefing, self).__init__()
        
        # variable for update, to descern state, the screen is in ----------- #
        self.clicked_on = None
        
        # variable representing currently selected mission ------------------ #
        self.selected_mission = None
        
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
        
        # button for starting the game -------------------------------------- #
        self.start_button = Button(self, "start game", WIN_WIDTH - 135, 400, "clicked_on", "battle", ["all_sprites"], 
                                   predefined_color_scheme = "transp_white", transparency=255, 
                                   active_font=self.font_smallcaps, font_size=24)
        self.observer.subscribe(pg.MOUSEMOTION, self.start_button)
        self.observer.subscribe(pg.MOUSEBUTTONDOWN, self.start_button)
        self.observer.subscribe(pg.MOUSEBUTTONUP, self.start_button)
        self.observer.subscribe(self.E_IDLE, self.start_button)
        
        # mission briefing text --------------------------------------------- #
        self.briefing_txt_path = None
        self.briefing_txt = "$text_col_1$\nplaceholder_text"
        
        # typewritercrawl for briefing text --------------------------------- #
        self.briefing_twc = TypewriterCrawl(self, 40, 40, 560, 330, self.briefing_txt, ["all_sprites"], 
                                            active_font=self.font_smallcaps)
        
        # persistent attributes to be carried over to briefing, battle ------ #
        self.persistent = {"selected_mission":self.selected_mission}
        
    def startup(self, persistent):
        self.persistent.update(persistent)
        self.selected_mission = self.persistent["selected_mission"]
        
        self.briefing_txt_path = ".\missions\\" + str(self.persistent["selected_mission"] + "\\briefing.txt")
        f = open(self.briefing_txt_path, 'r')
        self.briefing_txt = f.read()
        # reinitialise typewritercrawl with selected mission briefing text -- #
        self.briefing_twc = TypewriterCrawl(self, 40, 40, 560, 330, self.briefing_txt, ["all_sprites"], 
                                            active_font=self.font_smallcaps)
        self.observer.subscribe(event=pg.MOUSEMOTION, subscriber=self.briefing_twc.scrollbar)
        self.observer.subscribe(event=pg.MOUSEBUTTONDOWN, subscriber=self.briefing_twc.scrollbar)
        self.observer.subscribe(event=pg.MOUSEBUTTONUP, subscriber=self.briefing_twc.scrollbar)
        self.observer.subscribe(event=self.E_IDLE, subscriber=self.briefing_twc.scrollbar)
        self.observer.subscribe(event=pg.MOUSEWHEEL, subscriber=self.briefing_twc)
        # close briefing text file ------------------------------------------ #
        f.close()
         
    def event(self, event, delta):
        # pass events to observer ------------------------------------------- #
        self.observer.event_mngr(event, delta)
        
    def update(self, delta):
        # update persistent dict -------------------------------------------- #
        self.all_sprites.update(delta)
        
        # connected states -------------------------------------------------- #
        if self.clicked_on == "menu":
            self.to_menu()
        elif self.clicked_on == "battle":
            self.to_battle()
        
    def draw(self, surface):
        surface.fill("black") #"gray30" as placeholder if needed
        self.all_sprites.draw(surface)
        self.briefing_twc.draw(surface)
        
    def to_menu(self):
        self.next_state = "MAIN_MENU"
        self.done = True
    
    def to_battle(self):
        self.next_state = "BATTLE"
        self.done = True
        
