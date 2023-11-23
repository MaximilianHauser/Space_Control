# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 18:30:36 2022

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import json

# misc ---------------------------------------------------------------------- #
from settings import WIN_WIDTH, WIN_HEIGHT, SCROLL_AREA, SCROLL_BUFFER, SCROLL_SPEED

    
# get the max or min value along an axis from a tile -------------------- #
# max_x = right map border, min_x = left map border --------------------- #
# max_y = bottom map border, min_y = top map border --------------------- #
def get_map_borders(tile_grp):
    
    max_x = 0
    min_x = WIN_WIDTH
    max_y = 0
    min_y = WIN_HEIGHT
    
    for tile in tile_grp:
        if tile.x > max_x:
            max_x = tile.x
        if tile.x < min_x:
            min_x = tile.x
        if tile.y > max_y:
            max_y = tile.y
        if tile.y < min_y:
            min_y = tile.y
            
    return max_x, min_x, max_y, min_y

# open a json-map-file and get the map data ----------------------------- #
def load_from_json(json_file):
    json_o = open(json_file)
    map_raw = json.load(json_o)
    json_o.close()
    return map_raw

def get_dim(map_lst):
    rows = len(map_lst)
    colums = len(map_lst[0])
    return colums, rows

def get_center(map_lst):
    columns, rows = get_dim(map_lst)
    r_correct = rows // 2 
    c_correct = columns // 2
    return c_correct, r_correct

def assign_qrs(map_raw):
    map_setup_lst = []
    columns, rows = get_dim(map_raw)
    c_correct, r_correct = get_center(map_raw)
    for col in range(columns):
        for row in range(rows):
            q = col
            r = row
            s = -q-r
            t = map_raw[r][q][0]
            if t is not None:
                u = map_raw[r][q][1]
                triggers = map_raw[r][q][2] if len(map_raw[r][q]) == 3 else None
                map_setup_lst.append((q, r, s, t, u, triggers))

    return map_setup_lst


def scroll_logic(manager, event, delta):
    """
    Provides scrolling logic by relatively changing the position of all_sprites.
    """
    
    mouse_pos_x, mouse_pos_y = event.pos
    max_x, min_x, max_y, min_y = get_map_borders(manager.tile_group)
    
    # cursor is at left edge of the screen ---------------------------------- #
    if mouse_pos_x < SCROLL_AREA:
        # if left map border <= SCROLL_BUFFER ------------------------------- #
        if min_x <= SCROLL_BUFFER:
            # scroll left (move sprites right) ------------------------------ #
            for sprite in manager.all_sprites:
                sprite.x += delta * SCROLL_SPEED
    
    # cursor is at right edge of the screen --------------------------------- #
    if mouse_pos_x > WIN_WIDTH - SCROLL_AREA:
        # if right map border >= WIN_WIDTH - SCROLL_BUFFER ------------------ #
        if max_x >= WIN_WIDTH - SCROLL_BUFFER:
            # scroll right (move sprites left) ------------------------------ #
            for sprite in manager.all_sprites:
                sprite.x -= delta * SCROLL_SPEED
    
    # cursor is at top edge of the screen ----------------------------------- #
    if mouse_pos_y < SCROLL_AREA:
        # if top map border <= SCROLL_BUFFER -------------------------------- #
        if min_y <= SCROLL_BUFFER:
            # scroll up (move sprites down) --------------------------------- #
            for sprite in manager.all_sprites:
                sprite.y += delta * SCROLL_SPEED
    
    # cursor is at bottom edge of the screen -------------------------------- #
    if mouse_pos_y > WIN_HEIGHT - SCROLL_AREA:
        # if bottom map border >= WIN_HEIGHT - SCROLL_BUFFER ---------------- #
        if max_y >= WIN_HEIGHT - SCROLL_BUFFER:
            # scroll down (move sprites up) --------------------------------- #
            for sprite in manager.all_sprites:
                sprite.y -= delta * SCROLL_SPEED


