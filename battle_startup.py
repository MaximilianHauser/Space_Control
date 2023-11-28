# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 14:35:59 2023

@author: Maximilian Hauser
"""
# import section ------------------------------------------------------------ #
import json


# --------------------------------------------------------------------------- #
startup_dict = {"Hello ": "World!"}

# creates json file and writes map to it ------------------------------------ #
with open('battle_startup.json', 'w') as file:
    json.dump(startup_dict, file)
