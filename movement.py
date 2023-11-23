# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:46:05 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg

# custom functions ---------------------------------------------------------- #
import hexlogic as hl
import animations_logic as al
from custom_distributions import custom_cauchy_distribution

# misc ---------------------------------------------------------------------- #
from settings import U_ANIMATION_LAYER


# Movement class ------------------------------------------------------------ #
class Movement(pg.sprite.Sprite):
    
    def __init__(self, manager, clicked_tile:object, unit:object) -> None:
        pg.sprite.Sprite.__init__(self)
        
        self.manager = manager
        
        self.clicked_tile = clicked_tile
        self.unit = unit
        
        self.q = unit.q
        self.r = unit.r
        self.s = unit.s
        
        self.qrs = unit.qrs
        
        self.start_xy = self.unit.rect.center
        self.target_xy = self.clicked_tile.rect.center
        
        distance_movement = hl.distance(unit, clicked_tile)
        hl.set_qrs(unit, clicked_tile.q, clicked_tile.r, clicked_tile.s)
        unit.action_points -= distance_movement
        
        self._layer = U_ANIMATION_LAYER
        self.manager.all_sprites.add(self)
        self.manager.movement_group.add(self)
        
        x, y = hl.hex_to_pixel(self.qrs)
        self.x = unit.x
        self.y = unit.y
        
        # movemnt animation specific variables ------------------------------ #
        self.perc_traversed = 0
        self.speed = 50
        
        # image and animation variables ------------------------------------- #
        self.image = pg.Surface((5, 5))
        self.image.fill("white")

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.perc_traversed = 0
        
        # direction of movement for animation borders ----------------------- #
        if self.unit.x <= self.clicked_tile.x:
            self.dir_x = "right"
        else:
            self.dir_x = "left"
            
        if self.unit.y <= self.clicked_tile.y:
            self.dir_y = "down"
        else:
            self.dir_y = "up"
            
        self.direction = (self.dir_x, self.dir_y)
        
        self.check_movement_validity()
    
    
    # set animation based on distance traveled ------------------------------ #    
    def set_animation(self):
        x = (-0.5 + self.perc_traversed) * 2
        r = 0
        a = 255
        g = custom_cauchy_distribution(x) * 100 + 150
        b = custom_cauchy_distribution(x) * 100 + 150
        color = (r, g, b, a)
        self.image.fill(color)
    
        
    def update(self, delta) -> None:
        if self.perc_traversed <= 1:
            self.perc_traversed += 0.005 * self.speed * delta
        else:
            self.kill()
        
        movement_pos = hl.rect_linint(self.start_xy, self.target_xy, self.perc_traversed)
        
        self.x = movement_pos[0]
        self.y = movement_pos[1]
        
        self.rect.center = (self.x, self.y)
            
        # set animation based perc_traveled --------------------------------- #
        self.set_animation()
    
    
    def check_movement_validity(self):
        nbors = hl.neighbors(self.unit.qrs)
        if self.clicked_tile.qrs not in nbors:
            raise hl.ConstraintViolation("movement needs to be to neighboring tile.")
        
        
        
        