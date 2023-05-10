# -*- coding: utf-8 -*-
"""
Created on Mon May  8 08:43:41 2023

Provides an object with superclass pygame.Sprite, that is used to handle unit
animation as well as store attributes needed for unit interaction with the map
or other units.

Dependencies:
-------------
pygame - Community Edition
    pip install pygame-ce
    
itertools - standard library
    The module standardizes a core set of fast, memory efficient tools that are 
    useful by themselves or in combination. Together, they form an 
    “iterator algebra” making it possible to construct specialized tools 
    succinctly and efficiently in pure Python.

hexlogic
    Contains all hextile logic, specified as logic handling the relationship 
    between cartesian coordinates and cube coordinates, for the purpose of defining 
    the relative position of hexagon tiles on the screen. In addition it provides
    calculations in regards to hextile map related formulas and algorythms.

tile
    Provides an object with superclass pygame.Sprite, that creates a tile, which 
    can be used to create a hexagon tile map. It also holds the event management to 
    handle game interactions on the map, such as unit movement or attacks.

u_attr
    Contains a dictionary with all type specific unit attributes.

settings
    Containing constants for UNIT_LAYER, WIN_WIDTH and WIN_HEIGHT.

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg
import itertools
from hexlogic import HexLogic as hl
from attribute_dicts.u_attr import u_dict
from settings import UNIT_LAYER, WIN_WIDTH, WIN_HEIGHT

# Unit class ---------------------------------------------------------------- #
class Unit(pg.sprite.Sprite):
    """
    Creates an object with superclass pygame.Sprite, that is used to handle unit
    animation as well as store attributes needed for unit interaction with the map
    or other units.
    
    Attributes:
    -----------
    self.game = game
        Main game loop object.
    
    self.id = next(self.newid)
    
    
    self.q = q
        Cube coordinate q.
    
    self.r = r
        Cube coordinate r.
    
    self.s = s
        Cube coordinate s.
    
    self._layer = UNIT_LAYER
        Layer responsible for the order in which objects are drawn unto the screen.
    
    self.game.all_sprites.add(self)
        Add self to sprites.Group all_sprites.
    
    self.game.unit_redfor_grp.add(self)
        Add self to sprites.Group unit_redfor_grp or unit_blufor_grp.
        
    x, y = hl.hex_to_pixel((q,r,s))
        x and y pixel coordinates for center position on screen.
    
    self.x = x + WIN_WIDTH / 2
        Centers the initial map position.
        
    self.y = y + WIN_HEIGHT / 2
        Centers the initial map position.
    
    self.k = v
        Custom attributes based on u_dict.
    
    self.rect = self.image.get_rect()
        Get Rect from image.
    
    self.rect.center = (self.x, self.y)
        Position the center of the unit at x and y.
    
    self.activated = False
        Tracks whether it currently is this units turn.
    
    Methods:
    --------
    update(self) -> None:
        Update function to be used in combination with the main game loop to
        update the state of the unit.
   
    """
    newid = itertools.count(0,1)
    def __init__(self, game:object, q:int, r:int, s:int, u:str) -> object:
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.id = next(self.newid)
        
        self.q = q
        self.r = r
        self.s = s
        
        self._layer = UNIT_LAYER
        self.game.all_sprites.add(self)
        
        if u[0] == "r":
            self.game.unit_redfor_grp.add(self)
            
        if u[0] == "b":
            self.game.unit_blufor_grp.add(self)
            
        x, y = hl.hex_to_pixel((q,r,s))
        self.x = x + WIN_WIDTH / 2
        self.y = y + WIN_HEIGHT / 2
        
        for k, v in u_dict[u].items():
            if isinstance(v, str):
                setattr(self, k, eval(v))
            else:
                setattr(self, k, v)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.activated = False
            
    def update(self) -> None:
        """
        Update function to be used in combination with the main game loop to
        update the state of the unit.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.
        
        Returns:
        --------
        None
        """
        for tile in self.game.tile_grp:
            if tile.q == self.q:
                if tile.r == self.r:
                    if tile.s == self.s:
                        self.x = tile.x
                        self.y = tile.y
                        
                        if tile.fog_of_war == True:
                            if self.faction == "redfor":
                                self.image.set_alpha(0)
                        else:
                            self.image.set_alpha(255)
                            
        if self.health <= 0:
            self.kill()
        
        self.rect.center = (self.x, self.y)

