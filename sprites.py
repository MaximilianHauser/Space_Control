# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 06:54:39 2022

Will contain sprite objects and logic

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from hexlogic import HexLogic as hl
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
        
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.last_click_time = pg.time.get_ticks()
        
        
    def update(self):
        self.rect.center = (self.x, self.y)
    
    def msbtn_down(self, pos, button):
        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        touching = self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask)
        
        current_click_time = pg.time.get_ticks()

        if current_click_time - self.last_click_time >= 500:
            self.last_click_time = current_click_time
            if touching:
                current_click_time = pg.time.get_ticks()
                return True
            return False
        return False

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
        if u[0] == "b":
            self.game.unit_blufor_grp.add(self)
        
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
            
