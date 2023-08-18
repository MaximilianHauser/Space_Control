# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 18:20:51 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import sys
import pygame as pg

# misc ---------------------------------------------------------------------- #
from settings import FPS


# Game Engine class --------------------------------------------------------- #
class Engine:
    def __init__(self, screen, states, start_state, fps = FPS):
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = fps
        self.states = states
        self.state_name = start_state
        self.previous_state = None
        self.states[self.state_name]["instance"] = self.states[self.state_name]["constructor"]()
        self.state = self.states[self.state_name]["instance"]
        self.delta = 0
        
        # define custom_events ---------------------------------------------- #
        self.E_IDLE = 32867

    def event_loop(self, delta):
        # post custom_event "IDLE" ------------------------------------------ #
        if not pg.event.peek(pg.MOUSEMOTION):
            if not pg.event.peek(pg.MOUSEBUTTONDOWN):
                mouse_pos = pg.mouse.get_pos()
                event_data = {'pos': mouse_pos}
                pg.event.post(pg.event.Event(self.E_IDLE, event_data))
        # pass event to currently active state ------------------------------ #        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            else:
                self.state.event(event, delta)

    def flip_state(self):
        self.previous_state = self.state_name
        next_state = self.state.next_state
        self.state.leave()
        self.state_name = next_state
        persistent = self.state.persistent
        self.states[self.state_name]["instance"] = self.states[self.state_name]["constructor"]()
        self.state = self.states[self.state_name]["instance"]
        self.state.startup(persistent)
        self.states[self.previous_state]["instance"] = None

    def update(self, delta):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(delta)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            self.delta = self.clock.tick(self.fps) * 0.001
            self.event_loop(self.delta)
            self.update(self.delta)
            self.draw()
            pg.display.update()
