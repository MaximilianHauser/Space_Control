# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:14:54 2023

Provides an object, that together with the ciws attributes of tiles simulates 
a unit attacking another unit. It will also cover all the animatons in a later 
stage.

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg
from hexlogic import HexLogic as hl
from attribute_dicts.w_attr import w_dict
from settings import U_ANIMATION_LAYER, WIN_WIDTH, WIN_HEIGHT

# Unit class ---------------------------------------------------------------- #
class Munition(pg.sprite.Sprite):
    
    def __init__(self, game:object, weapon_type:str, launcher:object, target:object) -> object:
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.launcher = launcher
        self.target = target
        
        self.q = launcher.q
        self.r = launcher.r
        self.s = launcher.s
        
        self.qrs = launcher.qrs
        
        self._layer = U_ANIMATION_LAYER
        self.game.all_sprites.add(self)
        self.game.munition_grp.add(self)
        
        x, y = hl.hex_to_pixel(self.qrs)
        self.x = x + WIN_WIDTH / 2
        self.y = y + WIN_HEIGHT / 2
        
        for k, v in w_dict[weapon_type].items():
            setattr(self, k, v)
            
        self.tiles_traversed = hl.line_draw(launcher, target)
        self.tile_num = 0
        self.cooldown = 0
        self.speed = 1
        self.stage = "launch"
        self.life_cycle = ["launch", "midcourse", "evasion_calc", "terminal"]
        
        # image and animation variables ------------------------------------- #
        self.image = pg.Surface((5, 5))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.animation_dict = dict()
        
    
    def update(self) -> None:
        
        if self.cooldown <= 0:
            
            if self.stage == "launch":
                self.stage = "midcourse"
            
            elif self.stage == "midcourse":
                
                unit_grp = self.game.blufor_grp if self.launcher.faction == "redfor" else self.game.redfor_grp
                
                ciws_cover = [tile for tile in self.game.tile_grp if tile.qrs == self.qrs][0].ciws_dict
                ciws_cover_keys = ciws_cover.keys()
                for k in ciws_cover_keys:
                    if self.alive() and self.launcher.faction != ciws_cover[k]["faction"]:
                        self.armor -= ciws_cover[k]["dmg"]
                        self.dmg -= ciws_cover[k]["dmg"]
                        firing_unit = [unit for unit in unit_grp if unit.id == k][0]
                        firing_unit.ciws_charge -= 1
                        if self.armor <= 0:
                            self.kill()
                
                
                if self.tile_num >= len(self.tiles_traversed):
                    self.stage = "evasion_calc"
            
            elif self.stage == "evasion_calc":
                munition_evaded = True if (self.target.evasion * len(self.tiles_traversed) > 1) and self.type != "guided" else False
                if munition_evaded:
                    self.kill()
                else:
                    self.stage = "terminal"
            
            elif self.stage == "terminal":
                try:
                    penetrating_dmg = (self.dmg - self.target.armor) if (self.dmg - self.target.armor) > 0 else 0
                    applied_dmg = penetrating_dmg * self.dmg_multiplier
                    self.target.health -= applied_dmg
                    self.target.armor -= 0.5 * self.dmg
                    self.kill()
                except:
                    self.kill()
            
            # update tile position of munition ------------------------------ #
            new_qrs = self.tiles_traversed[self.tile_num].qrs
            
            self.qrs = new_qrs
            self.q = new_qrs[0]
            self.r = new_qrs[1]
            self.s = new_qrs[2]
            
            if self.tile_num < len(self.tiles_traversed):
                self.tile_num += 1

            
        else:
            self.cooldown += 10






