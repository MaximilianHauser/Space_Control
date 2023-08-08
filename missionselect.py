# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 15:29:04 2023

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import os
import itertools
import pygame as pg
from state import State
from observer import Observer
from button import Button
from settings import WIN_WIDTH, MOUSESCROLLSPEED, ui_colors_dict

# mission selection menu ---------------------------------------------------- #
class MissionSelect(State):
    def __init__(self):
        super(MissionSelect, self).__init__()
        
        # variable for update, to descern state, the screen is in ----------- #
        self.clicked_on = None
        
        # variable representing currently selected mission ------------------ #
        self.selected_mission = None
        
        # define custom_events ---------------------------------------------- #
        self.E_IDLE = pg.event.custom_type() + 0
        
        # observer for event management ------------------------------------- #
        self.observer = Observer()
        
        # button for returning to menu -------------------------------------- #
        self.menu_button = Button(self, "main menu", 40, 400, "clicked_on", "menu", ["all_sprites"], predefined_color_scheme = "transp_white", transparency=255)
        self.observer.subscribe(pg.MOUSEMOTION, self.menu_button)
        self.observer.subscribe(pg.MOUSEBUTTONDOWN, self.menu_button)
        self.observer.subscribe(pg.MOUSEBUTTONUP, self.menu_button)
        self.observer.subscribe(self.E_IDLE, self.menu_button)
        
        # button for starting the game -------------------------------------- #
        self.start_button = Button(self, "start game", WIN_WIDTH - 135, 400, "clicked_on", "briefing", ["all_sprites"], predefined_color_scheme = "transp_white", transparency=255)
        self.observer.subscribe(pg.MOUSEMOTION, self.start_button)
        self.observer.subscribe(pg.MOUSEBUTTONDOWN, self.start_button)
        self.observer.subscribe(pg.MOUSEBUTTONUP, self.start_button)
        self.observer.subscribe(self.E_IDLE, self.start_button)
        
        # Mission Menu ------------------------------------------------------ #
        self.mission_menu = MissionMenu(self, 170, 60, 300, 300)

        # persistent attributes to be carried over to briefing, battle ------ #
        self.persistent = {"selected_mission":self.selected_mission}
    
    def event(self, event):
        # pass events to observer ------------------------------------------- #
        self.observer.event_mngr(event)
    
    def update(self, delta):
        # update persistent dict -------------------------------------------- #
        self.all_sprites.update(delta)
        
        # connected states -------------------------------------------------- #
        if self.clicked_on == "menu":
            self.to_menu()
        elif self.clicked_on == "briefing":
            self.to_battle()
            
        # persistent attributes to be carried over to briefing, battle ------ #
        self.persistent = {"selected_mission":self.selected_mission}
    
    def draw(self, surface):
        surface.fill("black")
        self.all_sprites.draw(surface)
        self.mission_menu.draw(surface)
        
    def to_menu(self):
        self.next_state = "MAIN_MENU"
        self.done = True
    
    def to_battle(self):
        if self.selected_mission:
            self.next_state = "BRIEFING"
            self.done = True
        else:
            self.clicked_on = None
        

# mission selection scrollable menu sprite object --------------------------- #    
class MissionMenu(pg.sprite.Sprite):
    def __init__(self, menu_state, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        
        self.menu_state = menu_state
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # relative position to screen --------------------------------------- #
        self.rel_pos = (self.x, self.y)
        
        # add mission menu to MissionSelect states sprite group ------------- #
        self.menu_state.all_sprites.add(self)
        
        # scrollable mission select window ---------------------------------- #
        self.mission_menu = pg.sprite.Group()
        self.mission_scrollbar = pg.sprite.Group()
        
        # add menu entries -------------------------------------------------- #
        mission_folders = [entry.name for entry in os.scandir(".\missions") if entry.is_dir()]
        
        for folder in mission_folders:
            entry = MenuEntry(folder, str(folder), mission_menu_state=self)
        
        # get the height of one MenuEntry ----------------------------------- #
        entry_surface = next(iter(self.mission_menu)).image
        (es_width, es_height) = entry_surface.get_size()
        
        self.es_height = es_height
        
        # space out mission menu entries evenly ----------------------------- #
        left = 0
        uppery_menu = 0
        y = itertools.count(uppery_menu, es_height)
        for sprite in self.mission_menu:
            sprite.rect.left = left
            sprite.rect.y = next(y)
        
        # attributes for scroll mechanic ------------------------------------ #
        self.height_rows_total = es_height * len(self.mission_menu)
        self.height_ratio = height / self.height_rows_total
        
        if self.height_ratio >= 1:
            self.scrollbar_height = self.height
        else:
            self.scrollbar_height = self.height_ratio * self.height
        
        # difference height scrollbar to menu ------------------------------- #
        self.height_diff_sb_menu = self.height - self.scrollbar_height
        self.height_diff_entries_menu = self.height_rows_total - self.height
        
        if self.height_diff_sb_menu > 0:
            self.relative_y_traverse = self.height_diff_entries_menu / self.height_diff_sb_menu
        else:
            self.relative_y_traverse = 0
            
        # add scrollbar ----------------------------------------------------- #
        if self.height_ratio >= 1:
            pass
        else:
            self.scrollbar = ScrollBar(self, 10, self.scrollbar_height)
            self.scrollbar.rect.topleft = (self.width-10, 0)

        # surface for menu -------------------------------------------------- #
        self.image = pg.Surface((self.width, self.height))
        self.image.fill("black")
        self.image.set_colorkey("blue")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        # observer subscription for pg.MOUSEWHEEL --------------------------- #
        self.menu_state.observer.subscribe(event=pg.MOUSEWHEEL, subscriber=self)
    
    def update(self, delta):
        pass
    
    def draw(self, surface):
        self.image.fill("black")
        self.mission_menu.draw(self.image)
        self.mission_scrollbar.draw(self.image)
    
    def handle_events(self, event):
        # if MOUSEWHEEL scroll entries -------------------------------------- #
        if event.type == pg.MOUSEWHEEL:
            # scroll movement is forward ------------------------------------ #
            rel_y = -MOUSESCROLLSPEED * event.y
            if event.y > 0:
                if self.scrollbar.rect.top > 0:
                    self.scrollbar.rect.top += rel_y
                    menu_entries_top = min([menu_entry.rect.top for menu_entry in self.mission_menu])
                    y = itertools.count(menu_entries_top - rel_y * self.relative_y_traverse , self.es_height)
                    for menu_entry in self.mission_menu:
                        menu_entry.rect.top = next(y)
             
                # scrollbar is in its topmost position or past it --- #
                else:
                    self.scrollbar.rect.top = 0
                    y = itertools.count(0, self.es_height)
                    for menu_entry in self.mission_menu:
                        menu_entry.rect.top = next(y)
            # scroll movement is backwards ---------------------------------- #
            else:
                # scrollbar is not in its downwardmost position --------- #
                if self.scrollbar.rect.top < self.height - self.scrollbar.height:
                    self.scrollbar.rect.top += rel_y
                    menu_entries_top = min([menu_entry.rect.top for menu_entry in self.mission_menu])
                    y = itertools.count(menu_entries_top - rel_y * self.relative_y_traverse , self.es_height)
                    for menu_entry in self.mission_menu:
                        menu_entry.rect.top = next(y)
            
                # scrollbar is in its downwardmost position --------- #
                else:
                    self.scrollbar.rect.top = self.height - self.scrollbar.height
                    menu_entries_top = min([menu_entry.rect.top for menu_entry in self.mission_menu])
                    y = itertools.count(0 - self.height_diff_entries_menu, self.es_height)
                    for menu_entry in self.mission_menu:
                        menu_entry.rect.top = next(y)
        # else pass to individual menu entries ------------------------------ #
        else:
            for sprite in self.mission_menu:
                sprite.handle_events(event)
    
    def msbtn_down(self, pos, button):
        touching = self.rect.collidepoint(pos)
        return touching

# entry of a selectable mission --------------------------------------------- #
class MenuEntry(pg.sprite.Sprite):
    identity = 0
 
    def __init__(self, text, callback, mission_menu_state, un_text_col = "white", hov_text_col = "darkslategray1", pres_text_col = "darkslategray3"):
        pg.sprite.Sprite.__init__(self)
        self.mission_menu_state = mission_menu_state
        
        # add to all sprites ------------------------------------------------ #
        self.mission_menu_state.mission_menu.add(self)
        
        self._layer = 1
        
        # relative position to screen --------------------------------------- #
        self.rel_pos = (self.mission_menu_state.x, self.mission_menu_state.y)
        
        # observer subscription --------------------------------------------- #
        self.mission_menu_state.menu_state.observer.subscribe(event=pg.MOUSEMOTION, subscriber=self)
        self.mission_menu_state.menu_state.observer.subscribe(event=pg.MOUSEBUTTONDOWN, subscriber=self)
        self.mission_menu_state.menu_state.observer.subscribe(event=pg.MOUSEBUTTONUP, subscriber=self)
        self.mission_menu_state.menu_state.observer.subscribe(event=self.mission_menu_state.menu_state.E_IDLE, subscriber=self)
        
        self.text = text
        self.hover = False
        self.callback = callback
        
        self.state = "unpressed"
        
        image_type_dict = {"image_unpressed": {"text": un_text_col},
                           "image_hover": {"text": hov_text_col},
                           "image_pressed": {"text": pres_text_col}
                           }
        
        # prerendered images for each state --------------------------------- #
        self.render_images(image_type_dict)
        
        self.rect = self.image.get_rect()
        self.identity = MenuEntry.identity
        MenuEntry.identity += 1
        
    def render_images(self, image_type_dict):
        for key in image_type_dict.keys():
            metrics_text = self.mission_menu_state.menu_state.font_text.render(self.text, True, "white")
            (button_width, button_height) = metrics_text.get_size()
            button_width = self.mission_menu_state.width - 11
            image = pg.Surface((button_width, button_height))
            image.fill("black")
            image.set_colorkey("black")
            text = self.mission_menu_state.menu_state.font_text.render(self.text, True, image_type_dict[key]["text"])
            image.blit(text, (0,0))
            setattr(self, key, image)
        
    @property
    def image(self) -> pg.Surface:
        if self.state == "hover":
            return self.image_hover
        elif self.state == "pressed":
            return self.image_pressed
        else:
            return self.image_unpressed
        
    def update(self, delta):
        # relative position to screen --------------------------------------- #
        position_in_menu = self.rect.topleft
        menu_in_screen = (self.mission_menu_state.x, self.mission_menu_state.y)
        self.rel_pos = tuple(map(sum, zip(position_in_menu, menu_in_screen)))
        
    def msbtn_down(self, pos, button):
        # adjust position of mouse to relative position within sprite ------- #
        pos = (pos[0] - self.rel_pos[0], pos[1] - self.rel_pos[1])
        touching = self.rect.collidepoint(pos)
        return touching
        
    def handle_events(self, event):
        # menu entry is initially unpressed --------------------------------- #
        if self.state == "unpressed":
            if event.type == pg.MOUSEMOTION or event.type == self.mission_menu_state.menu_state.E_IDLE:
                if self.msbtn_down(event.pos, "key not needed"):
                    self.state = "hover"
                
        # menu entry is initially hovered on -------------------------------- #
        elif self.state == "hover":
            if event.type == pg.MOUSEMOTION or event.type == self.mission_menu_state.menu_state.E_IDLE:
                if not self.msbtn_down(event.pos, "key not needed"):
                    self.state = "unpressed"
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
                self.mission_menu_state.menu_state.selected_mission = self.callback
        
        # menu entry is initially pressed ----------------------------------- #
        elif self.state == "pressed":
            if self.mission_menu_state.menu_state.selected_mission != self.callback:
                self.state = "unpressed"
    
 
class ScrollBar(pg.sprite.Sprite):
    def __init__(self, mission_menu_state, width, height):
        pg.sprite.Sprite.__init__(self)
        
        self.mission_menu_state = mission_menu_state
        
        # add to all sprites ------------------------------------------------ #
        self.mission_menu_state.mission_scrollbar.add(self)
        
        self.state = "unpressed"
        
        self.height = height
        
        self._layer = 1
        
        # relative position to screen --------------------------------------- #
        self.rel_pos = (self.mission_menu_state.x, self.mission_menu_state.y)
        
        # observer subscription --------------------------------------------- #
        self.mission_menu_state.menu_state.observer.subscribe(event=pg.MOUSEMOTION, subscriber=self)
        self.mission_menu_state.menu_state.observer.subscribe(event=pg.MOUSEBUTTONDOWN, subscriber=self)
        self.mission_menu_state.menu_state.observer.subscribe(event=pg.MOUSEBUTTONUP, subscriber=self)
        self.mission_menu_state.menu_state.observer.subscribe(event=self.mission_menu_state.menu_state.E_IDLE, subscriber=self)
        
        # render scrollbar images ------------------------------------------- #
        self.render_images(width, height)
        
        # get rect for positioning and collision ---------------------------- #
        self.rect = self.image.get_rect()
        
    def render_images(self, width, height, 
                      predefined_color_scheme:str = False,
                      un_fill_col:str = "darkslategray3",
                      hov_fill_col:str = "darkslategray4",
                      pres_fill_col:str = "darkslategray",
                      un_border_col:str = "darkslategray1",
                      hov_border_col:str = "darkslategray1",
                      pres_border_col:str = "darkslategray1"
                      ) -> pg.sprite.Sprite:
        
        # if predefined colorscheme pull from ui_colors_dict ---------------- #
        if predefined_color_scheme:
            un_fill_col = ui_colors_dict[predefined_color_scheme]["un_fill_col"]
            hov_fill_col = ui_colors_dict[predefined_color_scheme]["hov_fill_col"]
            pres_fill_col = ui_colors_dict[predefined_color_scheme]["pres_fill_col"]
            un_border_col = ui_colors_dict[predefined_color_scheme]["un_border_col"]
            hov_border_col = ui_colors_dict[predefined_color_scheme]["hov_border_col"]
            pres_border_col = ui_colors_dict[predefined_color_scheme]["pres_border_col"]
        
        image_type_dict = {"image_unpressed": {"fill": un_fill_col, "border": un_border_col},
                           "image_hover": {"fill": hov_fill_col, "border": hov_border_col},
                           "image_pressed": {"fill": pres_fill_col, "border": pres_border_col}
                           }
        
        for key in image_type_dict.keys():
            image = pg.Surface((width, height))
            image.fill("black")
            image.set_colorkey("black")
            pg.draw.rect(image, image_type_dict[key]["fill"], ((0,0), (width, height)), 0, 5)
            pg.draw.rect(image, image_type_dict[key]["border"], ((0,0), (width, height)), 2, 5)
            setattr(self, key, image)
        
    
    @property
    def image(self) -> pg.Surface:
        if self.state == "hover":
            return self.image_hover
        elif self.state == "pressed":
            return self.image_pressed
        else:
            return self.image_unpressed
        
    def update(self, delta):
        # relative position to screen --------------------------------------- #
        position_in_menu = self.rect.topleft
        menu_in_screen = (self.mission_menu_state.x, self.mission_menu_state.y)
        self.rel_pos = tuple(map(sum, zip(position_in_menu, menu_in_screen)))
        
    def msbtn_down(self, pos, button):
        # adjust position of mouse to relative position within sprite ------- #
        pos = (pos[0] - self.rel_pos[0], pos[1] - self.rel_pos[1])
        touching = self.rect.collidepoint(pos)
        return touching
        
    def handle_events(self, event):
        # menu entry is initially unpressed --------------------------------- #
        if self.state == "unpressed":
            if event.type == pg.MOUSEMOTION or event.type == self.mission_menu_state.menu_state.E_IDLE:
                if self.msbtn_down(event.pos, "key not needed"):
                    self.state = "hover"
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
                
        # menu entry is initially hovered on -------------------------------- #
        elif self.state == "hover":
            if event.type == pg.MOUSEMOTION or event.type == self.mission_menu_state.menu_state.E_IDLE:
                if not self.msbtn_down(event.pos, "key not needed"):
                    self.state = "unpressed"
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
        
        # menu entry is initially pressed ----------------------------------- #
        elif self.state == "pressed":
            if event.type == pg.MOUSEMOTION:
                # move the scrollbar and the mission entries ---------------- #
                if self.msbtn_down(event.pos, "key not needed"):
                    # y_mousemovement is up or none ----------------------------- #
                    (rel_x, rel_y) = event.rel
                    if rel_y <= 0:
                        # scrollbar is not in its topmost position -------------- #
                        if self.rect.top > 0:
                            self.rect.top += rel_y
                            menu_entries_top = min([menu_entry.rect.top for menu_entry in self.mission_menu_state.mission_menu])
                            y = itertools.count(menu_entries_top - rel_y * self.mission_menu_state.relative_y_traverse , self.mission_menu_state.es_height)
                            for menu_entry in self.mission_menu_state.mission_menu:
                                menu_entry.rect.top = next(y)
                     
                        # scrollbar is in its topmost position or past it --- #
                        else:
                            self.rect.top = 0
                            y = itertools.count(0, self.mission_menu_state.es_height)
                            for menu_entry in self.mission_menu_state.mission_menu:
                                menu_entry.rect.top = next(y)
                            
                    # y_mousemovement is downwards ------------------------------ #        
                    else:
                        # scrollbar is not in its downwardmost position --------- #
                        if self.rect.top < self.mission_menu_state.height - self.height:
                            self.rect.top += rel_y
                            menu_entries_top = min([menu_entry.rect.top for menu_entry in self.mission_menu_state.mission_menu])
                            y = itertools.count(menu_entries_top - rel_y * self.mission_menu_state.relative_y_traverse , self.mission_menu_state.es_height)
                            for menu_entry in self.mission_menu_state.mission_menu:
                                menu_entry.rect.top = next(y)
                    
                        # scrollbar is in its downwardmost position --------- #
                        else:
                            self.rect.top = self.mission_menu_state.height - self.height
                            menu_entries_top = min([menu_entry.rect.top for menu_entry in self.mission_menu_state.mission_menu])
                            y = itertools.count(0 - self.mission_menu_state.height_diff_entries_menu, self.mission_menu_state.es_height)
                            for menu_entry in self.mission_menu_state.mission_menu:
                                menu_entry.rect.top = next(y)
                
                else:
                    self.state = "unpressed"
            elif event.type == pg.MOUSEBUTTONUP:
                self.state = "unpressed"
            
        
        
