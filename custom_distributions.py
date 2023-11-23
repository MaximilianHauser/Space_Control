# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 12:19:27 2023

@author: Maximilian Hauser
"""


def custom_cauchy_distribution(x, *, abs_y=True):
    """
    Function intercepts the x-axis at -1.075 and 1.075, the y-axis at 1. Roughly 
    has a plateau from -0.5 to 0.5, can be used to model acceleration deceleration 
    of spaceship movement. (absolute return values enforced to avoid any negative 
    value sinks, technically curently not needed)
    """
    
    y = 1 / ( 2/3 + x**4 ) - 0.5
    
    if abs_y:
        return abs(y)
    else:
        return y
    



