"""
Created on Fri May 12 15:14:54 2023

Provides an object, that together with the ciws attributes of tiles simulates 
a unit attacking another unit. It will also cover all the animatons in a later 
stage.

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg
import hexlogic as hl
import gamelogic as gl
from attribute_dicts.w_attr import w_dict
from settings import U_ANIMATION_LAYER


# Munition class ------------------------------------------------------------ #
class Munition(pg.sprite.Sprite):
    
    def __init__(self, manager:object, weapon_type:str, launcher:object, target:object) -> object:
        pg.sprite.Sprite.__init__(self)
        self.manager = manager
        
        self.launcher = launcher
        self.target = target
        
        self.q = launcher.q
        self.r = launcher.r
        self.s = launcher.s
        
        self.qrs = launcher.qrs
        
        self._layer = U_ANIMATION_LAYER
        self.manager.all_sprites.add(self)
        self.manager.munition_group.add(self)
        
        x, y = hl.hex_to_pixel(self.qrs)
        self.x = launcher.x
        self.y = launcher.y
        
        for k, v in w_dict[weapon_type].items():
            setattr(self, k, v)
            
        self.tiles_traversed = hl.line_draw(launcher, target)
        self.current_tile = None
        self.tile_num = 1
        self.speed = 30 if self.type == "guided" else 80
        self.stage = "launch"
        self.life_cycle = ["launch", "midcourse", "terminal"]
        
        self.logic_dict = dict()
        
        # adding entries to self.logic_dict --------------------------------- #
        for i in range(len(self.tiles_traversed)):
            current_tile = next(t for t in self.manager.tile_group if t.qrs == self.tiles_traversed[i])
            
            perc_traversed = (1 / len(self.tiles_traversed)) * i
            current_xy = hl.rect_linint(launcher.rect.center, target.rect.center, perc_traversed)
            
            if i == 0:
                current_phase = "launch"
            elif i < (len(self.tiles_traversed) - 1):
                current_phase = "midcourse"
            else:
                current_phase = "terminal"
                
            self.logic_dict.update({self.tiles_traversed[i]:{"phase":current_phase, "state":None, "xy_pos":current_xy, "ciws_cover":gl.get_ciws_cover(current_tile)}})
        
        # calculating outcome for each tile traversed ----------------------- #
        for i in range(len(self.tiles_traversed)):
            coords = list(self.logic_dict.keys())[i]
            print(coords)
            
            # phase: launch ------------------------------------------------- #
            if self.logic_dict[coords]["phase"] == "launch":
                print("phase: launch")
                self.launcher.action_points -= 1
                self.launcher.ammunition[weapon_type] -= 1
                self.logic_dict[self.tiles_traversed[i]]["state"] = "launching"
            
            # phase: midcourse ---------------------------------------------- #
            elif self.logic_dict[coords]["phase"] == "midcourse":
                print("phase: midcourse")
                # sprite group containing the units of target faction ------- #
                unit_group = self.manager.unit_blufor_group if self.launcher.faction == "redfor" else self.manager.unit_redfor_group
                # current tile and unit ids of units ciws covering the tile - #
                current_tile = next(t for t in self.manager.tile_group if t.qrs == coords)
                units_intercepting_ids = [unit.id for unit in unit_group]
                ciws_cover_keys = [unit_id for unit_id in current_tile.ciws_dict.keys() if unit_id in units_intercepting_ids]
                
                print("pre k in ciws_cover_keys:")
                print("unit_grp: " + str(unit_group))
                print("units_intercepting_ids: " + str(units_intercepting_ids))
                print("ciws_cover_keys: " + str(ciws_cover_keys))
                
                # for unit covering tile, if munition alive ----------------- #
                if ciws_cover_keys:
                    for k in ciws_cover_keys:
                        
                        alive = self.armor > 0
                        
                        if alive:
                            # apply damage of ciws and deduct one ciws charge from firing unit #
                            firing_unit = [unit for unit in unit_group if unit.id == k]
                            print(firing_unit[0].id)
                            if firing_unit:
                                self.armor = self.armor - firing_unit[0].ciws_dmg if (self.armor - firing_unit[0].ciws_dmg) >= 0 else 0
                                self.dmg = self.dmg - firing_unit[0].ciws_dmg if (self.dmg - firing_unit[0].ciws_dmg) >= 0 else 0
                                firing_unit[0].ciws_charge -= 1
                                self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_hits"
                                if self.armor <= 0:
                                    self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                                    
                            else:
                                if self.logic_dict[self.tiles_traversed[i]]["state"] == None:
                                   self.logic_dict[self.tiles_traversed[i]]["state"] = "traversing"
                                   print("no enemy ciws cover on tile")
                                   
                            print("projectile stats after_ciws")
                            print("dmg: " + str(self.dmg))
                            print("armor: " + str(self.armor))
                            
                        elif not alive:
                            if not self.logic_dict[self.tiles_traversed[i-1]]["state"] == "ciws_destroys":
                                self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                # if no enemy unit ciws covering tile, traverse tile -------- #                
                else:
                    self.logic_dict[self.tiles_traversed[i]]["state"] = "traversing"
                        
                
            # phase: terminal ----------------------------------------------- #        
            elif self.logic_dict[coords]["phase"] == "terminal":
                print("phase: terminal")
                # munition still alive? ------------------------------------- #
                if self.armor <= 0:
                    print("munition already d.e.d.")
                    break
                # target is a tile not a unit ------------------------------- #
                elif not hasattr(self.target, "evasion"):
                    print("target does not have attr evasion")
                    
                    if hasattr(self.target, "unit"):
                        print("target has attr unit")
                        munition_evaded = True if (self.target.unit.evasion * len(self.tiles_traversed) > 1) and self.type != "guided" else False
                        
                        if munition_evaded:
                            print("munition_evaded: " + str(munition_evaded))
                            self.logic_dict[self.tiles_traversed[i]]["state"] = "target_evades"
                            
                        else:
                            # resolving ciws_cover of final tile -------------------- #
                            unit_group = self.manager.unit_blufor_group if self.launcher.faction == "redfor" else self.manager.unit_redfor_group
                            
                            current_tile = next(t for t in self.manager.tile_group if t.qrs == coords)
                            units_intercepting_ids = [unit.id for unit in unit_group]
                            ciws_cover_keys = [unit_id for unit_id in current_tile.ciws_dict.keys() if unit_id in units_intercepting_ids]
                            
                            print("pre k in ciws_cover_keys:")
                            print("unit_grp: " + str(unit_group))
                            print("units_intercepting_ids: " + str(units_intercepting_ids))
                            print("ciws_cover_keys: " + str(ciws_cover_keys))
                            
                            if ciws_cover_keys:
                                for k in ciws_cover_keys:
                                    
                                    alive = self.armor > 0
                                    
                                    if alive:
                                        firing_unit = [unit for unit in unit_group if unit.id == k]
                                        print(firing_unit[0].id)
                                        if firing_unit:
                                            self.armor = self.armor - firing_unit[0].ciws_dmg if (self.armor - firing_unit[0].ciws_dmg) >= 0 else 0
                                            self.dmg = self.dmg - firing_unit[0].ciws_dmg if (self.dmg - firing_unit[0].ciws_dmg) >= 0 else 0
                                            firing_unit[0].ciws_charge -= 1
                                            if self.armor <= 0:
                                                self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                                    elif not alive:
                                        if not self.logic_dict[self.tiles_traversed[i-1]]["state"] == "ciws_destroys":
                                            self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                                    

                            # damage application if not intercepted ----------------- #
                            print("projectile stats hit_calc")
                            print("dmg: " + str(self.dmg))
                            print("armor: " + str(self.armor))
                            if self.armor > 0:
                                penetrating_dmg = (self.dmg - self.target.unit.armor) if (self.dmg - self.target.unit.armor) > 0 else 0
                                applied_dmg = penetrating_dmg * self.dmg_multiplier
                                self.target.unit.health -= applied_dmg
                                self.target.unit.armor = (self.target.unit.armor - 0.5 * self.dmg) if (self.target.unit.armor - 0.5 * self.dmg) >= 0 else 0
                                self.logic_dict[self.tiles_traversed[i]]["state"] = "target_hit"
                                print("target stats after hit")
                                print("health: " + str(self.target.unit.health))
                                print("armor: " + str(self.target.unit.armor))
                                
                    else:
                        print("tile is empty")
                        self.logic_dict[self.tiles_traversed[i]]["state"] = "traversing"
                        
                else:
                    print("target is a unit")
                    munition_evaded = True if (self.target.evasion * len(self.tiles_traversed) > 1) and self.type != "guided" else False
                    if munition_evaded:
                        print("munition_evaded: " + str(munition_evaded))
                        self.logic_dict[self.tiles_traversed[i]]["state"] = "target_evades"
                        break
                    # resolving ciws_cover of final tile -------------------- #
                    unit_group = self.manager.unit_blufor_group if self.launcher.faction == "redfor" else self.manager.unit_redfor_group
                    
                    current_tile = next(t for t in self.manager.tile_group if t.qrs == coords)
                    units_intercepting_ids = [unit.id for unit in unit_group]
                    ciws_cover_keys = [unit_id for unit_id in current_tile.ciws_dict.keys() if unit_id in units_intercepting_ids]
                    
                    print("pre k in ciws_cover_keys:")
                    print("unit_grp: " + str(unit_group))
                    print("units_intercepting_ids: " + str(units_intercepting_ids))
                    print("ciws_cover_keys: " + str(ciws_cover_keys))
                    
                    if ciws_cover_keys:
                        for k in ciws_cover_keys:
                            
                            alive = self.armor > 0
                            
                            if alive:
                                firing_unit = [unit for unit in unit_group if unit.id == k]
                                print(firing_unit[0].id)
                                if firing_unit:
                                    self.armor = self.armor - firing_unit[0].ciws_dmg if (self.armor - firing_unit[0].ciws_dmg) >= 0 else 0
                                    self.dmg = self.dmg - firing_unit[0].ciws_dmg if (self.dmg - firing_unit[0].ciws_dmg) >= 0 else 0
                                    firing_unit[0].ciws_charge -= 1
                                    if self.armor <= 0:
                                        self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                            elif not alive:
                                if not self.logic_dict[self.tiles_traversed[i-1]]["state"] == "ciws_destroys":
                                    self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                            

                    # damage application if not intercepted ----------------- #
                    print("projectile stats hit_calc")
                    print("dmg: " + str(self.dmg))
                    print("armor: " + str(self.armor))
                    if self.armor > 0:
                        penetrating_dmg = (self.dmg - self.target.armor) if (self.dmg - self.target.armor) > 0 else 0
                        applied_dmg = penetrating_dmg * self.dmg_multiplier
                        self.target.health -= applied_dmg
                        self.target.armor = (self.target.armor - 0.5 * self.dmg) if (self.target.armor - 0.5 * self.dmg) >= 0 else 0
                        self.logic_dict[self.tiles_traversed[i]]["state"] = "target_hit"
                        print("target stats after hit")
                        print("health: " + str(self.target.health))
                        print("armor: " + str(self.target.armor))
        
        print("")
        for key in self.logic_dict.keys():
            print(self.logic_dict[key]["state"])
        
        # image and animation variables ------------------------------------- #
        self.image = pg.Surface((5, 5))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.perc_traversed = 0
        self.state = "launching"
        
        # direction of munition for animation borders ----------------------- #
        if self.launcher.x <= self.target.x:
            self.dir_x = "right"
        else:
            self.dir_x = "left"
            
        if self.launcher.y <= self.target.y:
            self.dir_y = "down"
        else:
            self.dir_y = "up"
            
        self.direction = (self.dir_x, self.dir_y)
        

    def update(self, delta) -> None:
        
        if self.perc_traversed <= 1:
            self.perc_traversed += 0.005 * self.speed * delta
        else:
            self.kill()
        
        munition_pos = hl.rect_linint(self.launcher.rect.center, self.target.rect.center, self.perc_traversed)
        
        self.x = munition_pos[0]
        self.y = munition_pos[1]
        
        self.rect.center = (self.x, self.y)
        
        # animation depending on munition_state ----------------------------- #
        if self.tile_num < len(self.tiles_traversed):
            border = self.logic_dict[self.tiles_traversed[self.tile_num]]["xy_pos"]
            self.x_border = border[0]
            self.y_border = border[1]
        
            if self.direction == ("right", "down"):
                if self.x_border < self.x or self.y_border < self.y:
                    self.state = self.logic_dict[self.tiles_traversed[self.tile_num]]["state"]
                    self.tile_num += 1
            
            elif self.direction == ("left", "down"):
                if self.x_border > self.x or self.y_border < self.y:
                    self.state = self.logic_dict[self.tiles_traversed[self.tile_num]]["state"]
                    self.tile_num += 1
            
            elif self.direction == ("right", "up"):
                if self.x_border < self.x or self.y_border > self.y:
                    self.state = self.logic_dict[self.tiles_traversed[self.tile_num]]["state"]
                    self.tile_num += 1
            
            elif self.direction == ("left", "up"):
                if self.x_border > self.x or self.y_border > self.y:
                    self.state = self.logic_dict[self.tiles_traversed[self.tile_num]]["state"]
                    self.tile_num += 1
        
            
        # set animation based on state -------------------------------------- #
        if self.state == "launching":
            self.image.fill("blue")
            
        elif self.state == "traversing":
            self.image.fill("green")
            
        elif self.state == "ciws_hits":
            self.image.fill("yellow")
            
        elif self.state == "ciws_destroys":
            self.image.fill("orange")
            
        elif self.state == "target_hit":
            self.image.fill("red")
            
        elif self.state is None:
            self.kill()


