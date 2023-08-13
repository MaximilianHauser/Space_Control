"""
Created on Sat May  6 21:05:53 2023

Provides an object with superclass pygame.Sprite, that creates a tile, which 
can be used to create a hexagon tile map. It also holds the event management to 
handle game interactions on the map, such as unit movement or attacks.

Dependencies:
-------------
pygame - Community Edition
    pip install pygame-ce
    
settings.py
    Containing constants for UI_MAPINFO_LAYER, UI_TRANSPARENCY and FONTSIZE.
    
observer.py
    Passes events to the tile.

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
import pygame as pg
import hexlogic as hl
import gamelogic as gl
import animations_logic as al
from dropdownmenu import DropDownMenu
from attribute_dicts.t_attr import t_dict
from settings import TERRAIN_LAYER, WIN_WIDTH, WIN_HEIGHT


# Tile class ---------------------------------------------------------------- #
class Tile(pg.sprite.Sprite):
    """
    Creates an object with superclass pygame.Sprite, that creates a tile, which 
    can be used to create a hexagon tile map. It also holds the event management to 
    handle game interactions on the map, such as unit movement or attacks.
    
    Attributes:
    -----------
    self.game = game
        Main game loop object.
    
    self.q = q
        Cube coordinate q.
    
    self.r = r
        Cube coordinate r.
    
    self.s = s
        Cube coordinate s.
    
    self.t = t
        Terrain type.
    
    self._layer = TERRAIN_LAYER
        Layer responsible for the order in which objects are drawn unto the screen.
    
    self.game.all_sprites.add(self)
        Add self to sprites.Group all_sprites.
    
    self.game.tile_grp.add(self)
        Add self to sprites.Group tile_grp.
    
    x, y = hl.hex_to_pixel((q,r,s))
        x and y pixel coordinates for center position on screen.
    
    self.x = x + WIN_WIDTH / 2
        Centers the initial map position.
    
    self.y = y + WIN_HEIGHT / 2
        Centers the initial map position.
    
    self.k = v
        Custom attributes based on t_dict.
            
    self.mask_image = self.game.sprite_tile_mask
        Assigns an image, from which the mask will be drawn.
    
    self.image = self.original_image
        Image of the tile, without any animations applied.
    
    self.mask = pg.mask.from_surface(self.mask_image)
        Creates mask from the Surface.
    
    self.rect = self.mask.get_rect()
        Create a Rect from the mask image.
    
    self.rect.center = (self.x, self.y)
        Position the center of the tile at x and y.
    
    self.last_click_time = 0
        Last time the tile was clicked on.
    
    self.unit = None
        Attribute that tracks wether or not the tile contains a unit.
    
    self.fog_of_war = True
        Attribute that tracks wether or not the tile is revealed to a unit of 
        the player.
    
    self.ddm_open = False
        Attribute that tracks wether or not a dropdownmenu in relation to the 
        tile is currently open.
        
    Methods:
    --------
    update(self) -> None:
        Update function to be used in combination with the main game loop to
        update the state of the tile.
        
    msbtn_down(self, pos:tuple, button:int) -> bool:
        Checks wether the event position overlaps with the object, for observer.
        
    handle_events(self, event:int) -> None:
        Changes the state of the tile object, based on passed event.
        
    Examples:
    ---------
    
    """
    def __init__(self, manager:object, q:int, r:int, s:int, t:str) -> object:
        pg.sprite.Sprite.__init__(self)
        self.manager = manager
        
        self.q = q
        self.r = r
        self.s = s
        
        self.qrs = (q, r, s)
        
        self.t = t
        
        self._layer = TERRAIN_LAYER
        self.manager.all_sprites.add(self)
        self.manager.tile_group.add(self)
        
        x, y = hl.hex_to_pixel((q,r,s))
        self.x = x + WIN_WIDTH / 2
        self.y = y + WIN_HEIGHT / 2
        
        for k, v in t_dict[t].items():
            if isinstance(v, str):
                setattr(self, k, eval(v))
            else:
                setattr(self, k, v)
                
        self.mask_image = self.manager.sprite_tile_mask
        self.image = self.original_image
        self.mask = pg.mask.from_surface(self.mask_image)
        self.rect = self.mask.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.last_click_time = 0
        self.unit = None
        self.fog_of_war = True
        self.ddm_open = False
        
        # attributes for ciws mechanics ------------------------------------- #
        self.ciws_dict = dict()
        
    def update(self, delta) -> None:
        """
        Update function to be used in combination with the main game loop to
        update the state of the tile.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.
        
        Returns:
        --------
        None
        """
        # attaching unit to tile if occupied -------------------------------- #
        self.unit = gl.tile_has_unit(self, [self.manager.unit_blufor_group, self.manager.unit_redfor_group])
           
        # tints tile depending on animation_state --------------------------- #
        if self.animation_state != None:
            if self.animation_state == "activated_unit_on_tile":
                self.image = al.tint_image(self.original_image, "azure2")
            elif self.animation_state == "enemy_unit_in_range":
                self.image = al.tint_image(self.original_image, "tomato")
            elif self.animation_state == "in_movement_range":
                self.image = al.tint_image(self.original_image, "yellow")
        else:
            self.image = self.original_image
            
        # tints tile, if it is not within visible range by a unit ----------- #
        self.fog_of_war = gl.check_fog_of_war(self, self.manager.unit_blufor_group, self.manager.tile_group)
        
        if self.fog_of_war is True:
            self.image = al.tint_image(self.image, "grey")
        
        # update ciws dict -------------------------------------------------- #
        self.ciws_dict = gl.get_ciws_cover(self)
                    
        # updates position -------------------------------------------------- #
        self.rect.center = (self.x, self.y)
    
    # checks if click is touching tile and click cooldown ------------------- #
    def msbtn_down(self, pos:tuple, button:int) -> bool:
        """
        Checks wether the event position overlaps with the object.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.
        
        pos : tuple
            A tuple containing the pixel coordinates of an event (x,y).
        
        button : int
            Integer representing the mousebutton pressed, 1 for left, 3 for right.
        
        Returns:
        --------
        True, if event collided with self.mask, else False.
        """
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
    def handle_events(self, event:int, delta:float) -> None:
        """
        Changes the state of the tile object, based on passed event.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.

        pos : tuple
            A tuple containing the pixel coordinates of an event (x,y).
        
        Returns:
        --------
        None
        """
        # handle events related to mouse clicks on tile --------------------- #
        if event.type == pg.MOUSEBUTTONDOWN:
            
            # variables for wether or not there is a unit on the tile ------- #
            blufor_activated = None
            unit_on_tile = None
            
            # wether there is a blufor unit on tile and if its activated ---- #
            for unit in self.manager.unit_blufor_group:
                if unit.q == self.q and unit.r == self.r and unit.s == self.s:
                    unit_on_tile = unit
                if unit.activated == True:
                    blufor_activated = unit
            
            # wether there is a redfor unit on tile ------------------------- #
            redfor_on_tile = False
            for unit in self.manager.unit_redfor_group:
                if unit.q == self.q and unit.r == self.r and unit.s == self.s:
                    redfor_on_tile = True
                    unit_on_tile = unit
                    
            # left click on tile -------------------------------------------- #
            if event.button == 1:
                
                # redfor unit on tile --------------------------------------- #
                if redfor_on_tile:
                    if blufor_activated is not None:
                        if gl.in_weapon_range(blufor_activated, self.unit):
                            gl.attack_unit(blufor_activated, self.unit)
                
                # no unit on tile ------------------------------------------- #
                if unit_on_tile is None:
                    if blufor_activated is not None:
                        in_range = gl.in_mov_range(self, blufor_activated, self.manager.tile_group, "block_move")
                        neighbor = ((self.q, self.r, self.s)) in hl.neighbors((blufor_activated.q, blufor_activated.r, blufor_activated.s))
                        if in_range and neighbor:
                            gl.move_unit(self, blufor_activated)
                
            if event.button == 3:
                
                if blufor_activated is not None and hasattr(self.manager, "dropdownmenu") == False:
                    self.ddm_open = True
                    m_x, m_y = event.pos
                    kwargs = gl.get_kwargs_ddm(self, blufor_activated, self.manager.unit_blufor_group, self.manager.tile_group)
                    setattr(self.manager, "dropdownmenu", DropDownMenu(self.manager, m_x, m_y, 100, **kwargs))
                    self.manager.observer.subscribe(pg.MOUSEBUTTONDOWN, self.manager.dropdownmenu)
                    self.manager.observer.subscribe(pg.MOUSEBUTTONUP, self.manager.dropdownmenu)
                    self.manager.observer.subscribe(self.manager.E_IDLE, self.manager.dropdownmenu)
                

