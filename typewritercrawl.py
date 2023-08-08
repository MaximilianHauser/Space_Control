# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:39:07 2023

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import itertools
import re
import string as string_module
import pygame as pg
from settings import UI_INTERFACE_LAYER, ui_colors_dict


# typewritercrawl class ----------------------------------------------------- #
class TypewriterCrawl(pg.sprite.Sprite):
    def __init__(self, state:object, 
                           x:int, 
                           y:int, 
                           width:int, 
                           height:int, 
                           text:str, 
                           sprite_groups:list, 
                           text_col_1:str = "white", 
                           text_col_2:str = "darkslategray1", 
                           delete_frames = False,
                           transparency:int = 255
                           ) -> pg.sprite.Sprite:
        pg.sprite.Sprite.__init__(self)
        
        self.state = state
        
        self.active_font = self.state.font_text
        
        # scrollable typewritercrawl text window ---------------------------- #
        for group in sprite_groups:
            eval("self.state." + group + ".add(self)")
        
        self.text_menu = pg.sprite.Group()
        self.text_scrollbar = pg.sprite.Group()
        
        self._layer = UI_INTERFACE_LAYER
        
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        
        abc_lst = list(string_module.ascii_lowercase)
        
        row_id_gen_lst = list()
        for i in range(len(abc_lst)):
            for j in range(len(abc_lst)):
                row_id_gen_lst.append(abc_lst[i] + abc_lst[j])
        
        # transformation of text input to row color tuples ------------------ #
        text_in = text
        
        text_spl = text_in.split("$")

        text_lst = list(filter(None, text_spl))

        text_processed = list()

        for i in range(len(text_lst)):
            if re.match("text_col_\d", text_lst[i]):
                text_processed.append([text_lst[i+1],eval(text_lst[i])])

        for lst in text_processed:
            lst[0] = list(filter(None, lst[0].split("\n")))

        rows_colors_lst = list()
        
        for i in range(len(text_processed)):
            for row in text_processed[i][0]:
                row_color = (row, text_processed[i][1])
                rows_colors_lst.append(row_color)
        
        # get total number of rows ------------------------------------------ #
        num_rows = len(rows_colors_lst)
        
        # get height of one rendered text row ------------------------------- #
        test_row = TextRow(self, rows_colors_lst[0][0], rows_colors_lst[0][1])
        test_row_size = test_row.image.get_size()
        test_row.kill()
        
        self.height_row = test_row_size[1]
        
        self.height_rows_total = test_row_size[1] * num_rows

        self.height_ratio = height / self.height_rows_total
        
        if self.height_ratio >= 1:
            self.scrollbar_height = self.height
        else:
            self.scrollbar_height = self.height_ratio * self.height

        self.row_dct = dict()
        
        self.speed = 1
        self.cooldown = 0
        self.finished = False
        self.last_printed_row = 0
        self.delete_frames = delete_frames
        self.state = "unpressed"
        self.scrollbar_mask = None
        
        self.scrollbar_y = self.height - self.scrollbar_height
        
        # add TextRows ------------------------------------------------------ #
        for i in range(num_rows):
            row = TextRow(self, rows_colors_lst[i][0], rows_colors_lst[i][1])
            self.text_menu.add(row)
            
        # initial position for text rows ------------------------------------ #
        left = 0
        uppery_menu = 0
        y = itertools.count(uppery_menu, self.height_row)
        for sprite in self.text_menu:
            sprite.rect.left = left
            sprite.rect.y = next(y)
        
        # add ScrollBar ----------------------------------------------------- #
        scrollbar = ScrollBar(self, 10, self.scrollbar_height)
        self.text_scrollbar.add(scrollbar)
        scrollbar.rect.topleft = (self.width-10, 0)

        # surface for text -------------------------------------------------- #
        self.image = pg.Surface((self.width, self.height))
        self.image.fill("black")
        self.image.set_colorkey("blue")
        self.image.set_alpha(transparency)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        # subscribe text crawl object to observer --------------------------- #
        try:
            self.state.observer.subscribe(event=pg.MOUSEWHEEL, subscriber=self)
        except AttributeError as ae:
            print("# --------------------------------------------- #")
            print(ae)
            print(str(self) + " not subscribed to state.observer")
            print("pg.MOUSEWHEEL")
            print("# --------------------------------------------- #")
        
    def update(self, delta):
        pass
    
    def draw(self, surface):
        self.image.fill("black")
        self.text_menu.draw(self.image)
        self.text_scrollbar.draw(self.image)
    
    def handle_events(self, event):
        pass
    
    def msbtn_down(self, pos, button):
        touching = self.rect.collidepoint(pos)
        return touching

class TextRow(pg.sprite.Sprite):
    identity = 0
    def __init__(self, typewriter, text, color):
        pg.sprite.Sprite.__init__(self)
        
        self.typewriter = typewriter
        
        self._layer = 1
        
        # relative position to screen --------------------------------------- #
        self.rel_pos = (self.typewriter.x, self.typewriter.y)
        
        self.text = text
        
        # render text rows for different stages of printing to screen ------- #
        self.image = self.typewriter.active_font.render(self.text, True, color)
        
        self.rect = self.image.get_rect()
        self.identity = TextRow.identity
        TextRow.identity += 1
        
    def update(self, delta):
        # relative position to screen --------------------------------------- #
        position_in_menu = self.rect.topleft
        menu_in_screen = (self.typewriter.x, self.typewriter.y)
        self.rel_pos = tuple(map(sum, zip(position_in_menu, menu_in_screen)))


class ScrollBar(pg.sprite.Sprite):
    def __init__(self, typewriter, width, height):
        pg.sprite.Sprite.__init__(self)
        
        self.typewriter = typewriter
        
        self.state = "unpressed"
        
        self.height = height
        
        self._layer = 1
        
        # relative position to screen --------------------------------------- #
        self.rel_pos = (self.typewriter.x, self.typewriter.y)
        
        # render scrollbar images ------------------------------------------- #
        self.render_images(width, height)
        
        # get rect for positioning and collision ---------------------------- #
        self.rect = self.image.get_rect()
        
        # subscribe scrollbar to observer ----------------------------------- #
        try:
            self.typewriter.state.observer.subscribe(event=pg.MOUSEMOTION, subscriber=self)
            self.typewriter.state.observer.subscribe(event=pg.MOUSEBUTTONDOWN, subscriber=self)
            self.typewriter.state.observer.subscribe(event=pg.MOUSEBUTTONUP, subscriber=self)
            self.typewriter.state.observer.subscribe(event=self.typewriter.state.E_IDLE, subscriber=self)
            print("# --------------------------------------------- #")
            print(str(self) + " subscribed to state.observer")
            print("pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, E_IDLE")
            print("# --------------------------------------------- #")
        except AttributeError as ae:
            print("# --------------------------------------------- #")
            print(ae)
            print(str(self) + " not subscribed to state.observer")
            print("pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, E_IDLE")
            print("# --------------------------------------------- #")
        
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
        menu_in_screen = (self.typewriter.x, self.typewriter.y)
        self.rel_pos = tuple(map(sum, zip(position_in_menu, menu_in_screen)))
        
    def msbtn_down(self, pos, button):
        # adjust position of mouse to relative position within sprite ------- #
        pos = (pos[0] - self.rel_pos[0], pos[1] - self.rel_pos[1])
        touching = self.rect.collidepoint(pos)
        return touching
        
    def handle_events(self, event):
        # menu entry is initially unpressed --------------------------------- #
        if self.state == "unpressed":
            if event.type == pg.MOUSEMOTION or event.type == self.typewriter.menu_state.E_IDLE:
                if self.msbtn_down(event.pos, "key not needed"):
                    self.state = "hover"
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
                
        # menu entry is initially hovered on -------------------------------- #
        elif self.state == "hover":
            if event.type == pg.MOUSEMOTION or event.type == self.typewriter.menu_state.E_IDLE:
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
                            menu_entries_top = min([menu_entry.rect.top for menu_entry in self.typewriter.mission_menu])
                            y = itertools.count(menu_entries_top - rel_y * self.typewriter.relative_y_traverse , self.mission_menu_state.es_height)
                            for menu_entry in self.typewriter.mission_menu:
                                menu_entry.rect.top = next(y)
                     
                        # scrollbar is in its topmost position or past it --- #
                        else:
                            self.rect.top = 0
                            y = itertools.count(0, self.typewriter.es_height)
                            for menu_entry in self.typewriter.mission_menu:
                                menu_entry.rect.top = next(y)
                            
                    # y_mousemovement is downwards ------------------------------ #        
                    else:
                        # scrollbar is not in its downwardmost position --------- #
                        if self.rect.top < self.typewriter.height - self.height:
                            self.rect.top += rel_y
                            menu_entries_top = min([menu_entry.rect.top for menu_entry in self.typewriter.mission_menu])
                            y = itertools.count(menu_entries_top - rel_y * self.typewriter.relative_y_traverse , self.typewriter.es_height)
                            for menu_entry in self.typewriter.mission_menu:
                                menu_entry.rect.top = next(y)
                    
                        # scrollbar is in its downwardmost position --------- #
                        else:
                            self.rect.top = self.typewriter.height - self.height
                            menu_entries_top = min([menu_entry.rect.top for menu_entry in self.typewriter.mission_menu])
                            y = itertools.count(0 - self.typewriter.height_diff_entries_menu, self.typewriter.es_height)
                            for menu_entry in self.typewriter.mission_menu:
                                menu_entry.rect.top = next(y)
                
                else:
                    self.state = "unpressed"
            elif event.type == pg.MOUSEBUTTONUP:
                self.state = "unpressed"






