# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 06:54:39 2022

Will contain sprite objects and logic

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from hexlogic import HexLogic as hl
from game_logic import GameLogic as gl
from animations_logic import Animations as an
from settings import T_PURPLE, TERRAIN_LAYER, UNIT_LAYER, WIN_WIDTH, WIN_HEIGHT, UI_TRANSPARENCY, FONTSIZE, UI_INTERFACE_LAYER


# sprite type specific attributes dicts ------------------------------------- #
from t_attr import t_dict
from u_attr import u_dict


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
    def __init__(self,game, text, x, y, width, height, enabled, m_pos, m_click):
        self.game = game
        
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.enabled = enabled
        self.m_pos = m_pos
        self.m_click = m_click
        
        self.surface = pg.Surface((self.width, self.height))
        self.surface.set_alpha(UI_TRANSPARENCY)
        self.surface.fill(T_PURPLE)
        self.surface.set_colorkey(T_PURPLE)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def draw(self):    
        button_text = self.game.font.render(self.text, True, 'white')
        if self.enabled:
            if self.msbtn_down(self.m_pos) and self.m_click:
                pg.draw.rect(self.surface, 'darkslategray4', ((0,0), (self.width, self.height)), 0, 5)
                pg.draw.rect(self.surface, 'darkslategray1', ((0,0), (self.width, self.height)), 2, 5)
            else:
                pg.draw.rect(self.surface, 'darkslategray3', ((0,0), (self.width, self.height)), 0, 5)
                pg.draw.rect(self.surface, 'darkslategray1', ((0,0), (self.width, self.height)), 2, 5)
        else:
            self.kill()
        pg.draw.rect(self.surface, 'darkslategray1', ((0,0), (self.width, self.height)), 2, 5)
        self.surface.blit(button_text, (10, (self.height - FONTSIZE) * 0.75))
        
        self.game.screen.blit(self.surface, (self.x, self.y))
        
    def msbtn_down(self, pos, button):
        
        if self.rect.collidepoint(pos) and self.enabled:
            return True
        else:
            return False


# Tile class ---------------------------------------------------------------- #
# qrs: coordinates, t: terrain_type ----------------------------------------- #
class Tile(pg.sprite.Sprite):
    def __init__(self, game, q, r, s, t):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.q = q
        self.r = r
        self.s = s
        
        self.t = t
        
        self._layer = TERRAIN_LAYER
        self.game.all_sprites.add(self)
        self.game.tile_grp.add(self)
        
        x, y = hl.hex_to_pixel(q,r,s)
        self.x = x + WIN_WIDTH / 2
        self.y = y + WIN_HEIGHT / 2
        
        for k, v in t_dict[t].items():
            if isinstance(v, str):
                setattr(self, k, eval(v))
            else:
                setattr(self, k, v)
        
        self.image = self.original_image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.last_click_time = 0
        self.unit = None
        
        
    def update(self):
        
        # attaching unit to tile if occupied -------------------------------- #
        for unit in self.game.unit_blufor_grp:
            if unit.q == self.q and unit.r == self.r and unit.s == self.s:
                self.unit = unit
            else:
                self.unit = None
           
        # tints tile in case of activated unit on it ------------------------ #
        activated_unit = gl.is_activated_unit(self.game.unit_blufor_grp)
        
        if self.unit is not None:
            if self.unit.activated == True:
                self.image = an.tint_image(self.original_image, "azure2")
            else:
                self.image = self.original_image
        
        # tints tile in case of in movement range of an activated unit ------ #
        elif activated_unit is not None:
            in_range = gl.in_mov_range(self, self.game.unit_blufor_grp, self.game.tile_grp, "block_move")
            if in_range:
                self.image = an.tint_image(self.original_image, "yellow")
            else:
                self.image = self.original_image
        else:
            self.image = self.original_image
           
        # updates position -------------------------------------------------- #
        self.rect.center = (self.x, self.y)
    
    # checks if click is touching tile and click cooldown ------------------- #
    def msbtn_down(self, pos, button):

        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        touching = self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask)
        
        current_click_time = pg.time.get_ticks()

        if current_click_time - self.last_click_time >= 500:

            if touching:

                self.last_click_time = pg.time.get_ticks()
                return True
            return False
        return False
    
    # click on maptile management ------------------------------------------- #
    def handle_events(self, event):
        
        # handle events related to mouse clicks on tile --------------------- #
        if event.type == pg.MOUSEBUTTONDOWN:
            
            # variables for wether or not there is a unit on the tile ------- #
            blufor_activated = None
            blufor_on_tile = False
            unit_on_tile = None
            for unit in self.game.unit_blufor_grp:
                if unit.q == self.q and unit.r == self.r and unit.s == self.s:
                    blufor_on_tile = True
                    unit_on_tile = unit
                if unit.activated == True:
                    blufor_activated = unit
                    
            redfor_on_tile = False
            for unit in self.game.unit_redfor_grp:
                if unit.q == self.q and unit.r == self.r and unit.s == self.s:
                    redfor_on_tile = True
                    unit_on_tile = unit
                    
            # left click on tile -------------------------------------------- #
            if event.button == 1:
                
                # blufor unit on tile --------------------------------------- #
                if blufor_on_tile:
                    for unit in self.game.unit_blufor_grp:
                        if unit is not unit_on_tile:
                            unit.activated = False
                    unit_on_tile.activated = not unit_on_tile.activated                  
                
                # redfor unit on tile --------------------------------------- #
                if redfor_on_tile:
                    pass
                
                # no unit on tile ------------------------------------------- #
                if unit_on_tile is None:
                    if blufor_activated is not None:
                        in_range = gl.in_mov_range(self, self.game.unit_blufor_grp, self.game.tile_grp, "block_move")
                        if in_range:
                            gl.move_unit(self, blufor_activated)
                
            if event.button == 3:
                pass
    
    

# Unit class ---------------------------------------------------------------- #
# qrs: coordinates, u: unit_type, f: faction -------------------------------- #
class Unit(pg.sprite.Sprite):
    def __init__(self, game, q, r, s, u):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.q = q
        self.r = r
        self.s = s
        
        self._layer = UNIT_LAYER
        self.game.all_sprites.add(self)
        if u[0] == "r":
            self.game.unit_redfor_grp.add(self)
            self.faction = "redfor"
        if u[0] == "b":
            self.game.unit_blufor_grp.add(self)
            self.faction = "blufor"
        
        x, y = hl.hex_to_pixel(q,r,s)
        self.x = x + WIN_WIDTH / 2
        self.y = y + WIN_HEIGHT / 2
        
        for k, v in u_dict[u].items():
            if isinstance(v, str):
                setattr(self, k, eval(v))
            else:
                setattr(self, k, v)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.activated = False
            
    def update(self):
        for tile in self.game.tile_grp:
            if tile.q == self.q:
                if tile.r == self.r:
                    if tile.s == self.s:
                        self.x = tile.x
                        self.y = tile.y
        
        self.rect.center = (self.x, self.y)
            
