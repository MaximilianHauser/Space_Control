# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 13:10:09 2023

Main Game Loop to decouple the progression of game time from user input and 
processor speed. A Finite State Machine is used to switch between different 


@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #

# libraries ----------------------------------------------------------------- #
import pygame as pg
import sys


# game files ---------------------------------------------------------------- #
import spritelogic as sl
import observer as ob
from map_logic import MapLogic as ml
import gamelogic as gl
from animations_logic import Animations as al
import win_conditions as rbl
import initiative_queque as iq
import skynet as sn
from settings import WIN_WIDTH, WIN_HEIGHT, SCROLL_SPEED, SCROLL_AREA, SCROLL_BUFFER, FPS, FONTSIZE, TILE_HEIGHT, TILE_WIDTH


# sprite objects ------------------------------------------------------------ #
from tile import Tile
from unit import Unit
from munition import Munition
from button import Button
from typewritercrawl import TypewriterCrawl
from dropdownmenu import DropDownMenu


# Finite State Machine ------------------------------------------------------ #

class State:
    def __init__(self, manager):
        self.manager = manager
 
    def on_init(self, *args):
        """
        Executed when state is manualy set to active via manager.set_state.
        """
        pass
    
    def on_focus(self):
        """
        Executed when this state is set as current state.
        """
        pass
    
    def on_leave(self):
        """
        Executed when this state is replaced with a different state as 
        currently active state.
        """
        pass
 
    
    def on_event(self, event):
        pass
    
    def on_update(self, delta, ticks):
        pass
    
    def on_draw(self, surface):
        pass
 
    def on_quit(self):
        self.manager.quit()
 
class StateMachine:
    def __init__(self, manager):
        self.state = None
        self.manager = manager
        self.next_state = None
 
    def __call__(self):
        self.update()
        if self.state:
            return self.state
        else:
            State(self.manager)
 
    def set(self, state):
        if state:
            if self.state is None:
                state.on_focus()
                self.state = state
            else:
                self.next_state = state
 
    def update(self):
        if self.next_state:
            if self.state:
                self.state.on_leave()
 
            self.state = self.next_state
            self.state.on_focus()
            self.next_state = None
 
class DisplayEngine:
    def __init__(self, manager, caption, width, height, fps, flags):
        pg.display.set_caption(caption)
        pg.display.set_icon(pg.image.load("./img/window_icon.png"))
        self.screen = pg.display.set_mode((width, height), flags)
        self.rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.running = False
        self.delta = 0
        self.fps = fps
 
        self.state_machine = StateMachine(manager)
 
    def loop(self, state=None):
        self.running = True
        self.state_machine.set(state)
 
        while self.running:
            state = self.state_machine()
 
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    state.on_quit()
                else:
                    state.on_event(event)
 
            ticks = pg.time.get_ticks()
            state.on_update(self.delta, ticks)
            state.on_draw(self.screen)
            pg.display.flip()
            self.delta = self.clock.tick(self.fps) * 0.001
 
class StateControl:
    def __init__(self, state, *args):
        self.active = isinstance(state, State)
        self.state = state
        self.args = args
 
    def get(self, manager, *args):
        if not self.active:
            return self.state(manager, *self.args)
 
        return self.state
 
 # Store what to be share across all states
class Manager:
    def __init__(self, caption, width, height, fps=60, flags=0):
        self.engine = DisplayEngine(self, caption, width, height, fps, flags)
        
        # fonts ------------------------------------------------------------- #
        self.font1 = pg.font.Font("img/coalition.ttf", FONTSIZE)
        self.font2 = pg.font.Font("img/berlinsmallcaps.ttf", FONTSIZE)
        
        # setup sprite groups ----------------------------------------------- #
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.tile_grp = pg.sprite.Group()
        self.unit_blufor_grp = pg.sprite.Group()
        self.unit_redfor_grp = pg.sprite.Group()
        self.munition_grp = pg.sprite.Group()
        self.movement_grp = pg.sprite.Group()
        self.ui_mapinfo_grp = pg.sprite.Group()
        self.ui_buttons_grp = pg.sprite.Group()
        self.text_crawl_grp = pg.sprite.Group()
        
        # init Observer ----------------------------------------------------- #
        self.observer = ob.Observer()
        
        # define custom_events ---------------------------------------------- #
        self.E_IDLE = pg.event.custom_type() + 0
        self.E_VICTORY = pg.event.custom_type() + 1
        self.E_DEFEAT = pg.event.custom_type() + 2
 
    def run(self, state=None):
        self.engine.loop(state)
 
    def set_state(self, state, *args):
        if isinstance(state, State):
            state.on_init(*args)
            self.engine.state_machine.next_state = state
        else:
            print("Must be state or state key")
 
    def quit(self):
        self.engine.running = False
        
        
class NewBattle(State):
    def __init__(self, manager):
        super().__init__(manager)

        self.manager = manager
        
        # add battle specific attributes to manager ------------------------- #
        battle_specific_pre = {
            
            # background images --------------------------------------------- #
            "background_battle" : "pg.image.load('./img/background_battle.png')",
            
            # spritesheets -------------------------------------------------- #
            "terrain_sheet" : "sl.Spritesheet('img/hex_terrain_sheet.png')",
            "blufor_sheet" : "sl.Spritesheet('img/hex_blufor_sheet.png')",
            "redfor_sheet" : "sl.Spritesheet('img/hex_redfor_sheet.png')",
            
            # terrain sprites ----------------------------------------------- #
            "sprite_space" : "manager.terrain_sheet.get_sprite(0, 0, TILE_WIDTH, TILE_HEIGHT)",
            "sprite_asteroids" : "manager.terrain_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)",
            "sprite_big_roid" : "manager.terrain_sheet.get_sprite(130, 0, TILE_WIDTH, TILE_HEIGHT)",
            "sprite_micro_roids" : "manager.terrain_sheet.get_sprite(195, 0, TILE_WIDTH, TILE_HEIGHT)",
            "sprite_tile_mask" : "manager.terrain_sheet.get_sprite(260, 0, TILE_WIDTH, TILE_HEIGHT)",
            
            # unit sprites -------------------------------------------------- #
            # BLUFOR -------------------------------------------------------- #
            "sprite_blufor_CC" : "manager.blufor_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)",
            # REDFOR -------------------------------------------------------- #
            "sprite_redfor_CC" : "manager.redfor_sheet.get_sprite(65, 0, TILE_WIDTH, TILE_HEIGHT)",
            
            # game mechanics variables ------------------------------------------ #
            "round_counter" : 1,
            
            # init ResolveBattleLogic ------------------------------------------- #
            "resolver" : "rbl.ResolveBattleLogic(self.manager)"
            }
        
        for k, v in battle_specific_pre.items():
            if isinstance(v, str):
                setattr(manager, k, eval(v))
            else:
                setattr(manager, k, v)
        
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
            tile = Tile(self.manager, q, r, s, t)
            self.manager.observer.subscribe(pg.MOUSEBUTTONDOWN, tile)
            
            if u != None:
                Unit(manager, q, r, s, u)

        # add battle specific attributes to manager ------------------------- #
        battle_specific_aft = {
            
            # initialize initiative_queque -------------------------------------- #
            "initiative_queque" : "iq.InitiativeQueque(manager)",
            "iqsa" : "manager.initiative_queque.set_unit_attr(activated = True)",
            
            # initialize AI ----------------------------------------------------- #
            "skynet" : "sn.Skynet(manager)",
            
            # UI initialization ------------------------------------------------- #   
            # End-Turn-Button --------------------------------------------------- #
            "skip_turn_button" : 'Button(manager, "skip turn {a}", 480, 445, 150, 25, True, "gl.skip_turn(self.manager)", a = (manager, "round_counter"))',
            "os1" : "manager.observer.subscribe(pg.MOUSEBUTTONDOWN, manager.skip_turn_button)",
            "os2" : "manager.observer.subscribe(pg.MOUSEBUTTONUP, manager.skip_turn_button)",
            "os3" : "manager.observer.subscribe(manager.E_IDLE, manager.skip_turn_button)"
            
            }
        
        for k, v in battle_specific_aft.items():
            if isinstance(v, str):
                setattr(manager, k, eval(v))
            else:
                setattr(manager, k, v)
        
    def on_update(self, delta, ticks):
        self.manager.set_state(battle_input)
        
    
class BattleUserInput(State):
    def __init__(self, manager):
        super().__init__(manager)
        
        # function subsriptions to Observer --------------------------------- #
        self.manager.observer.subscribe(pg.QUIT, self)
        self.manager.observer.subscribe(pg.MOUSEMOTION, self)
        self.manager.observer.subscribe(self.manager.E_IDLE, self)

 
    def on_event(self, event):
        # post custom_event "victory" or "defeat" after checking conditions - #
        game_status = self.manager.resolver.update_gamestatus()
        if game_status == "victory":
            event_data = dict()
            pg.event.post(pg.event.Event(self.manager.E_VICTORY, event_data))
            print("VVVVV")
        elif game_status == "defeat":
            event_data = dict()
            pg.event.post(pg.event.Event(self.manager.E_DEFEAT, event_data))
            print("DDDDD")
        else:
            pass
        
        # post custom_event "IDLE" ------------------------------------------ #
        if not pg.event.peek(pg.MOUSEMOTION):
            if not pg.event.peek(pg.MOUSEBUTTONDOWN):
                mouse_pos = pg.mouse.get_pos()
                event_data = {'pos': mouse_pos}
                pg.event.post(pg.event.Event(self.manager.E_IDLE, event_data))
    
        # pass events to observer ------------------------------------------- #
        self.manager.observer.event_mngr(event)
 
    def on_update(self, delta, ticks):
        self.manager.initiative_queque.check_unit_ap()
        self.manager.skynet.get_situation()
        
        mun_sprite_lst = self.manager.munition_grp.sprites()
        mov_sprite_lst = self.manager.movement_grp.sprites()
        
        if not mun_sprite_lst and not mov_sprite_lst:
            self.manager.skynet.red_active_next_action()
        
        self.manager.all_sprites.update()
        al.set_animation_state_tiles(self.manager.tile_grp, [self.manager.unit_blufor_grp, self.manager.unit_redfor_grp])
        self.manager.text_crawl_grp.update()
        
        # switch state to animation if movement or attack animation --------- #
        if mun_sprite_lst or mov_sprite_lst:
            self.manager.set_state(battle_animation)
    
    def on_draw(self, surface):
        # draw/render ------------------------------------------------------- #
        self.manager.engine.screen.blit(self.manager.background_battle, (0, 0))
        self.manager.all_sprites.draw(self.manager.engine.screen)
        self.manager.text_crawl_grp.draw(self.manager.engine.screen)
        
    def handle_events(self, event):
        ml.scroll_logic(self.manager, event)
    
    
class BattleAnimation(State):
    def __init__(self, manager):
        super().__init__(manager)

 
    def on_event(self, event):
        pass
 
    def on_update(self, delta, ticks):
        
        self.manager.all_sprites.update()
        al.set_animation_state_tiles(self.manager.tile_grp, [self.manager.unit_blufor_grp, self.manager.unit_redfor_grp])
        self.manager.text_crawl_grp.update()
        
        # switch state to input if animation is concluded ------------------- #
        mun_sprite_lst = self.manager.munition_grp.sprites()
        mov_sprite_lst = self.manager.movement_grp.sprites()
        
        if not mun_sprite_lst and not mov_sprite_lst:
            self.manager.set_state(battle_input)
    
    def on_draw(self, surface):
        # draw/render ------------------------------------------------------- #
        self.manager.engine.screen.blit(self.manager.background_battle, (0, 0))
        self.manager.all_sprites.draw(self.manager.engine.screen)
        self.manager.text_crawl_grp.draw(self.manager.engine.screen)
    
    
if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    manager = Manager("Space Control", WIN_WIDTH, WIN_HEIGHT, fps=FPS)
    new_battle = NewBattle(manager)
    battle_input = BattleUserInput(manager)
    battle_animation = BattleAnimation(manager)
    manager.run(new_battle)
    pg.quit()