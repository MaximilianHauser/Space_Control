# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 15:31:28 2023

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


# mission debriefing state -------------------------------------------------- #
class Debriefing(State):
    def __init__(self):
        super(Debriefing, self).__init__()
        
        # variable for update, to descern state, the screen is in ----------- #
        self.clicked_on = None
        
        # variable representing currently selected mission ------------------ #
        self.selected_mission = None
        
        # outcome of the battle that linked to the debriefing --------------- #
        self.battle_conclusion = None
        
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
        
        # button to retry or start next mission depending battle conclusion - #
        self.cont_button = None
        
        # mission briefing text --------------------------------------------- #
        self.debriefing_txt_path = None
        self.debriefing_txt = "$text_col_1$\nplaceholder_text"
        
        # typewritercrawl for briefing text --------------------------------- #
        self.debriefing_twc = TypewriterCrawl(self, 40, 40, 560, 330, self.debriefing_txt, ["all_sprites"], 
                                            active_font=self.font_smallcaps)
        
        # persistent attributes to be carried over to briefing, battle ------ #
        self.persistent = {"selected_mission":self.selected_mission, 
                           "battle_conclusion":self.battle_conclusion}
        
    def startup(self, persistent):
        # set variables carried over from battle state as attributes -------- #
        self.persistent.update(persistent)
        self.selected_mission = self.persistent["selected_mission"]
        self.battle_conclusion = self.persistent["battle_conclusion"]
        
        # load text for debriefing based on battle_conclusion --------------- #
        if self.battle_conclusion == "victory":
            self.debriefing_txt_path = ".\missions\\" + str(self.persistent["selected_mission"] + "\\debriefing_v.txt")
        elif self.battle_conclusion == "defeat":
            self.debriefing_txt_path = ".\missions\\" + str(self.persistent["selected_mission"] + "\\debriefing_d.txt")
        
        f = open(self.debriefing_txt_path, 'r')
        self.debriefing_txt = f.read()
        
        # close briefing text file ------------------------------------------ #
        f.close()
        
        # reinitialise typewritercrawl with selected mission debriefing text  #
        self.debriefing_twc = TypewriterCrawl(self, 40, 40, 560, 330, self.debriefing_txt, ["all_sprites"], 
                                            active_font=self.font_smallcaps)
        self.observer.subscribe(event=pg.MOUSEMOTION, subscriber=self.debriefing_twc.scrollbar)
        self.observer.subscribe(event=pg.MOUSEBUTTONDOWN, subscriber=self.debriefing_twc.scrollbar)
        self.observer.subscribe(event=pg.MOUSEBUTTONUP, subscriber=self.debriefing_twc.scrollbar)
        self.observer.subscribe(event=self.E_IDLE, subscriber=self.debriefing_twc.scrollbar)
        self.observer.subscribe(event=pg.MOUSEWHEEL, subscriber=self.debriefing_twc)
        
        # button to retry or start next mission depending battle conclusion - #
        if self.battle_conclusion == "victory":
            self.cont_button = Button(self, "next mission", WIN_WIDTH - 135, 400, "clicked_on", "next", ["all_sprites"], 
                                      predefined_color_scheme = "transp_white", transparency=255, 
                                      active_font=self.font_smallcaps, font_size=24)
        elif self.battle_conclusion == "defeat":
            self.cont_button = Button(self, "retry mission", WIN_WIDTH - 135, 400, "clicked_on", "retry", ["all_sprites"], 
                                      predefined_color_scheme = "transp_white", transparency=255, 
                                      active_font=self.font_smallcaps, font_size=24)
        self.observer.subscribe(pg.MOUSEMOTION, self.cont_button)
        self.observer.subscribe(pg.MOUSEBUTTONDOWN, self.cont_button)
        self.observer.subscribe(pg.MOUSEBUTTONUP, self.cont_button)
        self.observer.subscribe(self.E_IDLE, self.cont_button)
            
    def event(self, event, delta):
        # pass events to observer ------------------------------------------- #
        self.observer.event_mngr(event, delta)
        
    def update(self, delta):
        # update persistent dict -------------------------------------------- #
        self.all_sprites.update(delta)
        
        # connected states -------------------------------------------------- #
        if self.clicked_on == "menu":
            self.to_menu()
        elif self.clicked_on == "next":
            self.to_nextmission()
        elif self.clicked_on == "retry":
            self.to_retrycurrent()
        
    def draw(self, surface):
        surface.fill("black") #"gray30" as placeholder if needed
        self.all_sprites.draw(surface)
        self.debriefing_twc.draw(surface)
        
    def to_menu(self):
        self.next_state = "MAIN_MENU"
        self.done = True
    
    def to_nextmission(self):
        self.next_state = "BRIEFING"
        self.done = True
        
    def to_retrycurrent(self):
        self.next_state = "BATTLE"
        self.done = True
        
