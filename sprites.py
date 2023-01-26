# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 06:54:39 2022

Will contain sprite objects and logic

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import string as string_module
import pygame as pg
from hexlogic import HexLogic as hl
from game_logic import GameLogic as gl
from animations_logic import Animations as an
from settings import T_PURPLE, TERRAIN_LAYER, UNIT_LAYER, WIN_WIDTH, WIN_HEIGHT, UI_TRANSPARENCY, UI_TRANSPARENCY_PRESSED, FONTSIZE, UI_INTERFACE_LAYER


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
    
    
# Button Class -------------------------------------------------------------- #
class Button(pg.sprite.Sprite):
    def __init__(self, game, text_in, x, y, width, height, enabled, function, **kwargs):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.text_in = text_in
        
        self.var_dict = kwargs
        self.attr_dict = dict()
        
        for k, v in kwargs.items():
            attr_v = getattr(v[0], v[1])
            setattr(self, k, attr_v)
            self.attr_dict.update({k:attr_v}) 
             
        self.text_out = text_in.format(**self.attr_dict)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._layer = UI_INTERFACE_LAYER
        
        self.game.all_sprites.add(self)
        self.game.ui_buttons_grp.add(self)
        
        self.enabled = enabled
        self.state = "unpressed"
        self.function = function
        
        self.image = pg.Surface((self.width, self.height))
        self.image.set_alpha(UI_TRANSPARENCY)
        self.image.fill(T_PURPLE)
        self.image.set_colorkey(T_PURPLE)
        self.mask = None
        self.rect = self.image.get_rect()
        
        self.rect.topleft = (self.x, self.y)
        
    def update(self):
        
        self.attr_dict = dict()
        
        for k, v in self.var_dict.items():
            attr_v = getattr(v[0], v[1])
            setattr(self, k, attr_v)
            self.attr_dict.update({k:attr_v}) 
        
        self.text_out = self.text_in.format(**self.attr_dict)
        button_text = self.game.font.render(self.text_out, True, "white")
        if self.enabled:
            if self.state == "pressed":
                pg.draw.rect(self.image, "darkslategray4", ((0,0), (self.width, self.height)), 0, 5)
                pg.draw.rect(self.image, "darkslategray1", ((0,0), (self.width, self.height)), 2, 5)
            else:
                pg.draw.rect(self.image, "darkslategray3", ((0,0), (self.width, self.height)), 0, 5)
                pg.draw.rect(self.image, "darkslategray1", ((0,0), (self.width, self.height)), 2, 5)
        else:
            self.kill()
        pg.draw.rect(self.image, "darkslategray1", ((0,0), (self.width, self.height)), 2, 5)
        self.image.blit(button_text, (10, (self.height - FONTSIZE) * 0.75))
        
        self.mask = pg.mask.from_surface(self.image)
        
        self.game.screen.blit(self.image, (self.x, self.y))
        
    # checks if click is touching tile and click cooldown ------------------- #
    def msbtn_down(self, pos, button):

        pos_in_mask = pos[0] - self.rect.x, pos[1] - self.rect.y
        touching = self.rect.collidepoint(pos) and self.mask.get_at(pos_in_mask)

        if touching:

            return True
        return False


    def handle_events(self, event):
        # handle events related to mouse clicks on tile --------------------- #
        if self.state == "unpressed":
            if event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
                
        if self.state == "pressed":
            if event.type == pg.MOUSEBUTTONUP:
                self.state = "unpressed"
                eval(self.function)
                
        if self.state == "pressed":
            if event.type == self.game.E_IDLE:
                pos_in_mask = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
                touching = self.rect.collidepoint(event.pos) and self.mask.get_at(pos_in_mask)
                if not touching:
                    self.state = "unpressed"


class TypewriterCrawl(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, text_in):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.text_in = text_in
        self.text_splitted = text_in.split("#")
        self.text_rows = len(self.text_splitted)
        self.colors = ["white", "darkslategray1"]

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self._layer = UI_INTERFACE_LAYER
        self.game.text_crawl_grp.add(self)
        
        self.abc_lst = list(string_module.ascii_lowercase)
        
        self.row_dct =dict()
        for i in range(self.text_rows):
            current_color = self.colors[(i + 1)%2]
            self.row_dct.update({self.abc_lst[i]:
                                 {"row_y" : FONTSIZE * i,
                                 "letters_printed" : 0,
                                 "letters_max" : len(self.text_splitted[i]),
                                 "row_text" : self.text_splitted[i],
                                 "row_color" : current_color}
                                 })
        
        self.speed = 1
        self.cooldown = 0
        self.finished = False
        
        self.double_width = ["w", "W"]
        
        self.image = pg.Surface((self.width, FONTSIZE * self.text_rows))
        self.image.fill("black")
        self.image.set_colorkey("black")
        self.image.set_alpha(UI_TRANSPARENCY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def update(self):
        
        # logic for progressive printing of text ---------------------------- #
        if self.cooldown <= 0 and not self.finished:
            for i in range(self.text_rows):
                
                row_name = self.abc_lst[i]
                letters_printed = self.row_dct[row_name]["letters_printed"]
                letters_max = self.row_dct[row_name]["letters_max"]
                
                if letters_printed < letters_max:
                    
                    self.row_dct[row_name]["letters_printed"] += 1
                    self.cooldown += 10
                    break
                
                elif i == self.text_rows - 1:
                    self.finished = True
            
        else:
            self.cooldown -= self.speed
        
        # logic for blitting text to screen --------------------------------- #
        for i in range(self.text_rows):
            
            row_name = self.abc_lst[i]
            row_color = self.row_dct[row_name]["row_color"]
            last_letter = self.row_dct[row_name]["letters_printed"]
            row_text = self.row_dct[row_name]["row_text"][0:last_letter]
            rendered_txt = self.game.font.render(row_text, True, row_color)
            self.image.blit(rendered_txt, (0, self.row_dct[row_name]["row_y"]))
     


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
        self.fog_of_war = True
        
        
    def update(self):
        
        # attaching unit to tile if occupied -------------------------------- #
        self.unit = gl.tile_has_unit(self, [self.game.unit_blufor_grp, self.game.unit_redfor_grp])
           
        # tints tile depending on animation_state --------------------------- #
        if self.animation_state != None:
            if self.animation_state == "activated_unit_on_tile":
                self.image = an.tint_image(self.original_image, "azure2")
            elif self.animation_state == "enemy_unit_in_range":
                self.image = an.tint_image(self.original_image, "tomato")
            elif self.animation_state == "in_movement_range":
                self.image = an.tint_image(self.original_image, "yellow")
        else:
            self.image = self.original_image
            
        # tints tile, if it is not within visible range by a unit ----------- #
        self.fog_of_war = gl.check_fog_of_war(self, self.game.unit_blufor_grp, self.game.tile_grp)
        
        if self.fog_of_war is True:
            self.image = an.tint_image(self.image, "grey")
            
                    
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
            
            # wether there is a blufor unit on tile and if its activated ---- #
            for unit in self.game.unit_blufor_grp:
                if unit.q == self.q and unit.r == self.r and unit.s == self.s:
                    blufor_on_tile = True
                    unit_on_tile = unit
                if unit.activated == True:
                    blufor_activated = unit
            
            # wether there is a redfor unit on tile ------------------------- #
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
                    if blufor_activated is not None:
                        if gl.in_weapon_range(blufor_activated, self.unit):
                            gl.attack_unit(blufor_activated, self.unit)
                
                # no unit on tile ------------------------------------------- #
                if unit_on_tile is None:
                    if blufor_activated is not None:
                        in_range = gl.in_mov_range(self, blufor_activated, self.game.tile_grp, "block_move")
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
                        
                        if tile.fog_of_war == True:
                            if self.faction == "redfor":
                                self.image.set_alpha(0)
                        else:
                            self.image.set_alpha(255)
                            
        if self.health <= 0:
            self.kill()
        
        self.rect.center = (self.x, self.y)
            
