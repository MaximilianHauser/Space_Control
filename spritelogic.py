# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:29:50 2023

Allows to cut sprites from spriteseets. Provides an object that loads an image 
and saves it as an attribute, from which smaller images can be cut out and 
saved as new attributes.

Dependencies:
-------------
pygame - Community Edition
    pip install pygame-ce
    
settings
    Containing constant for T_PURPLE.

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from settings import T_PURPLE

# Spritesheet class --------------------------------------------------------- #
class Spritesheet:
    """
    Creates an object that loads an image and saves it as an attribute, from 
    which smaller images can be cut out and saved as new attributes.
    
    Attributes:
    -----------
    self.sheet = pg.image.load(file).convert()
        Main game loop object.
    
    Methods:
    --------
    get_sprite(self, x:int, y:int, width:int, height:int) -> object:
        Returns a cutout from a spritesheet, to be used as an image in pygame.
   
    """
    def __init__(self, file:str) -> object:
        self.sheet = pg.image.load(file).convert()
        
    def get_sprite(self, x:int, y:int, width:int, height:int) -> object:

        sprite = pg.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(T_PURPLE)
        
        return sprite
