# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 10:33:21 2022

@author: Maximilian
"""

# global settings ----------------------------------------------------------- #

# screen dimensions
WIN_WIDTH = 1000 #324 #640
WIN_HEIGHT = 1000 #720 #480

# times the screen is updated per min
FPS = 60

# tilesize
TILE_WIDTH = 64
TILE_HEIGHT = 64

# transparency color
T_PURPLE = (255, 0, 255)

# fontsize
FONTSIZE = 14

# ui_transparency
UI_TRANSPARENCY = 100
UI_TRANSPARENCY_PRESSED = 200

# layers for animation
BACKGROUND_LAYER = 1
TERRAIN_LAYER = 2
T_ANIMATION_LAYER = 3
UNIT_LAYER = 4
U_ANIMATION_LAYER = 5
UI_MAPINFO_LAYER = 6
UI_INTERFACE_LAYER = 7

# attributes, related to scrolling the map
SCROLL_SPEED = 2
SCROLL_AREA = 48
SCROLL_BUFFER = 48
