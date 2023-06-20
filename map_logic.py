# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 18:30:36 2022

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import json
import numpy as np
import pandas as pd
import pygame as pg
import hexlogic as hl
from settings import WIN_WIDTH, WIN_HEIGHT, SCROLL_AREA, SCROLL_BUFFER, SCROLL_SPEED


# MapLogic class ------------------------------------------------------------ #
class MapLogic:
    
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
        columns, rows = MapLogic.get_dim(map_lst)
        r_correct = rows // 2 
        c_correct = columns // 2
        return c_correct, r_correct
    
    def assign_qrs(map_raw):
        map_setup_lst = []
        columns, rows = MapLogic.get_dim(map_raw)
        c_correct, r_correct = MapLogic.get_center(map_raw)
        for col in range(columns):
            for row in range(rows):
                q = col
                r = row
                s = -q-r
                t = map_raw[r][q][0]
                if t is not None:
                    u = map_raw[r][q][1]
                    map_setup_lst.append((q, r, s, t, u))
    
        return map_setup_lst

    def create_graph_matrix(tile_grp):
        
        # individual tile coords for column/index names --------------------- #
        idx = list()
        
        for tile in tile_grp:
            idx.append((tile.q, tile.r, tile.s))
        
        # creating a set with all connections ------------------------------- #
        edges = set()
        
        for tile in tile_grp:
            tile_qrs = (tile.q, tile.r, tile.s)
            t_nbors_lst = hl.neighbors(tile_qrs[0], tile_qrs[1], tile_qrs[2])
            for nbor in t_nbors_lst:
                nbor_qrs = (nbor[0], nbor[1], nbor[2])
                for t in tile_grp:
                    if t.q == nbor[0] and t.r == nbor[1] and t.s == nbor[2]:
                        edges.add((tile_qrs, nbor_qrs))

        map_matrix = np.identity(len(idx))
        
        matrix_df = pd.DataFrame(map_matrix, index=idx, columns=idx)
        
        for edge in edges:
            matrix_df[edge[0]][edge[1]] = 1
            matrix_df[edge[1]][edge[0]] = 1
        
        matrix_df = matrix_df.astype("int64")
        
        return matrix_df

    def scroll_logic(manager, event):
        
        if event.type == pg.MOUSEMOTION or event.type == manager.E_IDLE:
            mouse_pos_x, mouse_pos_y = event.pos
            max_x, min_x, max_y, min_y = MapLogic.get_map_borders(manager.tile_grp)
            
            if mouse_pos_x < SCROLL_AREA:
                if max_x < WIN_WIDTH - SCROLL_BUFFER:
                    for sprite in manager.all_sprites:
                        sprite.x += SCROLL_SPEED
            
            if mouse_pos_x > WIN_WIDTH - SCROLL_AREA:
                if min_x > SCROLL_BUFFER:
                    for sprite in manager.all_sprites:
                        sprite.x -= SCROLL_SPEED
            
            if mouse_pos_y < SCROLL_AREA:
                if max_y < WIN_HEIGHT - SCROLL_BUFFER:
                    for sprite in manager.all_sprites:
                        sprite.y += SCROLL_SPEED
            
            if mouse_pos_y > WIN_HEIGHT - SCROLL_AREA:
                if min_y > SCROLL_BUFFER:
                    for sprite in manager.all_sprites:
                        sprite.y -= SCROLL_SPEED
