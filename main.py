# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:09:00 2023

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import sys
import pygame as pg

# generell game files ------------------------------------------------------- #
from engine import Engine
from settings import WIN_WIDTH, WIN_HEIGHT

# states -------------------------------------------------------------------- #
from splashscreen import SplashScreen
from mainmenu import MainMenu
from missionselect import MissionSelect
from briefing import Briefing
from battle import Battle
from debriefing import Debriefing
from credits import Credits

# pygame-ce and mixer init -------------------------------------------------- #
pg.init()
pg.mixer.init()

# display setup ------------------------------------------------------------- #
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Space Control")
pg.display.set_icon(pg.image.load("./img/window_icon.png"))

# initial state instances --------------------------------------------------- #
splashscreen = SplashScreen()
mainmenu = None #MainMenu()
missionselect = None #MissionSelect()
briefing = None #Briefing()
battle = None #BattleNew()
debriefing = None #Debriefing()
credits = None #Credits()

# states dictionary --------------------------------------------------------- #
states = {
    "SPLASH_SCREEN":
        {"constructor":SplashScreen(),
         "instance":splashscreen},
        
    "MAIN_MENU":
        {"constructor":MainMenu() ,
         "instance":mainmenu},
        
    "MISSION_SELECT":
        {"constructor":MissionSelect() ,
         "instance":missionselect},
        
    "BRIEFING":
        {"constructor":Briefing(),
         "instance":briefing},
        
    "BATTLE":
        {"constructor":Battle(),
         "instance":battle},

    "DEBRIEFING":
        {"constructor":Debriefing(),
         "instance":debriefing},
        
    "CREDITS":
        {"constructor":Credits(),
         "instance":credits}
            }

engine = Engine(screen, states, "SPLASH_SCREEN")
engine.run()

pg.quit()
sys.exit()
