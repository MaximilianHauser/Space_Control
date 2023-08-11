# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 10:33:21 2022

Contains all global constants.

@author: Maximilian Hauser
"""

# global settings ----------------------------------------------------------- #

# screen dimensions
WIN_WIDTH = 640 #324 #640
WIN_HEIGHT = 480 #720 #480

# times the screen is updated per min
FPS = 60

# tilesize
TILE_WIDTH = 64
TILE_HEIGHT = 64

# transparency color
T_PURPLE = (255, 0, 255)

# fontsize
DEFAULT_FONTSIZE = 38

# ui_transparency
UI_TRANSPARENCY = 100

# layers for animation
BACKGROUND_LAYER = 1
TERRAIN_LAYER = 2
T_ANIMATION_LAYER = 3
UNIT_LAYER = 4
U_ANIMATION_LAYER = 5
UI_MAPINFO_LAYER = 6
UI_INTERFACE_LAYER = 7

# relative speed for mousewheel scrolling
MOUSESCROLLSPEED = 3

# attributes, related to scrolling the map
SCROLL_SPEED = 3
SCROLL_AREA = 48
SCROLL_BUFFER = 48

# color and font schemes in a dict, to be used as templates
ui_colors_dict = {"transp_white":
                 {                 
                                    "active_font" : None,
                                    "un_text_col" : "white",
                                    "hov_text_col" : "darkslategray1",
                                    "pres_text_col" : "darkslategray3",
                                    "un_fill_col" : "black",
                                    "hov_fill_col" : "black",
                                    "pres_fill_col" : "black",
                                    "un_border_col" : "black",
                                    "hov_border_col" : "black",
                                    "pres_border_col" : "black"
                                    },
                  
                  "solid_darkslate":     
                {
                                    "active_font" : None,
                                    "un_text_col" : "white",
                                    "hov_text_col" : "white",
                                    "pres_text_col" : "white",
                                    "un_fill_col" : "darkslategray3",
                                    "hov_fill_col" : "darkslategray4",
                                    "pres_fill_col" : "darkslategray",
                                    "un_border_col" : "darkslategray1",
                                    "hov_border_col" : "darkslategray1",
                                    "pres_border_col" : "darkslategray1"
                                    }
    
                
                    }


