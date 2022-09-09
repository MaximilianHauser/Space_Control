# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 06:54:39 2022

Will contain sprite objects and logic

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg

# settings section ---------------------------------------------------------- #
# transparency color
T_PURPLE = (255, 0, 255)

# loads images as img or spritesheet, saves them as attributes -------------- #
class Spritesheet:
    def __init__(self, file):
        self.sheet = pg.image.load(file).convert()
        
    def get_sprite(self, x, y, width, height):

        sprite = pg.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(T_PURPLE)
        return sprite
    
# Button class -------------------------------------------------------------- #
class Button:
    pass

# Tile class ---------------------------------------------------------------- #
# qrs: coordinates, t: terrain_type ----------------------------------------- #
class Tile:
    pass

# Unit class ---------------------------------------------------------------- #
# qrs: coordinates, u: unit_type, f: faction -------------------------------- #
class Unit:
    pass