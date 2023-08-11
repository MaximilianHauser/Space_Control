# -*- coding: utf-8 -*-
"""
Created on Wed May  3 13:04:31 2023

Provides an object with superclass pygame.Sprite, which essentially functions 
as a button, that executes a linked function, when released.

Dependencies:
-------------
pygame - Community Edition
    pip install pygame-ce
    
settings.py
    Containing constants for UI_INTERFACE_LAYER, UI_TRANSPARENCY, T_PURPLE, FONTSIZE.
    
observer.py optional
    Can be used as one way to pass events to the Button object.

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from settings import UI_INTERFACE_LAYER, UI_TRANSPARENCY, ui_colors_dict


class Button(pg.sprite.Sprite):
    def __init__(self, manager:object, text_in:str, x:int, y:int, cb_attr:str, cb_val:str, 
                 sprite_groups:list,
                 specific_width:int = False,
                 specific_height:int = False,
                 enabled:bool = True,
                 predefined_color_scheme:str = False,
                 transparency:int = UI_TRANSPARENCY,
                 active_font = None,
                 font_size = 24,
                 un_text_col:str = "white",
                 hov_text_col:str = "white",
                 pres_text_col:str = "white",
                 un_fill_col:str = "darkslategray3",
                 hov_fill_col:str = "darkslategray3",
                 pres_fill_col:str = "darkslategray4",
                 un_border_col:str = "darkslategray1",
                 hov_border_col:str = "darkslategray1",
                 pres_border_col:str = "darkslategray1"
                 ) -> pg.sprite.Sprite:
        
        pg.sprite.Sprite.__init__(self)
        
        self.manager = manager
        
        self.text_in = text_in
        
        self.x = x
        self.y = y

        self._layer = UI_INTERFACE_LAYER
        
        for group in sprite_groups:
            eval("self.manager." + group + ".add(self)")
        
        self.state = "unpressed"
        self.enabled = enabled
        self.cb_attr = cb_attr
        self.cb_val = cb_val
        
        self.active_font = active_font
        self.active_font.point_size = font_size
        
        # colors for each element in each state ----------------------------- #
        if predefined_color_scheme:
            un_text_col = ui_colors_dict[predefined_color_scheme]["un_text_col"]
            hov_text_col = ui_colors_dict[predefined_color_scheme]["hov_text_col"]
            pres_text_col = ui_colors_dict[predefined_color_scheme]["pres_text_col"]
            un_fill_col = ui_colors_dict[predefined_color_scheme]["un_fill_col"]
            hov_fill_col = ui_colors_dict[predefined_color_scheme]["hov_fill_col"]
            pres_fill_col = ui_colors_dict[predefined_color_scheme]["pres_fill_col"]
            un_border_col = ui_colors_dict[predefined_color_scheme]["un_border_col"]
            hov_border_col = ui_colors_dict[predefined_color_scheme]["hov_border_col"]
            pres_border_col = ui_colors_dict[predefined_color_scheme]["pres_border_col"]
        
        
        self.render_images(specific_width, specific_height, active_font, un_text_col, hov_text_col, pres_text_col, un_fill_col, hov_fill_col, pres_fill_col, un_border_col, hov_border_col, pres_border_col, transparency)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        
    def render_images(self, specific_width, specific_height, active_font, un_text_col, hov_text_col, pres_text_col, un_fill_col, hov_fill_col, pres_fill_col, un_border_col, hov_border_col, pres_border_col, transparency=255):
        # getting metrics shared by all images ------------------------------ #
        metrics_text = self.active_font.render(self.text_in, True, un_text_col)
        (button_width, button_height) = metrics_text.get_size()
        
        if isinstance(specific_width, int):
            if specific_width > button_width:
                button_width = specific_width
           
        if isinstance(specific_height, int):
            if specific_height > button_height:
                button_height = specific_height
        
        image_type_dict = {"image_unpressed": {"text": un_text_col, "fill": un_fill_col, "border": un_border_col},
                           "image_hover": {"text": hov_text_col, "fill": hov_fill_col, "border": hov_border_col},
                           "image_pressed": {"text": pres_text_col, "fill": pres_fill_col, "border": pres_border_col}
                           }
        
        for key in image_type_dict.keys():
            image = pg.Surface((button_width, button_height))
            image.set_alpha(transparency)
            image.fill("black")
            image.set_colorkey("black")
            pg.draw.rect(image, image_type_dict[key]["fill"], ((0,0), (button_width, button_height)), 0, 5)
            pg.draw.rect(image, image_type_dict[key]["border"], ((0,0), (button_width, button_height)), 2, 5)
            text = self.active_font.render(self.text_in, True, image_type_dict[key]["text"])
            image.blit(text, (0,0))
            setattr(self, key, image)
    
    
    @property
    def image(self) -> pg.Surface:
        if self.enabled:
            if self.state == "pressed":
                return self.image_pressed
            elif self.state == "hover":
                return self.image_hover
            else:
                return self.image_unpressed
         
        
    # checks if click is touching tile -------------------------------------- #
    def msbtn_down(self, pos:tuple, button:int) -> bool:
        if self.enabled:
            touching = self.rect.collidepoint(pos)
        
            return touching


    def handle_events(self, event:int) -> None:
        # handle events related to mouse clicks on tile --------------------- #
        # button state is unpressed ----------------------------------------- #
        if self.state == "unpressed":
            if event.type == pg.MOUSEMOTION or self.manager.E_IDLE:
                touching = self.rect.collidepoint(event.pos)
                if touching:
                    self.state = "hover"
        
        # button state is hover --------------------------------------------- #
        elif self.state == "hover":
            if event.type == pg.MOUSEMOTION or event.type == self.manager.E_IDLE:
                touching = self.rect.collidepoint(event.pos)
                if not touching:
                    self.state = "unpressed"
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
                    
                    
        # button state is pressed ------------------------------------------- #        
        elif self.state == "pressed":
            if event.type == pg.MOUSEBUTTONUP:
                self.state = "unpressed"
                setattr(self.manager, self.cb_attr, self.cb_val)
                
            elif event.type == pg.MOUSEMOTION or event.type == self.manager.E_IDLE:
                touching = self.rect.collidepoint(event.pos)
                if not touching:
                    self.state = "unpressed"
                    
