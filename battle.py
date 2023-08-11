# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 15:30:43 2023

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from state import State
from observer import Observer
import map_logic as ml
from tile import Tile
import spritelogic as sl
from settings import TILE_WIDTH, TILE_HEIGHT

# battle state -------------------------------------------------------------- #
class Battle(State):
    def __init__(self):
        super(Battle, self).__init__()
        
        # background images --------------------------------------------- #
        self.background_battle = pg.image.load('./img/background_battle.png')
        
        # spritesheets -------------------------------------------------- #
        self.terrain_sheet = sl.Spritesheet('img/hex_terrain_sheet.png')
        self.blufor_sheet = sl.Spritesheet('img/hex_blufor_sheet.png')
        self.redfor_sheet = sl.Spritesheet('img/hex_redfor_sheet.png')
        
        # terrain sprites ----------------------------------------------- #
        self.sprite_space = self.terrain_sheet.get_sprite(0, 0, TILE_WIDTH, TILE_HEIGHT)
        self.sprite_asteroids = self.terrain_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)
        self.sprite_big_roid = self.terrain_sheet.get_sprite(130, 0, TILE_WIDTH, TILE_HEIGHT)
        self.sprite_micro_roids = self.terrain_sheet.get_sprite(195, 0, TILE_WIDTH, TILE_HEIGHT)
        self.sprite_tile_mask = self.terrain_sheet.get_sprite(260, 0, TILE_WIDTH, TILE_HEIGHT)
        
        # unit sprites -------------------------------------------------- #
        # BLUFOR -------------------------------------------------------- #
        self.sprite_blufor_CC = self.blufor_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)
        # REDFOR -------------------------------------------------------- #
        self.sprite_redfor_CC = self.redfor_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)
        
        # setup sprite groups ----------------------------------------------- #
        self.tile_group = pg.sprite.Group()
        self.unit_blufor_group = pg.sprite.Group()
        self.unit_redfor_group = pg.sprite.Group()
        self.munition_group = pg.sprite.Group()
        self.movement_group = pg.sprite.Group()
        self.ui_mapinfo_group = pg.sprite.Group()
        self.ui_buttons_group = pg.sprite.Group()
        self.text_crawl_group = pg.sprite.Group()
        
        # gameplayphases management variables ------------------------------- #
        self.phase = None
        self.phases = {"dialogue":None,
                       "player_input":None,
                       "animation":None,
                       "skynet_move":None,
                       "victory_conditions":None
                        }
        
        # define custom_events ---------------------------------------------- #
        self.E_IDLE = pg.event.custom_type() + 0
        self.E_VICTORY = pg.event.custom_type() + 1
        self.E_DEFEAT = pg.event.custom_type() + 2
        
        # observer for event management ------------------------------------- #
        self.observer = Observer()
        
        # dict for logging last state of map -------------------------------- #
        self.map_running_dict = dict()
        
    
    def startup(self, persistent):
        self.persistent = persistent
        
        # get mission files from folder ------------------------------------- #
        map_path = ".\missions\\" + str(self.persistent["selected_mission"] + "\\map.json")
        map_list = ml.load_from_json(map_path)
        map_setup_lst = ml.assign_qrs(map_list)
        
        # sprite initialization --------------------------------------------- #
        for i in range(len(map_setup_lst)):
            q, r, s, t, u = map_setup_lst[i]
            
            # adding map logic to running_dict ------------------------------ #
            self.map_running_dict.update({(q,r,s):[t,u]})
            
            # creating Tile and Unit sprite objects ------------------------- #
            tile = Tile(self, q, r, s, t)
            self.observer.subscribe(pg.MOUSEBUTTONDOWN, tile)


    def event(self, event):
        pass
        
    def update(self, delta):
        self.all_sprites.update(delta)
        
    def draw(self, surface):
        surface.fill("black") #"gray30" as placeholder if needed
        self.all_sprites.draw(surface)
    
