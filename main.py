# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 10:03:53 2022

Will contain the main game loop and functionality.

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import pygame as pg
import sys

# game files ---------------------------------------------------------------- #
import sprites as sp
import observer as ob
from map_logic import MapLogic as ml
from game_logic import GameLogic as gl
from animations_logic import Animations as al
import win_conditions as rbl
from settings import WIN_WIDTH, WIN_HEIGHT, TILE_WIDTH, TILE_HEIGHT, FPS, FONTSIZE, SCROLL_SPEED, SCROLL_AREA, SCROLL_BUFFER

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
        self.text_crawl_grp = pg.sprite.Group()
        
        # game mechanics variables ------------------------------------------ #
        self.round_counter = 1
        
        # init Observer ----------------------------------------------------- #
        self.observer = ob.Observer()
        
        # init ResolveBattleLogic ------------------------------------------- #
        self.resolver = rbl.ResolveBattleLogic(self)
        
        # define custom_events ---------------------------------------------- #
        self.E_IDLE = pg.event.custom_type() + 0
        self.E_VICTORY = pg.event.custom_type() + 1
        self.E_DEFEAT = pg.event.custom_type() + 2
        
        # function subsriptions to Observer --------------------------------- #
        self.observer.subscribe(pg.QUIT, g)
        self.observer.subscribe(pg.MOUSEMOTION, g)
        self.observer.subscribe(self.E_IDLE, g)
        
        # map loading from file --------------------------------------------- #
        test_map = ml.load_from_json("./missions/test_map/test_map.json")
        self.map_running_dict = {}
        self.map_setup_lst = ml.assign_qrs(test_map)
        
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
        
        # UI initialization ------------------------------------------------- #   
        # End-Turn-Button --------------------------------------------------- #
        end_turn_button = sp.Button(self, "end turn: {a}", 480, 445, 150, 25, True, "gl.end_turn(self.game)", a = (self, "round_counter"))
        self.observer.subscribe(pg.MOUSEBUTTONDOWN, end_turn_button)
        self.observer.subscribe(pg.MOUSEBUTTONUP, end_turn_button)
        self.observer.subscribe(self.E_IDLE, end_turn_button)
        
        # Test_Dialogue ----------------------------------------------------- #
        test_text = "hello world!#hello world!#hello world!#hello world!#hello world!#hello world!"
        colors_index = [0,0,1,0,0,0]
        typewriter_crawl = sp.TypewriterCrawl(self, 100, 50, 300, 60, test_text, colors_index, delete_frames = None)
        self.observer.subscribe(pg.MOUSEBUTTONDOWN, typewriter_crawl)
        self.observer.subscribe(pg.MOUSEBUTTONUP, typewriter_crawl)
        self.observer.subscribe(pg.MOUSEMOTION, typewriter_crawl)
        self.observer.subscribe(self.E_IDLE, typewriter_crawl)
                                
    def events(self):
        
        # post custom_event "victory" or "defeat" after checking conditions - #
        game_status = self.resolver.update_gamestatus()
        if game_status == "victory":
            event_data = dict()
            pg.event.post(pg.event.Event(self.E_VICTORY, event_data))
            print("VVVVV")
        elif game_status == "defeat":
            print("DDDDD")
            event_data = dict()
            pg.event.post(pg.event.Event(self.E_DEFEAT, event_data))
        else:
            pass
        
        # post custom_event "IDLE" ------------------------------------------ #
        if not pg.event.peek(pg.MOUSEMOTION):
            if not pg.event.peek(pg.MOUSEBUTTONDOWN):
                mouse_pos = pg.mouse.get_pos()
                event_data = {'pos': mouse_pos}
                pg.event.post(pg.event.Event(self.E_IDLE, event_data))
        
        # process input / events -------------------------------------------- #
        events = pg.event.get()
    
        # pass events to observer ------------------------------------------- #
        self.observer.event_mngr(events)
        
        # restricts speed of loop ------------------------------------------- #
        self.clock.tick(FPS)
    
    def update(self):
        # update ------------------------------------------------------------ #
        self.all_sprites.update()
        al.set_animation_state(self.tile_grp, [self.unit_blufor_grp, self.unit_redfor_grp])
        self.text_crawl_grp.update()
    
    def draw(self):
        # draw/render ------------------------------------------------------- #
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
        self.text_crawl_grp.draw(self.screen)
        
        # after drawing / flip display -------------------------------------- #
        pg.display.flip()
    
    def main_loop(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
    
    def briefing(self):
        pass
    
    def debriefing(self):
        pass
    
    def defeat(self):
        pass
            

    # event management functions -------------------------------------------- #
    def handle_events(self, event):
        
        # exiting the game via the red x in the top right corner ------------ #
        if event.type == pg.QUIT:
            self.playing = False
            pg.quit()
            sys.exit()
            
        # map scrolling ----------------------------------------------------- #
        if event.type == pg.MOUSEMOTION or event.type == self.E_IDLE:
            mouse_pos_x, mouse_pos_y = event.pos
            max_x, min_x, max_y, min_y = gl.get_map_borders(self.tile_grp)
            
            if mouse_pos_x < SCROLL_AREA:
                if max_x < WIN_WIDTH - SCROLL_BUFFER:
                    for sprite in self.all_sprites:
                        sprite.x += SCROLL_SPEED
            
            if mouse_pos_x > WIN_WIDTH - SCROLL_AREA:
                if min_x > SCROLL_BUFFER:
                    for sprite in self.all_sprites:
                        sprite.x -= SCROLL_SPEED
            
            if mouse_pos_y < SCROLL_AREA:
                if max_y < WIN_HEIGHT - SCROLL_BUFFER:
                    for sprite in self.all_sprites:
                        sprite.y += SCROLL_SPEED
            
            if mouse_pos_y > WIN_HEIGHT - SCROLL_AREA:
                if min_y > SCROLL_BUFFER:
                    for sprite in self.all_sprites:
                        sprite.y -= SCROLL_SPEED
        
        


# top layer ----------------------------------------------------------------- #
g = Game()

g.new_battle()
g.main_loop()


