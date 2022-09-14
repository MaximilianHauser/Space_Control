# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 06:54:39 2022

Will contain sprite objects and logic

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from hexlogic import HexLogic as hl
from settings import T_PURPLE, TERRAIN_LAYER, UNIT_LAYER, WIN_WIDTH, WIN_HEIGHT, TILE_WIDTH, TILE_HEIGHT

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
    pass

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
        
        if t == "s":
            self.image = self.game.sprite_space
            self.dmg_to_light = 0
            self.dmg_to_medium = 0
            self.dmg_to_heavy = 0
            self.block_move = False
            self.block_sight = False
        if t == "m":
            self.image = self.game.sprite_micro_roids
            self.dmg_to_light = 0.25
            self.dmg_to_medium = 0
            self.dmg_to_heavy = 0
            self.block_move = False
            self.block_sight = False
        if t == "a":
            self.image = self.game.sprite_asteroids
            self.dmg_to_light = 0
            self.dmg_to_medium = 0.5
            self.dmg_to_heavy = 0.05
            self.block_move = False
            self.block_sight = False
        if t == "b":
            self.image = self.game.sprite_big_roid
            self.dmg_to_light = 0
            self.dmg_to_medium = 0
            self.dmg_to_heavy = 0
            self.block_move = True
            self.block_sight = True
            
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
                return (self.q, self.r, self.s)
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
        
        if u == "b_cc":
            self.image = self.game.sprite_blufor_CC
            self.ship_size_light = False
            self.ship_size_medium = False
            self.ship_size_heavy = True
            
            self.max_health = 10
            self.health = 10
            self.dmg_per_shot = 10
            self.starting_ap = 1
            self.action_points = 1
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.activated = False
        
    def move(self, n_q, n_r, n_s):
        if self.action_points >= 1:
            self.q = n_q
            self.r = n_r
            self.s = n_s
            self.action_points -= 1