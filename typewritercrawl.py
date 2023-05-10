# -*- coding: utf-8 -*-
"""
Created on Fri May  5 07:38:08 2023

Provides an object with superclass pygame.Sprite, which prints text to the 
screen like a typewriter. The text automaticly is moved upwards so it stays 
within the predefined space, with the topmost rows disappearing, below the top
edge. Text can be colored differently for each line. After the whole text is 
printed to the screen, a scrollbar appears, with which the whole text can be 
reviewed, alternativly the object deletes itsself after n frames.

Dependencies:
-------------
pygame - Community Edition
    pip install pygame-ce
    
string.py
    Standard library, common string operations.
    
settings.py
    Containing constants for UI_INTERFACE_LAYER, UI_TRANSPARENCY, FONTSIZE.
    
observer.py optional
    Can be used as one way to pass events to the Button object.

@author: Maximilian Hauser
"""


# import section ------------------------------------------------------------ #
import pygame as pg
import string as string_module
from settings import FONTSIZE, UI_INTERFACE_LAYER, UI_TRANSPARENCY


class TypewriterCrawl(pg.sprite.Sprite):
    """
    Creates a object with superclass pygame.Sprite, which essentially functions 
    as a button, that executes a linked function, when released.
    
    Attributes:
    -----------
    self.game = game
        Main game loop object.
    
    self.text_in = text_in
        Static text to be displayed as a typewritercrawl.
    
    self.text_splitted = text_in.split("#")
        Text splitted at the "#", each resulting string represents a new line.
    
    self.text_rows = len(self.text_splitted)
        Number of individial strings/lines.
    
    self.height_rows_total = self.text_rows * FONTSIZE
        Height of all text rows in pixel.
    
    self.height_ratio = round(height / self.height_rows_total, 3)
        
    
    self.colors = ["white", "darkslategray1"]
        Colors to be used for the text.
    
    self.colors_index = colors_index
        List indexing each line to a color to be used.

    self.x = x
        Topleft position of the button, in pixel from the left edge of the screen.
    
    self.y = y
        Topleft position of the button, in pixel from the top edge of the screen.
    
    self.width = width
        Width of the Surface in pixel.
    
    self.height = height
        Heigth of the Surface in pixel.
    
    self.scrollbar_height = self.height or self.height_ratio * self.height
        Height of the scrollbar in pixel, dependent on the total height of the 
        rendered text. 
    
    self.sb_d = self.height - self.scrollbar_height
        Difference between surface height and scrollbar height.
    
    self.t_d = self.height_rows_total - self.height
        Difference between rendered text height and surface height.
    
    self.relative_y_traverse = self.t_d / self.sb_d or 0
        Position of the scrollbar relative to the scrolled text.
    
    self._layer = UI_INTERFACE_LAYER
        Layer responsible for the order in which objects are drawn unto the screen.
    
    self.game.text_crawl_grp.add(self)
        Add self to sprites.Group text_crawl_grp.
    
    self.abc_lst = list(string_module.ascii_lowercase)
        List containing all lower case letters as individual strings, for use
        as key in self.row_dct.
    
    self.row_dct = dict()
        Dictionary containing the current values for each row of text.
        {self.abc_lst[i]: {"row_y" : FONTSIZE * i,
                           "letters_printed" : 0,
                           "letters_max" : len(self.text_splitted[i]),
                           "row_text" : self.text_splitted[i],
                           "row_color" : current_color}
                          }
    
    self.speed = 1
        Speed with which letters are printed, rows moved upwards and at which
        in frames to countdown to deletion counts if activated.
        
    self.cooldown = 0
        Cooldown in frames between each letter being printed. Default +=10 after
        each letter is printed, -= self.speed.
        
    self.finished = False
        Boolean, set to True if all letters are printed. Begins countdown to
        self.kill, or displays scrollbar if True.
        
    self.last_printed_row = 0
        Number from the top that still printed numbers.
        
    self.delete_frames = delete_frames
        Boolean, delete in n frames after completion of printing the text.
        
    self.state = "unpressed"
        State of the scrollbar, used for functionality and animation.
        
    self.scrollbar_mask = None
        Mask generated from the Surface of the scrollbar.
        
    self.scrollbar_y = self.height - self.scrollbar_height
        Height of the Scrollbar for drawing.
        
    self.double_width = ["w", "W"]
        Letters in the current font, that have double the width than the rest.
        
    self.image = pg.Surface((self.width, self.height))
        Surface to be used as canvas for text and scrollbar.
    
    self.image.fill("black")
        Fill Surface with color black.
    
    self.image.set_colorkey("black")
        Set transparency color to black.
    
    self.image.set_alpha(UI_TRANSPARENCY)
        Set transparency to UI_TRANSPARENCY.
    
    self.rect = self.image.get_rect()
        Get Rect from Surface.
    
    self.rect.topleft = (self.x, self.y)
        Set Rect top left position to (x,y).
        
        
    Methods:
    --------
    update(self) -> None:
        Update function to be used in combination with the main game loop to
        update the state of the typewritercrawl.
        
    msbtn_down(self, pos:tuple, button:int) -> bool:
        Checks wether the event position overlaps with the object.
        
    handle_events(self, event:int) -> None:
        Changes the state of the button object, based on passed event.
        
    Examples:
    ---------
    test_text = "hello world!#hello world!#hello world!#hello world!#hello world!#hello world!"
    colors_index = [0,0,1,0,0,0]
    typewriter_crawl = sp.TypewriterCrawl(self, 100, 50, 300, 60, test_text, colors_index, delete_frames = None)
    self.observer.subscribe(pg.MOUSEBUTTONDOWN, typewriter_crawl)
    self.observer.subscribe(pg.MOUSEBUTTONUP, typewriter_crawl)
    self.observer.subscribe(pg.MOUSEMOTION, typewriter_crawl)
    self.observer.subscribe(self.E_IDLE, typewriter_crawl)
    """
    def __init__(self, game:object, x:int, y:int, width:int, height:int, text_in:str, colors_index:list, delete_frames = None) -> object:
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        self.text_in = text_in
        self.text_splitted = text_in.split("#")
        self.text_rows = len(self.text_splitted)
        self.height_rows_total = self.text_rows * FONTSIZE
        self.height_ratio = round(height / self.height_rows_total, 3)
        self.colors = ["white", "darkslategray1"]
        self.colors_index = colors_index

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        if self.height_ratio >= 1:
            self.scrollbar_height = self.height
        else:
            self.scrollbar_height = self.height_ratio * self.height
        
        self.sb_d = self.height - self.scrollbar_height
        self.t_d = self.height_rows_total - self.height
        
        if self.sb_d != 0:
            self.relative_y_traverse = self.t_d / self.sb_d
        else:
            self.relative_y_traverse = 0
        
        self._layer = UI_INTERFACE_LAYER
        self.game.text_crawl_grp.add(self)
        
        self.abc_lst = list(string_module.ascii_lowercase)
        
        self.row_dct =dict()
        for i in range(self.text_rows):
            current_color = self.colors[self.colors_index[i]]
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
        self.last_printed_row = 0
        self.delete_frames = delete_frames
        self.state = "unpressed"
        self.scrollbar_mask = None
        
        self.scrollbar_y = self.height - self.scrollbar_height
        
        self.double_width = ["w", "W"]
        
        # surface for text -------------------------------------------------- #
        self.image = pg.Surface((self.width, self.height))
        self.image.fill("black")
        self.image.set_colorkey("black")
        self.image.set_alpha(UI_TRANSPARENCY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        
    def update(self) -> None:
        """
        Update function to be used in combination with the main game loop to
        update the state of the typewritercrawl.
        
        Parameters:
        -----------
        self : Object
            Access to object attributes of self.
        
        Returns:
        --------
        None
        """
        if not self.finished:
            # logic for having text slowly crawl up ------------------------- #
            for i in range(self.text_rows):
                row_name = self.abc_lst[i]
                letters_printed = self.row_dct[row_name]["letters_printed"]
                if letters_printed != 0:
                    self.last_printed_row = i
                else:
                    break
        
            lowest_y_printed = self.row_dct[self.abc_lst[self.last_printed_row]]["row_y"]
            if lowest_y_printed > self.height - 2 * FONTSIZE:
                for i in range(self.text_rows):
                    row_name = self.abc_lst[i]
                    self.row_dct[row_name]["row_y"] -= self.speed / 10
        
            # logic for progressive printing of text ------------------------ #
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
        
        # delete after set time in self.speed frames ------------------------ #
        elif self.delete_frames != None:
            if self.delete_frames >= 0:
                self.delete_frames -= self.speed
            else:
                self.kill()
        
                
        # paint over previous image before blitting new image --------------- #
        self.image.fill("black")
        
        # provide scrollbar to reread hidden text if permanent -------------- #
        if self.delete_frames == None and self.finished:
                
            if self.state == "unpressed":
                pg.draw.rect(self.image, "darkslategray3", ((self.width - 10, self.scrollbar_y), (10, self.scrollbar_height)), 0, 5)
                pg.draw.rect(self.image, "darkslategray1", ((self.width - 10, self.scrollbar_y), (10, self.scrollbar_height)), 2, 5)
            if self.state == "pressed":
                pg.draw.rect(self.image, "darkslategray4", ((self.width - 10, self.scrollbar_y), (10, self.scrollbar_height)), 0, 5)
                pg.draw.rect(self.image, "darkslategray1", ((self.width - 10, self.scrollbar_y), (10, self.scrollbar_height)), 2, 5)
                    
            self.scrollbar_mask = pg.mask.from_surface(self.image)
                
            
        # logic for blitting text to screen --------------------------------- #
        for i in range(self.text_rows):
            
            row_name = self.abc_lst[i]
            row_color = self.row_dct[row_name]["row_color"]
            last_letter = self.row_dct[row_name]["letters_printed"]
            row_text = self.row_dct[row_name]["row_text"][0:last_letter]
            rendered_txt = self.game.font2.render(row_text, True, row_color)
            self.image.blit(rendered_txt, (0, self.row_dct[row_name]["row_y"]))
     
        
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
        touching = self.rect.collidepoint(pos) and self.scrollbar_mask.get_at(pos_in_mask)

        return touching

    def handle_events(self, event:int) -> None:
        """
        Changes the state of the button object, based on passed event.
        
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
        if self.state == "unpressed":
            if event.type == pg.MOUSEBUTTONDOWN:
                self.state = "pressed"
                
        if self.state == "pressed":
            if event.type == pg.MOUSEBUTTONUP:
                self.state = "unpressed"
                
            elif event.type == self.game.E_IDLE:
                pos_in_mask = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
                touching = self.rect.collidepoint(event.pos) and self.scrollbar_mask.get_at(pos_in_mask)
                if not touching:
                    self.state = "unpressed"        
                
            elif event.type == pg.MOUSEMOTION:
                (rel_x, rel_y) = event.rel
                
                # y_mousemovement is up or none ----------------------------- #
                if rel_y <= 0:
                    # scrollbar is not in its topmost position -------------- #
                    if self.scrollbar_y > 0:
                        
                        self.scrollbar_y += rel_y
                        for i in range(self.text_rows):
                            row_name = self.abc_lst[i]
                            self.row_dct[row_name]["row_y"] -= rel_y * self.relative_y_traverse
                     
                    # scrollbar is in its topmost position or past it ------- #
                    else:
                        self.scrollbar_y = 0
                        for i in range(self.text_rows):
                            row_name = self.abc_lst[i]
                            self.row_dct[row_name]["row_y"] = FONTSIZE * i
                            
                # y_mousemovement is downwards ------------------------------ #        
                else:
                    # scrollbar is not in its downwardmost position --------- #
                    if self.scrollbar_y < self.height - self.scrollbar_height:
                        self.scrollbar_y += rel_y
                        for i in range(self.text_rows):
                            row_name = self.abc_lst[i]
                            self.row_dct[row_name]["row_y"] -= rel_y * self.relative_y_traverse
                    
                    # scrollbar is in its downwardmost position ------------- #
                    else:
                        self.scrollbar_y = self.height - self.scrollbar_height
                        for i in range(self.text_rows):
                            row_name = self.abc_lst[i]
                            self.row_dct[row_name]["row_y"] = (self.height - self.height_rows_total) + (FONTSIZE * i)
                        