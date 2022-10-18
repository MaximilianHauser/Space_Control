# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 10:03:53 2022

Will contain the main game loop and functionality.

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg
import sys
import sprites as sp
from hexlogic import HexLogic as hl
import observer as ob
from settings import WIN_WIDTH, WIN_HEIGHT, TILE_WIDTH, TILE_HEIGHT, FPS, FONTSIZE

# game class ---------------------------------------------------------------- #
class Game:
    def __init__(self):

        # initialize all imported pygame modules / init sounds module ------- #
        pg.init()
        pg.mixer.init()
        
        # Setup pygame / window --------------------------------------------- #
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.caption = pg.display.set_caption('Space Control')
        self.window_icon = pg.display.set_icon(pg.image.load('./img/window_icon.png'))
        self.clock = pg.time.Clock()
        
        # fonts ------------------------------------------------------------- #
        self.font = pg.font.Font('img/coalition.ttf', FONTSIZE)
        
        # spritesheets ------------------------------------------------------ #
        self.terrain_sheet = sp.Spritesheet('img/hex_terrain_sheet.png')
        self.blufor_sheet = sp.Spritesheet('img/hex_blufor_sheet.png')
        self.redfor_sheet = sp.Spritesheet('img/hex_redfor_sheet.png')

        # terrain sprites --------------------------------------------------- #
        self.sprite_space = self.terrain_sheet.get_sprite(0, 0, TILE_WIDTH, TILE_HEIGHT)
        self.sprite_asteroids = self.terrain_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)
        self.sprite_big_roid = self.terrain_sheet.get_sprite(130, 0, TILE_WIDTH, TILE_HEIGHT)
        self.sprite_micro_roids = self.terrain_sheet.get_sprite(195, 0, TILE_WIDTH, TILE_HEIGHT)
        
        # unit sprites ------------------------------------------------------ #
        # BLUFOR ------------------------------------------------------------ #
        self.sprite_blufor_CC = self.blufor_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)
        # REDFOR ------------------------------------------------------------ #
        self.sprite_redfor_CC = self.redfor_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)
        
    def new_battle(self):
        self.playing = True
        
        # setup sprite groups ----------------------------------------------- #
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.tile_grp = pg.sprite.Group()
        self.unit_blufor_grp = pg.sprite.Group()
        self.unit_redfor_grp = pg.sprite.Group()
        self.ui_buttons_grp = pg.sprite.Group()
        
        # init Observer ----------------------------------------------------- #
        self.observer = ob.Observer()
        
        # function subsriptions to Observer --------------------------------- #
        self.observer.subscribe(pg.QUIT, g)
        
        # map loading from file --------------------------------------------- #
        self.map_running_dict = {}
        self.map_setup_lst = [(0,0,0,"b",None), (0,-1,1,"s",None), (1,-1,0,"b",None), (1,0,-1,"a",None), (0,1,-1,"s",None), (-1, 1, 0, "m", None), (-1, 0, 1, "a", None), (0,-2,2,"s",None), (1,-2,1,"s",None), (2,-2,0,"s",None), (2,-1,-1,"s",None), (2,0,-2,"s",None), (1,1,-2,"s",None), (0,2,-2,"s","b_cc"), (-1,2,-1,"s",None), (-2,2,0,"s",None), (-2,1,1,"s",None), (-2,0,2,"s",None), (-1,-1,2,"s",None)]
        
        # sprite initialization --------------------------------------------- #
        for i in range(len(self.map_setup_lst)):
            q, r, s, t, u = self.map_setup_lst[i]
            
            # adding map logic to running_dict ------------------------------ #
            self.map_running_dict.update({(q,r,s):[t,u]})
            
            # creating Tile and Unit sprite objects ------------------------- #
            tile = sp.Tile(self, q, r, s, t)
            self.observer.subscribe(pg.MOUSEBUTTONDOWN, tile)
            
            if u != None:
                sp.Unit(self, q, r, s, u)
                
                                
    def events(self):
        
        # process input / events -------------------------------------------- #
        events = pg.event.get()
        self.observer.event_mngr(events)
        
        # restricts speed of loop ------------------------------------------- #
        self.clock.tick(FPS)
    
    def update(self):
        # update ------------------------------------------------------------ #
        self.all_sprites.update()
    
    def draw(self):
        # draw/render ------------------------------------------------------- #
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
        
        # after drawing / flip display -------------------------------------- #
        pg.display.flip()
    
    def main_loop(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            

    # event management functions -------------------------------------------- #
    def handle_events(self, event):
        if event.type == pg.QUIT:
            self.playing = False
        


# top layer ----------------------------------------------------------------- #
g = Game()

g.new_battle()
g.main_loop()

pg.quit()
sys.exit()

