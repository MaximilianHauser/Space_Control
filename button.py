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
from settings import UI_INTERFACE_LAYER, UI_TRANSPARENCY, T_PURPLE, FONTSIZE


class Button(pg.sprite.Sprite):
    """
    Creates a object with superclass pygame.Sprite, which essentially functions 
    as a button, that executes a linked function, when released.
    
    Attributes:
    -----------
    self.game = game
        Main game loop object.
    
    self.text_in = text_in
        Static text to be displayed on the button.
    
    self.var_dict = kwargs
        Stores all kwargs in {key : value} pairs.
        
    self.attr_dict = dict()
        Stores kwargs pairs, also used for accessing attributes defined by kwargs.
         
    self.text_out = text_in.format(**self.attr_dict)
        Inserts the kwargs derived from the attributes into the button text.
        Part of the mechanics enabling a working counter for example.
    
    self.x = x
        Topleft position of the button, in pixel from the left edge of the screen.
    
    self.y = y
        Topleft position of the button, in pixel from the top edge of the screen.
    
    self.width = width
        Width of the button in pixel.
        
    self.height = height
        Height of the button in pixel.
        
    self._layer = UI_INTERFACE_LAYER
        Layer responsible for the order in which objects are drawn unto the screen.
    
    self.game.all_sprites.add(self)
        Add self to sprites.Group all_sprites.
        
    self.game.ui_buttons_grp.add(self)
        Add self to sprites.Group ui_buttons_grp.
    
    self.enabled = enabled
        Initial state of the button, either True or False.
        
    self.state = "unpressed"
        Initial state of finite state algorithm.
    
    self.function = function
        Function to be executed when the mousebutton is released on the button object.
    
    self.image = pg.Surface((self.width, self.height))
        Creates a pygame Surface to draw the button on top.
    
    self.image.set_alpha(UI_TRANSPARENCY)
        Set the transparency of the button.
    
    self.image.fill(T_PURPLE)
        Fill the Surface with the transparency color.
        
    self.image.set_colorkey(T_PURPLE)
        Set the transperency color of the image.
    
    self.mask = None
        Creates mask variable, initial value None.
        
    self.rect = self.image.get_rect()
        Creates a pygame.Rect object for storing coordinates based on the 
        previously defined Surface.
    
    self.rect.topleft = (self.x, self.y)
        Set the topleft Rect coordinates equal to x and y.
        
    Methods:
    --------
    update(self) -> None:
        Update function to be used in combination with the main game loop to
        update the state of the button.
        
    msbtn_down(self, pos:tuple, button:int) -> bool:
        Linear interpolation returns point at t of distance between a and b.
        
    handle_events(self, event:int) -> None:
        Changes the state of the button object, based on passed event.
    
    """
    def __init__(self, game:object, text_in:str, x:int, y:int, width:int, height:int, enabled:bool, function, **kwargs) -> object:
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.text_in = text_in
        
        self.var_dict = kwargs
        self.attr_dict = dict()
        
        for k, v in kwargs.items():
            attr_v = getattr(v[0], v[1])
            setattr(self, k, attr_v)
            self.attr_dict.update({k:attr_v}) 
             
        self.text_out = text_in.format(**self.attr_dict)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._layer = UI_INTERFACE_LAYER
        
        self.game.all_sprites.add(self)
        self.game.ui_buttons_grp.add(self)
        
        self.enabled = enabled
        self.state = "unpressed"
        self.function = function
        
        self.image = pg.Surface((self.width, self.height))
        self.image.set_alpha(UI_TRANSPARENCY)
        self.image.fill(T_PURPLE)
        self.image.set_colorkey(T_PURPLE)
        self.mask = None
        self.rect = self.image.get_rect()
        
        self.rect.topleft = (self.x, self.y)
        
    def update(self) -> None:
        """
        Update function to be used in combination with the main game loop to
        update the state of the button.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.
        
        Returns:
        --------
        None
        """
        self.attr_dict = dict()
        
        for k, v in self.var_dict.items():
            attr_v = getattr(v[0], v[1])
            setattr(self, k, attr_v)
            self.attr_dict.update({k:attr_v}) 
        
        self.text_out = self.text_in.format(**self.attr_dict)
        button_text = self.game.font1.render(self.text_out, True, "white")
        if self.enabled:
            if self.state == "pressed":
                pg.draw.rect(self.image, "darkslategray4", ((0,0), (self.width, self.height)), 0, 5)
                pg.draw.rect(self.image, "darkslategray1", ((0,0), (self.width, self.height)), 2, 5)
            else:
                pg.draw.rect(self.image, "darkslategray3", ((0,0), (self.width, self.height)), 0, 5)
                pg.draw.rect(self.image, "darkslategray1", ((0,0), (self.width, self.height)), 2, 5)
        else:
            self.kill()
        pg.draw.rect(self.image, "darkslategray1", ((0,0), (self.width, self.height)), 2, 5)
        self.image.blit(button_text, (10, (self.height - FONTSIZE) * 0.75))
        
        self.mask = pg.mask.from_surface(self.image)
        
        self.game.screen.blit(self.image, (self.x, self.y))
        
    # checks if click is touching tile -------------------------------------- #
    def msbtn_down(self, pos:tuple, button:int) -> bool:
        """
        Checks wether the event position overlaps with the button.
        
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
        Changes the state of the button object, based on passed event.
        
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
        # handle events related to mouse clicks on tile --------------------- #
        if self.state == "unpressed":
            if event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
                
        if self.state == "pressed":
            if event.type == pg.MOUSEBUTTONUP:
                self.state = "unpressed"
                eval(self.function)
                
            elif event.type == self.game.E_IDLE:
                pos_in_mask = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
                touching = self.rect.collidepoint(event.pos) and self.mask.get_at(pos_in_mask)
                if not touching:
                    self.state = "unpressed"