# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 10:03:53 2022

Will contain the main game loop and functionality.

@author: Maximilian
"""

# import section ------------------------------------------------------------ #
import pygame as pg
import sys

# settings section ---------------------------------------------------------- #
# screen dimensions
WIN_WIDTH = 640 #324
WIN_HEIGHT = 480 #720

# times the screen is updated per min
FPS = 60

# game class ---------------------------------------------------------------- #
class Game:
    def __init__(self):

        # initialize all imported pygame modules / init sounds module ------- #
        pg.init()
        pg.mixer.init()
        
        # Setup pygame / window --------------------------------------------- #
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.caption = pg.display.set_caption('Space Control')
        self.window_icon = pg.display.set_icon(pg.image.load('./img/window_icon.png'))
        self.clock = pg.time.Clock()
        
    def new_battle(self):
        self.playing = True
                                
    def events(self):
        
        # process input / events -------------------------------------------- #
        for event in pg.event.get():
            
            # handles exiting the program via red, right, top x ------------- #
            if event.type == pg.QUIT:
                self.playing = False
        
        # restricts speed of loop ------------------------------------------- #
        self.clock.tick(FPS)
    
    def update(self):
        # update ------------------------------------------------------------ #
        pass
    
    def draw(self):
        # draw/render ------------------------------------------------------- #
        self.screen.fill('black')
        
        # after drawing / flip display -------------------------------------- #
        pg.display.flip()
    
    def main_loop(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
           
g = Game()

g.new_battle()
g.main_loop()

pg.quit()
sys.exit()