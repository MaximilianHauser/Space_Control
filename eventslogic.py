# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 13:33:17 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import json
import pygame as pg

# custom functions ---------------------------------------------------------- #
import hexlogic as hl
import gamelogic as gl

# sprite objects ------------------------------------------------------------ #
from munition import Munition


# custom errors, defined to refer to incorrect condition format ------------- #
class ConditionFormatViolation(ValueError):
    """
    The format the conditions needs to be in was violated.
    """
    pass

# mock launcher object for Munition spawn occurence ------------------------- #
class MockLauncher(pg.sprite.Sprite):
    
    def __init__(self, manager, coords, weapon_type):
        pg.sprite.Sprite.__init__(self)
        
        self.manager = manager
        
        obj_on_coords = gl.get_coords_occupancy(self.manager, coords)
        
        if obj_on_coords:
            obj = obj_on_coords.pop()
            mock_coords = (obj.q, obj.r, obj.s)
        else:
            mock_coords = coords
        
        self.q = mock_coords[0]
        self.r = mock_coords[1]
        self.s = mock_coords[2]
        
        self.qrs = mock_coords

        self.x = [t for t in self.manager.tile_group if t.qrs == (self.q, self.r, self.s)][0].x
        self.y = [t for t in self.manager.tile_group if t.qrs == (self.q, self.r, self.s)][0].y
        
        self.action_points = 99
        self.ammunition = dict()
        self.ammunition[weapon_type] = 99
        
        self.faction = "redfor"
        
        self.image = pg.Surface((5, 5))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        

# eventslogic class --------------------------------------------------------- #
class EventsLogic:
    
    def __init__(self, manager):
        
        self.manager = manager
        self.unit_set = set()
        
        spritegroup_lst = [self.manager.unit_blufor_group, self.manager.unit_redfor_group]
        for group in spritegroup_lst:
            for unit in group:
                self.unit_set.add(unit)
        
        # set for events not yet triggered ---------------------------------- #
        self.ids_not_done_or_active = set()
        
        # set for currently active events ----------------------------------- #
        self.currently_active_events = set()
        
        # import based on selected mission ---------------------------------- #
        battle_events_dict_path = ".\missions\\" + str(self.manager.persistent["selected_mission"] + "\\battle_events.json")
        
        json_o = open(battle_events_dict_path)
        self.battle_events_dict = json.load(json_o)
        json_o.close()
        
        for key in self.battle_events_dict.keys():
            self.ids_not_done_or_active.add(key)
            
        # conditions tree for interpreting passed trigger ------------------- #
        self.conditions_tree = {
                                "unit_blufor":{
                                    "coordinate",
                                    "coordinates",
                                    "health_rel",
                                    "health_abs",
                                    },
                                
                                "unit_redfor":{
                                    "coordinate",
                                    "coordinates",
                                    "health_rel",
                                    "health_abs",
                                    },
                                
                                "blufor":{
                                    "health_rel",
                                    "health_abs",
                                    "num_rel",
                                    "num_abs"
                                    },
                                
                                "redfor":{
                                    "health_rel",
                                    "health_abs",
                                    "num_rel",
                                    "num_abs"
                                    },
                                
                                "countdown":{
                                    "ticks",
                                    "moves",
                                    "rounds"
                                    }
                                }
    

    def check_condition_validity(self, condition):
        split_condition = condition.split(":")
        if split_condition[1] not in self.conditions_tree[split_condition[0]]:
            raise ConditionFormatViolation("""Either trigger_type or trigger_subject is not in the correct format.""")
            
            
    def interpret_condition(self, event_id, stage):
        # get trigger condition --------------------------------------------- #
        trigger_raw = self.battle_events_dict[event_id][stage]
        split_by_condition = trigger_raw.split()
        
        num_building_blocks = len(split_by_condition)
        # test if format is valid ------------------------------------------- #
        if num_building_blocks % 2 == 0:
            raise ConditionFormatViolation("""The format of the TRIGGER needs to 
                                           be condition_1 AND condition_2 AND ...""")
        
        elif not all(map(lambda x:x in ("AND","OR"), split_by_condition[1::2])) and num_building_blocks != 1:
            raise ConditionFormatViolation("""The conditions need to be connected 
                                           with either AND or OR.""")
        else:
            conditions = split_by_condition[0::2]
            for condition in conditions:
                self.check_condition_validity(condition)
                
                condition_split = condition.split(":")
                if condition_split[0] in ("unit_blufor", "unit_redfor"):
                    triggered = self.unit_eoconst(event_id, condition)
                elif condition_split[0] == "countdown":
                    triggered = self.countdown_eoconst(event_id, condition)
                    
        return triggered
        
        
    # condition enforcement functions --------------------------------------- #
    def unit_eoconst(self, event_id, condition):
        """
        Checks if TRIGGER condition is met for each unit having the trigger assigned
        to the event_triggers attribute, returns Boolean.
        """
        # condition split into TYPE, SPECIFIC_CONDITION, SPECIFIC_VALUE ----- #
        condition_split = condition.split(":")
        faction = condition_split[0]
        specific = condition_split[1]
        value = condition_split[2]
        
        # specific is a set containing 1+ coordinates ----------------------- #
        if specific == "coordinates":
            # test for each unit with faction blufor if on coords ----------- #
            for unit in self.unit_set:
                if unit.faction == faction[-6:] and (unit.q,unit.r,unit.s) in eval(value) and unit.event_triggers == event_id:
                    return event_id

            # return False if no unit is on coords described in set --------- #
            return False
                    
        # specific is health rel or abs ------------------------------------- #
        elif specific[:7] == "health":
            if specific[-3:] == "rel":
                for unit in self.unit_set:
                    if unit.faction == faction[-6:] and (unit.health / unit.max_health) <= eval(value) and unit.event_triggers == event_id:
                        return event_id
                return False
            
            elif specific[-3:] == "abs":
                for unit in self.unit_set:
                    if unit.faction == faction[-6:] and unit.health <= eval(value) and unit.event_triggers == event_id:
                        return event_id
                return False
        
    
    def countdown_eoconst(self, event_id, condition):
        """
        Checks if TRIGGER condition is met, returns Boolean.
        """
        # condition split into COUNTDOWN, METRIC, VALUE --------------------- #
        condition_split = condition.split(":")
        countdown = condition_split[0]
        metric = condition_split[1]
        value = condition_split[2]
        
        if metric == "ticks":
            if self.manager.total_runtime >= float(value):
                return event_id
        
        elif metric == "moves":
            pass
        
        elif metric == "rounds":
            if self.manager.round_counter >= int(value):
                return event_id
            
            
    def interpret_occurence(self, event_id):
        occurence = self.battle_events_dict[event_id]["OCCURENCE"]
        print(occurence[:14])
        if occurence == "block_input":
            pass
        elif occurence[:14] == "spawn_munition":
            occurence_split = occurence.split("(")[1]
            stripped = occurence_split[:-1]
            variables = stripped.split(",")
            weapon_type = variables[0]
            launcher_coords = variables[1].split("|")
            target_coords = variables[2].split("|")
            target_tuple = (int(target_coords[0]), int(target_coords[1]), int(target_coords[2]))
            Munition(self.manager, weapon_type, MockLauncher(self.manager, launcher_coords, weapon_type), gl.get_coords_occupancy(self.manager, target_tuple).pop())
    
    
    def eventlogic_loop(self):
        # move event_if from ids_not_done_or_active to currently_active ----- #
        triggerd_ids = set()
        for event_id in self.ids_not_done_or_active:
            triggerd = self.interpret_condition(event_id, "TRIGGER")
            if triggerd:
                print(triggerd)
                triggerd_ids.add(triggerd)
        for event_id in triggerd_ids:
            self.ids_not_done_or_active.remove(event_id)
            self.currently_active_events.add(event_id)
        # execute event function -------------------------------------------- #
        for event_id in self.currently_active_events:
            print("start occurence: ", event_id)
            self.interpret_occurence(event_id)
        # delete if DONE ---------------------------------------------------- #
        done_ids = set()
        for event_id in self.currently_active_events:
            done = self.interpret_condition(event_id, "DONE")
            if done:
                print(done)
                done_ids.add(done)
        for done_id in done_ids:
            self.currently_active_events.remove(done_id)
        
    

            
            

            
