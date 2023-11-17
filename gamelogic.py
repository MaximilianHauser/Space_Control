"""
Created on Thu Oct 20 16:49:27 2022

Contains all gamelogic, specified as functions that handle interactions that 
are dictated by game specific mechanics and are not covered by dedicated classes
or are not included in those classes. 

Dependencies:
-------------
hexlogic
    Handles the relationship between cartesian coordinates and cube coordinates.
    
w_attr
    Contains weapons statistics, like dmg, range, etc.
    
Functions:
----------


@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import re

# custom functions ---------------------------------------------------------- #
import hexlogic as hl

# game mechanic properties -------------------------------------------------- #
from attribute_dicts.w_attr import w_dict

    
# function determines, wether or not a unit is on the tile ------------------ #
# and if there is, assigns the unit as attribute to the tile ---------------- #
def tile_has_unit(tile:object, unit_sprite_groups_lst:list) -> object:
        
    on_tile = None
    for group in unit_sprite_groups_lst:
        for unit in group:
            if unit.q == tile.q:
                if unit.r == tile.r:
                    if unit.s == tile.s:
                        on_tile = unit
                            
    return on_tile
    
   
# function determines, if there currently is an activated blufor_unit ------- #
# and if yes, returns it ---------------------------------------------------- #
def is_activated_unit(unit_blufor_grp) -> object:
        
    activated_unit = None
    for unit in unit_blufor_grp:
        if unit.activated:
            activated_unit = unit
            
    return activated_unit
    
    
    
# function determines, wether or not tile is within movement range ---------- #
# of an activated blufor unit ----------------------------------------------- #
def in_mov_range(tile:object, unit:object, tile_grp, movement_var:str) -> bool:
        
    # determine variables for dist_lim_flood_fill --------------------------- #
    moves = unit.action_points
    obj_lst = tile_grp
        
    # returns list of coords within movement range -------------------------- #
    visited = hl.dist_lim_flood_fill(unit, moves, obj_lst, movement_var=movement_var)
    visited.remove((unit.q, unit.r, unit.s))
        
    # check if tile was visited in floodfil --------------------------------- #
    return hl.get_qrs(tile) in visited
        
    
# determine if unit_b is in weapon range of unit_a -------------------------- #
def in_weapon_range(unit_a:object, unit_b:object, weapon:str) -> bool:
    ab_dist = hl.distance(unit_a, unit_b)
    return ab_dist <= w_dict[weapon]["max_range"]
    
    
# range of the weapon with the longest range which is available ------------- #
def get_max_weapon_range(unit:object) -> int:
    max_range = 0
    for weapon in unit.ammunition:
        has_ammo = unit.ammunition[weapon] > 0
        ammo_range = w_dict[weapon]["max_range"]
        if has_ammo and ammo_range > max_range:
            max_range = ammo_range
                
    return max_range
    

# function determines if a tile is covered by fog of war -------------------- #
def check_fog_of_war(tile:object, blufor_grp, tile_grp) -> bool:
    fog_of_war = True
        
    for unit in blufor_grp:
        line_coords = hl.line_draw(unit, tile)
        coords_visible = list()
        for coords in line_coords:
            for tile in tile_grp:
                if tile.q == coords[0]:
                    if tile.r == coords[1]:
                        if tile.s == coords[2]:
                            coords_visible.append(tile.block_sight)
        if all(c is False for c in coords_visible):
            fog_of_war = False
                
    return fog_of_war

# function handles mechanics related to turn advancement -------------------- #
def skip_turn(manager:object) -> None:
    for unit in manager.unit_blufor_group:
        if unit.activated == True:
            unit.action_points = 0
    

# get total numerical attribute in sprite_group ----------------------------- #
def get_group_attr_total_num(attr:str, sprite_group) -> int:
    attr_total = 0
    for unit in sprite_group:
        attr_total += getattr(unit, attr)
    return attr_total
    
    
# get total damage potential of all weapons on ships ------------------------ #
def get_group_total_munition_dmg(sprite_group) -> int:
    potential_dmg_total = 0
    for unit in sprite_group:
        ammunition_types = unit.ammunition.keys()
        for a_type in ammunition_types:
            potential_dmg = unit.ammunition[a_type] * w_dict[a_type]["dmg"]
            potential_dmg_total += potential_dmg
        
    return potential_dmg_total
    
    
# get ciws cover dict for tile ---------------------------------------------- #
def get_ciws_cover(tile:object) -> dict:
    """
    Updates a tiles ciws_dict, containing all units that cover that field with 
    their ciws.
    """
    ciws_units = set()
    ciws_dict = dict()
    
    # get units of attacked faction ----------------------------------------- #
    ciws_units = collect_from_attrs_pattern(tile.manager, "^unit_.*_group$")
                
    # get units covering tile ----------------------------------------------- #
    for unit in ciws_units:
        if unit.ciws_range >= hl.distance(unit, tile) and unit.ciws_charge > 0:
            line_of_sight = hl.line_draw(unit, tile)
            # if all tiles on the los aren't blocked ------------------------ #
            if all(t for t in tile.manager.tile_group if t.qrs in line_of_sight[1:]):
                ciws_dict.update({unit.id:{"dmg":unit.ciws_dmg, "range":unit.ciws_range, "faction":unit.faction, "qrs":unit.qrs}})
        
    return ciws_dict            
    
    
# get the possible actions to be performed, after right clicking tile ------- #
def get_kwargs_ddm(tile, blufor_activated, blufor_grp, tile_grp):
    kwargs_dct = dict()
        
    # if tile is neighbor, has no unit => movable --------------------------- #
    nbors_lst = hl.neighbors((tile.q, tile.r, tile.s))
    if (blufor_activated.q, blufor_activated.r, blufor_activated.s) in nbors_lst:
        if in_mov_range(tile, blufor_activated, tile_grp, "block_move"):
            if tile.unit == None:
                kwargs_dct.update({"move":"gl.move_unit(next(t for t in self.game.tile_group if t.ddm_open == True), next(u for u in self.game.unit_blufor_group if u.activated == True))"})        
        
    # if tile has enemy or fog => attackable -------------------------------- #
    fog_bool = check_fog_of_war(tile, blufor_grp, tile_grp)
    available_munition = dict()
        
    for k in blufor_activated.ammunition.keys():
        if blufor_activated.ammunition[k] > 0:
            available_munition.update({k:blufor_activated.ammunition[k]})
                
    for k in available_munition.keys():
        if fog_bool:
            if in_weapon_range(blufor_activated, tile, weapon=k):
                kwargs_dct.update({k:"Munition(self.game, '"+str(k)+"', next(u for u in self.game.unit_blufor_group if u.activated == True), next(t for t in self.game.tile_group if t.ddm_open == True))"})
                    
        elif hasattr(tile.unit, "faction"):
            if in_weapon_range(blufor_activated, tile.unit, weapon=k):
                kwargs_dct.update({k:"Munition(self.game, '"+str(k)+"', next(u for u in self.game.unit_blufor_group if u.activated == True), next(t for t in self.game.tile_group if t.ddm_open == True))"})
        
    return kwargs_dct


# get unit > tile > coords as target ---------------------------------------- #
def get_coords_occupancy(manager, coords_in):
    q_str, r_str, s_str = (int(coords_in[0]), int(coords_in[1]), int(coords_in[2]))
    coords = hl.tuple_or_object((q_str, r_str, s_str), 3)
    
    unit_blufor = hl.getobj(manager.unit_blufor_group, "qrs", coords, return_set=True)
    unit_redfor = hl.getobj(manager.unit_redfor_group, "qrs", coords, return_set=True)
    tile = hl.getobj(manager.tile_group, "qrs", coords, return_set=True)
    
    if unit_blufor:
        return unit_blufor
    elif unit_redfor:
        return unit_redfor
    elif tile:
        return tile
    else:
        return None
    
    
# add all elements stored in values(containers) of properties to a set ------ #
def collect_from_attrs_pattern(top_obj:object, pattern:str) -> set:
    matched = set()
    for property, value in vars(top_obj).items():
        if re.fullmatch(pattern, property):
            for element in value:
                matched.add(element)
    return matched
    
    
