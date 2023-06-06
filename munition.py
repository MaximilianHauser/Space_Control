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
from settings import U_ANIMATION_LAYER, WIN_WIDTH, WIN_HEIGHT


# Munition class ------------------------------------------------------------ #
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
        self.life_cycle = ["launch", "midcourse", "terminal"]
        
        self.logic_dict = dict()
        
        # adding entries to self.logic_dict --------------------------------- #
        for i in range(len(self.tiles_traversed)):
            current_tile = next(t for t in self.game.tile_grp if t.qrs == self.tiles_traversed[i])
            
            perc_traversed = (1 / len(self.tiles_traversed)) * i
            current_xy = hl.cartesian_linint(launcher.rect.center, target.rect.center, perc_traversed)
            
            if i == 0:
                current_phase = "launch"
            elif i < (len(self.tiles_traversed) - 1):
                current_phase = "midcourse"
            else:
                current_phase = "terminal"
                
            self.logic_dict.update({self.tiles_traversed[i]:{"phase":current_phase, "state":None, "xy_pos":current_xy, "ciws_cover":gl.get_ciws_cover(current_tile)}})
            
        for i in range(len(self.tiles_traversed)):
            coords = list(self.logic_dict.keys())[i]
            print(coords)
                
            if self.logic_dict[coords]["phase"] == "launch":
                print("phase: launch")
                self.launcher.action_points -= 1
                self.launcher.ammunition[weapon_type] -= 1
                self.logic_dict[self.tiles_traversed[i]]["state"] = "firing"
                    
            elif self.logic_dict[coords]["phase"] == "midcourse":
                print("phase: midcourse")
                unit_grp = self.game.unit_blufor_grp if self.launcher.faction == "redfor" else self.game.unit_redfor_grp
                
                current_tile = next(t for t in self.game.tile_grp if t.qrs == coords)
                units_intercepting_ids = [unit.id for unit in unit_grp]
                ciws_cover_keys = [unit_id for unit_id in current_tile.ciws_dict.keys() if unit_id in units_intercepting_ids]
                
                counter = 0
                
                print("pre k in ciws_cover_keys:")
                print("unit_grp: " + str(unit_grp))
                print("units_intercepting_ids: " + str(units_intercepting_ids))
                print("ciws_cover_keys: " + str(ciws_cover_keys))
                
                if ciws_cover_keys:
                    for k in ciws_cover_keys:
                        
                        alive = self.armor > 0
                        counter += 1
                        all_engaged = counter > len(ciws_cover_keys)
                        print("all_engaged: " + str(all_engaged))
                        
                        if alive and not all_engaged:
                            firing_unit = [unit for unit in unit_grp if unit.id == k]
                            print(firing_unit)
                            if firing_unit:
                                self.armor -= firing_unit[0].ciws_dmg
                                self.dmg -= firing_unit[0].ciws_dmg * 0.5
                                firing_unit[0].ciws_charge -= 1
                                self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_hits"
                                if self.armor <= 0:
                                    self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                                    
                            else:
                                if self.logic_dict[self.tiles_traversed[i]]["state"] == None:
                                   self.logic_dict[self.tiles_traversed[i]]["state"] = "traversing"
                                
                        elif alive:
                            counter = 0
                            if self.logic_dict[self.tiles_traversed[i]]["state"] == None:
                               self.logic_dict[self.tiles_traversed[i]]["state"] = "traversing"
                            
                        elif not alive:
                            if not self.logic_dict[self.tiles_traversed[i-1]]["state"] == "ciws_destroys":
                                self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                                
                else:
                    self.logic_dict[self.tiles_traversed[i]]["state"] = "traversing"
                        
                
                    
            elif self.logic_dict[coords]["phase"] == "terminal":
                print("phase: terminal")
                if self.armor <= 0:
                        break
                munition_evaded = True if (self.target.evasion * len(self.tiles_traversed) > 1) and self.type != "guided" else False
                print("munition_evaded: " + str(munition_evaded))
                if munition_evaded:
                    self.logic_dict[self.tiles_traversed[i]]["state"] = "target_evades"
                else:
                    # resolving ciws_cover of final tile -------------------- #
                    unit_grp = self.game.unit_blufor_grp if self.launcher.faction == "redfor" else self.game.unit_redfor_grp
                    
                    current_tile = next(t for t in self.game.tile_grp if t.qrs == coords)
                    units_intercepting_ids = [unit.id for unit in unit_grp]
                    ciws_cover_keys = [unit_id for unit_id in current_tile.ciws_dict.keys() if unit_id in units_intercepting_ids]
                    
                    counter = 0
                    
                    print("pre k in ciws_cover_keys:")
                    print("unit_grp: " + str(unit_grp))
                    print("units_intercepting_ids: " + str(units_intercepting_ids))
                    print("ciws_cover_keys: " + str(ciws_cover_keys))
                    
                    if ciws_cover_keys:
                        for k in ciws_cover_keys:
                            
                            alive = self.armor > 0
                            counter += 1
                            all_engaged = counter > len(ciws_cover_keys)
                            print("all_engaged: " + str(all_engaged))
                            
                            if alive and not all_engaged:
                                firing_unit = [unit for unit in unit_grp if unit.id == k]
                                print(firing_unit)
                                if firing_unit:
                                    self.armor -= firing_unit[0].ciws_dmg
                                    self.dmg -= firing_unit[0].ciws_dmg * 0.5
                                    firing_unit[0].ciws_charge -= 1
                            elif not alive:
                                self.logic_dict[self.tiles_traversed[i]]["state"] = "ciws_destroys"
                            

                    # damage application if not intercepted ----------------- #
                    if self.armor > 0:
                        penetrating_dmg = (self.dmg - self.target.armor) if (self.dmg - self.target.armor) > 0 else 0
                        applied_dmg = penetrating_dmg * self.dmg_multiplier
                        self.target.health -= applied_dmg
                        self.target.armor = (self.target.armor - 0.5 * self.dmg) if (self.target.armor - 0.5 * self.dmg) >= 0 else 0
                        self.logic_dict[self.tiles_traversed[i]]["state"] = "target_hit"
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
        
        
    def update(self) -> None:
        pass

        





