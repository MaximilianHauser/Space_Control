# -*- coding: utf-8 -*-
"""
Created on Sat May  6 16:39:29 2023

Provides an object with superclass pygame.Sprite, that creates a dropdownmenu
with n buttons, each button executing a function. The button_text, function
pairs are passed as keywordarguments.

Dependencies:
-------------
pygame - Community Edition
    pip install pygame-ce
    
settings.py
    Containing constants for UI_MAPINFO_LAYER, UI_TRANSPARENCY, FONTSIZE.
    
observer.py
    Can be used as one way to pass events to the object, different method 
    requires changing the code.

@author: Maximilian Hauser
"""


# import section ------------------------------------------------------------ #
import pygame as pg
from game_logic import GameLogic as gl
from settings import UI_MAPINFO_LAYER, FONTSIZE, UI_TRANSPARENCY

# DropdownMenu class -------------------------------------------------------- #
class DropDownMenu(pg.sprite.Sprite):
    """
    Creates a object with superclass pygame.Sprite, which essentially functions 
    as a button, that executes a linked function, when released.
    
    Attributes:
    -----------
    self.game = game
        Main game loop object.
        
    self.x = x
        Topleft position of the menu, in pixel from the left edge of the screen.
    
    self.y = y
        Topleft position of the menu, in pixel from the top edge of the screen.
    
    self._layer = UI_MAPINFO_LAYER
        Layer responsible for the order in which objects are drawn unto the screen.
    
    self.game.ui_mapinfo_grp.add(self)
        Add self to sprites.Group ui_mapinfo_grp.
    
    self.game.all_sprites.add(self)
        Add self to sprites.Group all_sprites.
    
    self.attr_dict = dict()
        Dictionary to hold button text, function key, value pairs.
    
    self.num_rows = len(self.attr_dict)
        Number of buttons the dropdown menu contains.
        
    self.width = width
        Width of the menu in pixel.
        
    self.heigt_option = FONTSIZE
        Height of one button.
    
    self.height_total = FONTSIZE * self.num_rows
        Height of the menu.
    
    self.image = pg.Surface((self.width, self.height_total))
        Creates a pygame Surface to draw the menu on top.
    
    self.image.fill("blue")
        Fill the Surface with blue color.
    
    self.image.set_colorkey("black")
        Set the transperency color of the image.
    
    self.image.set_alpha(UI_TRANSPARENCY)
        Set the transparency of the button.
    
    self.rect = self.image.get_rect()
        Creates a pygame.Rect object for storing coordinates based on the 
        previously defined Surface.
    
    self.rect.topleft = (self.x, self.y)
        Set the topleft Rect coordinates equal to x and y.
    
    self.mask = pg.mask.from_surface(self.image)
        Creates mask from the Surface.

    self.pressed_lst = ["unpressed" for i in range(self.num_rows)]
        Creates a list with the state of each button, initially "unpressed".
    
    self.rect_lst = [None for i in range(self.num_rows)]
        Creates a list with the rect of each button, initial None, created with
        initial update().

    self.update()
        Initial draw, as events get checked before update in main.
        
    Methods:
    --------
    update(self) -> None:
        Update function to be used in combination with the main game loop to
        update the state of the dropdownmenu.
        
    msbtn_down(self, pos:tuple, button:int) -> bool:
        Checks wether the event position overlaps with the object, for observer.
        
    handle_events(self, event:int) -> None:
        Changes the state of the menu object, based on passed event.
        
    Examples:
    ---------
    self.ddm_open = True
    m_x, m_y = event.pos
    kwargs = gl.get_kwargs_ddm(self, blufor_activated, self.game.unit_blufor_grp, self.game.tile_grp)
    setattr(self.game, "dropdownmenu", DropDownMenu(self.game, m_x, m_y, 100, **kwargs))
    self.game.observer.subscribe(pg.MOUSEBUTTONDOWN, self.game.dropdownmenu)
    self.game.observer.subscribe(pg.MOUSEBUTTONUP, self.game.dropdownmenu)
    self.game.observer.subscribe(self.game.E_IDLE, self.game.dropdownmenu)
    """
    def __init__(self, game:object, x:int, y:int, width:int, **kwargs) -> object:
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.x = x
        self.y = y
        
        self._layer = UI_MAPINFO_LAYER
        self.game.ui_mapinfo_grp.add(self)
        self.game.all_sprites.add(self)
        
        self.attr_dict = dict()
        
        for k, v in kwargs.items():
            setattr(self, k, v)
            self.attr_dict.update({k:v})
        
        self.num_rows = len(self.attr_dict)
            
        self.width = width
        self.heigt_option = FONTSIZE
        self.height_total = FONTSIZE * self.num_rows
        
        # surface for dropdown menu ----------------------------------------- #
        self.image = pg.Surface((self.width, self.height_total))
        self.image.fill("blue")
        self.image.set_colorkey("black")
        self.image.set_alpha(UI_TRANSPARENCY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)
        
        # functionality of individual buttons ------------------------------- #
        self.pressed_lst = ["unpressed" for i in range(self.num_rows)]
        self.rect_lst = [None for i in range(self.num_rows)]
        
        # initial draw, as events get checked before update in main --------- #
        self.update()
        
    def update(self) -> None:
        """
        Update function to be used in combination with the main game loop to
        update the state of the menu.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.
        
        Returns:
        --------
        None
        """
        for i in range(self.num_rows):
            
            if self.pressed_lst[i] == "hover":
                button_image = pg.draw.rect(self.image, "darkslategray4", [0, i*FONTSIZE+1, self.width, FONTSIZE])
                pg.draw.rect(self.image, "darkslategray1", [0, i*FONTSIZE+1, self.width, FONTSIZE], 2)
                
            elif self.pressed_lst[i] == "pressed":
                button_image = pg.draw.rect(self.image, "darkslategray", [0, i*FONTSIZE+1, self.width, FONTSIZE])
                pg.draw.rect(self.image, "darkslategray1", [0, i*FONTSIZE+1, self.width, FONTSIZE], 2)
                
            elif self.pressed_lst[i] == "unpressed":
                button_image = pg.draw.rect(self.image, "darkslategray3", [0, i*FONTSIZE+1, self.width, FONTSIZE])
                pg.draw.rect(self.image, "darkslategray1", [0, i*FONTSIZE+1, self.width, FONTSIZE], 2)
            
            text = list(self.attr_dict.keys())[i]
            text = self.game.font2.render(text, True, "white")
            
            self.image.blit(text, (4, i*FONTSIZE-2))
            
            self.rect_lst[i] = button_image
            
            self.rect.topleft = (self.x, self.y)
        
    
    def msbtn_down(self, pos:tuple, button:int) -> bool:
        """
        Checks wether the event position overlaps with the object.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.
        
        pos : tuple
            A tuple containing the pixel coordinates of an event (x,y).
        
        button : int
            Integer representing the mousebutton pressed, 1 for left, 3 for right.
        
        Returns:
        --------
        True, if event collided with self.mask, else False.
        """
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        touching = self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask)

        return touching
    
    def handle_events(self, event:int) -> None:
        """
        Changes the state of the menu object, based on passed event.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.

        pos : tuple
            A tuple containing the pixel coordinates of an event (x,y).
        
        Returns:
        --------
        None
        """
        for i in range(self.num_rows):
            
            pos_in_rect = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            
            if self.pressed_lst[i] == "unpressed":
                if event.type == self.game.E_IDLE:
                    if self.rect_lst[i].collidepoint(pos_in_rect):
                        self.pressed_lst[i] = "hover"
                
            elif self.pressed_lst[i] == "hover":
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.rect_lst[i].collidepoint(pos_in_rect):
                        self.pressed_lst[i] = "pressed"
                    
                elif event.type == self.game.E_IDLE:
                    touching = self.rect_lst[i].collidepoint(pos_in_rect)
                    if not touching:
                        self.pressed_lst[i] = "unpressed"
                
            elif self.pressed_lst[i] == "pressed":
                if event.type == pg.MOUSEBUTTONUP:
                    if self.rect_lst[i].collidepoint(pos_in_rect):
                        exec(getattr(self, list(self.attr_dict.keys())[i]))
                        setattr(next(t for t in self.game.tile_grp if t.ddm_open == True), "ddm_open", False)
                        self.game.observer.unsubscribe(pg.MOUSEBUTTONDOWN, self.game.dropdownmenu)
                        self.game.observer.unsubscribe(pg.MOUSEBUTTONUP, self.game.dropdownmenu)
                        self.game.observer.unsubscribe(self.game.E_IDLE, self.game.dropdownmenu)
                        self.kill()
                        delattr(self.game, "dropdownmenu")
                        
                elif event.type == self.game.E_IDLE:
                    touching = self.rect_lst[i].collidepoint(pos_in_rect)
                    if not touching:
                        self.pressed_lst[i] = "unpressed"
