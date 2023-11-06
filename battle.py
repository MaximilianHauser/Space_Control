# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 15:30:43 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import pygame as pg

# custom functions ---------------------------------------------------------- #
import animations_logic as al
import map_logic as ml
import gamelogic as gl
import spritelogic as sl
import hexlogic as hl

# algorithm objects --------------------------------------------------------- #
from state import State
from observer import Observer
from win_conditions import ResolveBattleLogic
from initiative_queque import InitiativeQueque
from skynet import Skynet
from eventslogic import EventsLogic

# sprite objects ------------------------------------------------------------ #
from button import Button
from tile import Tile
from unit import Unit

# misc ---------------------------------------------------------------------- #
from settings import WIN_WIDTH, TILE_WIDTH, TILE_HEIGHT, UI_TRANSPARENCY


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
        
        self.round_counter = 1
        
        # define custom_events ---------------------------------------------- #
        self.E_VICTORY = pg.event.custom_type() + 1
        self.E_DEFEAT = pg.event.custom_type() + 2
        
        # battle conclusion variable ---------------------------------------- #
        self.battle_conclusion = None
        self.selected_mission = None
        
        # variable to descern state change ---------------------------------- #
        self.clicked_on = None
        
        # observer for event management ------------------------------------- #
        self.observer = Observer()
        
        # dict for logging last state of map -------------------------------- #
        self.map_running_dict = dict()
        
        # state subsriptions to Observer ------------------------------------ #
        self.observer.subscribe(pg.MOUSEMOTION, self)
        self.observer.subscribe(self.E_IDLE, self)
        
        # init ResolveBattleLogic ------------------------------------------- #
        self.resolver = ResolveBattleLogic(self)
        
        # placeholder variable for initiative_queque ------------------------ #
        self.initiative_queque = None
        
        # placeholder variable for AI --------------------------------------- #
        self.skynet = None
        
        # placeholder variable for EventsLogic ------------------------------ #
        self.events_logic = None
        
        # UI initialization ------------------------------------------------- #   
        # End-Turn-Button --------------------------------------------------- #
        self.skip_turn_button = Button(self, "skip turn", WIN_WIDTH - 135, 400, "clicked_on", "skip_turn", ["all_sprites"], 
                                   predefined_color_scheme = "solid_darkslate", transparency=UI_TRANSPARENCY, 
                                   active_font=self.font_smallcaps, font_size=24)
        self.observer.subscribe(pg.MOUSEBUTTONDOWN, self.skip_turn_button)
        self.observer.subscribe(pg.MOUSEBUTTONUP, self.skip_turn_button)
        self.observer.subscribe(self.E_IDLE, self.skip_turn_button)
        
        # subscription to E_VICTORY and E_DEFEAT for state management ------- #
        self.observer.subscribe(self.E_VICTORY, self)
        self.observer.subscribe(self.E_DEFEAT, self)
        
        # persistant dictionary to be carried over to debriefing ------------ #
        self.persistent = {"selected_mission":self.selected_mission, 
                           "battle_conclusion":self.battle_conclusion}
        
    
    def startup(self, persistent):
        self.persistent.update(persistent)
        self.selected_mission = self.persistent["selected_mission"]
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
            
            if u != None:
                Unit(self, q, r, s, u)
                
        # initialize initiative_queque -------------------------------------- #
        self.initiative_queque = InitiativeQueque(self)
        self.initiative_queque.set_unit_attr(activated = True)
        
        # initialize AI ----------------------------------------------------- #
        self.skynet = Skynet(self)
        
        # initialize EventsLogic -------------------------------------------- #
        self.events_logic = EventsLogic(self)


    def event(self, event, delta):
        # block events while movement or attack in progress ----------------- #
        mun_sprite_lst = self.munition_group.sprites()
        mov_sprite_lst = self.movement_group.sprites()
        if not mun_sprite_lst and not mov_sprite_lst:
            # post custom_event "victory" or "defeat" after checking conditions - #
            game_status = self.resolver.update_gamestatus()
            if game_status == "victory":
                event_data = dict()
                pg.event.post(pg.event.Event(self.E_VICTORY, event_data))
            elif game_status == "defeat":
                event_data = dict()
                pg.event.post(pg.event.Event(self.E_DEFEAT, event_data))
            else:
                pass
            
            # pass events to observer ------------------------------------------- #
            self.observer.event_mngr(event, delta)
        
    def update(self, delta):
        self.initiative_queque.check_unit_ap()
        self.skynet.get_situation()
        
        self.all_sprites.update(delta)
        al.set_animation_state_tiles(self.tile_group, [self.unit_blufor_group, self.unit_redfor_group])
        
        # block actions redfor while animation of movement or attack in prog  #
        mun_sprite_lst = self.munition_group.sprites()
        mov_sprite_lst = self.movement_group.sprites()
        if not mun_sprite_lst and not mov_sprite_lst:
            self.skynet.red_active_next_action()
            
        # connected states -------------------------------------------------- #
        if self.clicked_on == "victory":
            self.to_debriefing_v()
        elif self.clicked_on == "defeat":
            self.to_debriefing_d()
        
        # game mechanics button --------------------------------------------- #
        elif self.clicked_on == "skip_turn":
            self.skip_turn()
            self.clicked_on = None
        
    def draw(self, surface):
        surface.fill("black") #"gray30" as placeholder if needed
        self.all_sprites.draw(surface)
    
    def handle_events(self, event, delta):
        # map scroll mechanic ----------------------------------------------- #
        if event.type == pg.MOUSEMOTION or event.type == self.E_IDLE:
            ml.scroll_logic(self, event, delta)
        # victory and defeat events, change state --------------------------- #
        elif event.type == self.E_VICTORY:
            self.clicked_on = "victory"
        elif event.type == self.E_DEFEAT:
            self.clicked_on = "defeat"

    def to_debriefing_v(self):
        self.next_state = "DEBRIEFING"
        self.battle_conclusion = "victory"
        self.done = True
    
    def to_debriefing_d(self):
        self.next_state = "DEBRIEFING"
        self.battle_conclusion = "defeat"
        self.done = True
        
    def skip_turn(self):
        gl.skip_turn(self)

