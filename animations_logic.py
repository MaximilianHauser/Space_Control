# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:54:56 2022

will contain animation logic

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg

# Animations class contains animation functions ----------------------------- #
class Animations:
    
    # tinting a sprite in a certain colorshade ------------------------------ #
    def tint_image(image, color):
        colored_image = pg.Surface(image.get_size())
        colored_image.fill(color)
        
        tinted_image = image.copy()
        
        tinted_image.blit(colored_image, (0, 0), special_flags = pg.BLEND_MULT)
        colorkey = tinted_image.get_at((0,0))
        tinted_image.set_colorkey(colorkey)
        
        return tinted_image
