# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 07:19:00 2022

Will contain all hextile logic, specified as logic handling the relationship 
between cartesian coordinates and cube coordinates, for the purpose of defining 
the relative position of hexagon tiles on the screen. In addition it provides
calculations in regards to hextile map related formulas and algorythms.

Dependencies:
-------------
settings
    A custom python file containing the constants TILE_WIDTH and TILE_HEIGHT.
    

@author: Maximilian Hauser
"""

# import section ------------------------------------------------------------ #
from settings import TILE_WIDTH, TILE_HEIGHT

# Hexlogic class ------------------------------------------------------------ #
class HexLogic:
    """
    Methods:
    --------
    linint(a : int, b : int, t : float) -> float:
        Linear interpolation returns point at t of distance between a and b.
        
    cube_linint(obj_a:object, obj_b:object, t:float) -> tuple:
        Returns the hextile coordinates of a point situated at t part of the way from obj_a to obj_b.
        
    round_hex(qrs:tuple) -> tuple:
        Rounds each of the coordinates to the nearest integer.
        
    get_qrs(obj:object) -> tuple:
        Returns values of attributes q, r, s of obj.
        
    set_qrs(obj:object, q:int, r:int, s:int) -> None:
        Set q r and s attribute of obj to specified values.
        
    hex_to_pixel(qrs:tuple) -> tuple:
        Converts hex_coords to pixel_coords.
        
    pixel_to_hex(xy:tuple) -> tuple:
        Converts pixel_coords to hex_coords.
        
    neighbors(qrs:tuple) -> tuple:
        Return a list of coordinates of neighboring hexagons.
        
    distance(obj_a:object, obj_b:object) -> int:
        Returns distance from one object to another in a cube coordinate system.
        
    in_range(obj:object, n:int) -> set:
        Returns a set containing the cube coordinates of every hexagon in distance n from obj.
        
    line_draw(obj_a:object, obj_b:object) -> tuple:
        Draws a line from one hexagon to another, returns a tuple containing the hexagons with the center closest to the line.
        
    dist_lim_flood_fill(start_obj:object, n:int, obj_grp:(list, set, pg.sprite.Group), block_var:str) -> set:
        All cube coordinates within n distance from an object, factoring in block_var (variable if True blocks object).
    """

    def linint(a : int, b : int, t : float) -> float:
        """
        Linear interpolation returns point at t of distance between a and b.
        
        Parameters:
        -----------
        a : integer
            An object having a q, r and s attribute, with real number values.
        
        b : integer
            An object having a q, r and s attribute, with real number values.
        
        t : float
            Float denominating the distance between 
        
        Raises:
        -------
        TypeError: If the input is not an integer for a and b or a float for t.
        
        Returns:
        --------
        linint(float): Linear interpolation t part of the way from a to b.
        """
        
        linint = a + (b - a) * t
        return linint


    def cube_linint(obj_a:object, obj_b:object, t:float) -> tuple:
        """
        Returns the hextile coordinates of a point situated at t part of the way from obj_a to obj_b.
        
        Parameters:
        -----------
        obj_a : object
            An object having a q, r and s attribute, with real number values.
        
        obj_b : object
            An object having a q, r and s attribute, with real number values.
        
        t : float
            Float denominating the distance between 
        
        Raises:
        -------
        TypeError: If the input is not an object for obj_a and obj_b or a float for t.
        ValueError:
        
        Returns:
        --------
        linint_coords(tuple): The hextile coordinates of a point situated at the t part of the way from obj_a to obj_b.
        """
        q = HexLogic.linint(obj_a.q, obj_b.q, t)
        r = HexLogic.linint(obj_a.r, obj_b.r, t)
        s = HexLogic.linint(obj_a.s, obj_b.s, t)
        
        linint_coords = (q, r, s)
        
        return linint_coords


    def round_hex(qrs:tuple) -> tuple:
        """
        Rounds each of the coordinates to the nearest integer.
        
        Parameters:
        -----------
        qrs : Tuple
            A Tuple containing 3 real numerical values.
        
        Raises:
        -------
        TypeError: If the input is not a tuple.
        ValueError: If the input tuple is empty.
        
        Returns:
        --------
        rounded_qrs(tuple): The input tuple, each element rounded to the nearest integer. 
        """
        try:
            q_f, r_f, s_f = qrs
        except ValueError as ve:
            print(ve)
        
        q = round(q_f)
        r = round(r_f)
        s = round(s_f)

        q_diff = abs(q - q_f)
        r_diff = abs(r - r_f)
        s_diff = abs(s - s_f)

        if q_diff > r_diff and q_diff > s_diff:
            q = -r-s
        elif r_diff > s_diff:
            r = -q-s
        else:
            s = -q-r
        
        rounded_qrs = (q, r, s)
        
        return rounded_qrs
    

    def get_qrs(obj:object) -> tuple:
        """
        Returns values of attributes q, r, s of obj as tuple.
        
        Parameters:
        -----------
        obj : object
            An object having attributes q, r, s, values being integer.
        
        Raises:
        -------
        TypeError: If the input is not an object, or if the value of q, r or s is not an integer.
        
        Returns:
        --------
        qrs(tuple): The values of attributes q, r, s of obj as tuple.
        """
        try:
            q = obj.q
            r = obj.r
            s = obj.s
        except AttributeError as ae:
            print(ae)
        
        try:
            q:int
            r:int
            s:int
        except TypeError as te:
            print(te)
            
        qrs = (q, r, s)
        
        return qrs
    

    def set_qrs(obj:object, q:int, r:int, s:int) -> None:
        """
        Set q r and s attribute of obj to specified values.
        
        Parameters:
        -----------
        obj : object
            An object having attributes q, r, s, values being integer.
        
        Raises:
        -------
        TypeError: If obj input is not an object, or q, r or s is not an integer.
        AttributeError: If obj is missing q, r or s as attribute.
        
        Returns:
        --------
        None
        """
        try:
            obj.q = q
            obj.r = r
            obj.s = s
            
        except AttributeError as ae:
            print(ae)
    

    def hex_to_pixel(qrs:tuple) -> tuple:
        """
        Converts hex_coords to pixel_coords.
        
        Parameters:
        -----------
        qrs : Tuple
            A Tuple containing 3 real numerical values.
        
        Raises:
        -------
        TypeError: If qrs input is not a tuple, or q, r or s is not an integer.
        ValueError: If tuple does contain less than 4 variables.
        
        Returns:
        --------
        xy(tuple): The input coordinates of hexagon qrs converted to a 2-axis coordinates system xy.
        """
        try:
            q,r,s = qrs
        except ValueError as ve:
            print(ve)
        
        x = ((4/3)*q - (2/3)*r - (2/3)*s) * TILE_WIDTH * 0.375
        y = (r - s) * TILE_HEIGHT * 0.5
        
        xy = (x, y)
        
        return xy
    

    def pixel_to_hex(xy:tuple) -> tuple:
        """
        Converts pixel_coords to hex_coords.
        
        Parameters:
        -----------
        xy : Tuple
            A Tuple containing 2 real numerical values.
        
        Raises:
        -------
        TypeError: If xy input is not a tuple, or x or y is not an integer.
        ValueError: If tuple does contain less than 3 variables.
        
        Returns:
        --------
        qrs(tuple): The input cartesian coordinates tuple of xy converted to a hexagon coordinates system qrs.
        """
        try:
            x, y = xy
        except ValueError as ve:
            print(ve)
        
        q = (x / 2) / TILE_WIDTH * (8 / 3)
        r = (y / 2 - x / 4) / TILE_HEIGHT * 2
        s = -q-r
        
        qrs = (q,r,s)
        
        return qrs
    

    def neighbors(qrs:tuple) -> tuple:
        """
        Return a list of coordinates of neighboring hexagons.
        
        Parameters:
        -----------
        qrs : Tuple
            A Tuple containing 3 real numerical values.
        
        Raises:
        -------
        TypeError: If qrs input is not a tuple, or q, r or s is not an integer.
        ValueError: If tuple does contain less than 4 variables.
        
        Returns:
        --------
        nbors(set): A set containing all cube coordinates neighboring qrs.
        """
        q, r, s = qrs
        nbors = ((q+1,r,s-1), (q+1,r-1,s), (q,r-1,s+1), (q-1,r,s+1), (q-1,r+1,s), (q,r+1,s-1))
        return nbors
    

    def distance(obj_a:object, obj_b:object) -> int:
        """
        Returns distance from one object to another in a cube coordinate system.
        
        Parameters:
        -----------
        obj_a : Object
            An Object containing the attributes q, r and s, having integer values.
        obj_b : Object
            An Object containing the attributes q, r and s, having integer values.
        
        Raises:
        -------
        TypeError: If obj_a or obj_b is not an object.
        AttributeError: If obj_a or obj_b is missing q, r or s as an attribute.
        
        Returns:
        --------
        ab_dist(int): The distance between obj_a and obj_b in hexagon tiles.
        """
        try:
            a_q = getattr(obj_a, "q")
            a_r = getattr(obj_a, "r")
            a_s = getattr(obj_a, "s")
            b_q = getattr(obj_b, "q")
            b_r = getattr(obj_b, "r")
            b_s = getattr(obj_b, "s")
            
        except AttributeError as ae:
            print(ae)
        
        q_diff = abs(a_q - b_q)
        r_diff = abs(a_r - b_r)
        s_diff = abs(a_s - b_s)
        ab_dist = max(q_diff, r_diff, s_diff)
        
        return ab_dist
    

    def in_range(obj:object, n:int) -> set:
        """
        Returns a set containing the cube coordinates of every hexagon in distance n from obj.
        
        Parameters:
        -----------
        obj : Object
            An Object containing the attributes q, r and s, having integer values.
        n : Integer
            An Integer limiting the distance 
        
        Raises:
        -------
        TypeError: If obj is not an object or n is not an Integer.
        AttributeError: If obj is missing q, r or s as an Attribute.
        
        Returns:
        --------
        hex_in_range(set): A set containing all cube coordinates within distance n from obj.
        """
        try:
            o_q = getattr(obj, "q")
            o_r = getattr(obj, "r")
            o_s = getattr(obj, "s")
            
        except AttributeError as ae:
            print(ae)
        hex_in_range = set()
        
        for q in range(-n, n):
            for r in range(max(-n, -q-n), min(n, -q+n)):
                s = -q-r
                hex_in_range.add((o_q+q, o_r+r, o_s+s))
                
        return hex_in_range
    

    def line_draw(obj_a:object, obj_b:object) -> tuple:
        """
        Draws a line from one hexagon to another, returns a tuple containing the hexagons with the center closest to the line.
        
        Parameters:
        -----------
        obj_a : Object
            An Object containing the attributes q, r and s, having integer values.
        obj_a : Object
            An Object containing the attributes q, r and s, having integer values.
        
        Raises:
        -------
        TypeError: If obj_a or pbj_b is not an object.
        AttributeError: If obj_a or obj_b is missing q, r or s as an Attribute.
        
        Returns:
        --------
        line_hexes_coords(tuple): A tuple containing all cube cordinates from obj_a to obj_b inclusive.
        """
        ab_dist = HexLogic.distance(obj_a, obj_b)
        
        line_hexes_coords = list()
        
        for i in range(0, ab_dist):
            qrs_f = HexLogic.cube_linint(obj_a, obj_b, 1.0/ab_dist * i)
            item = HexLogic.round_hex(qrs_f)
            line_hexes_coords.append(item)
            
        return tuple(line_hexes_coords)
    

    def dist_lim_flood_fill(start_obj:object, n:int, obj_grp:(list, set), block_var:str) -> set:
        """
        All cube coordinates within n distance from an object, factoring in block_var (variable if True blocks object).
        
        Parameters:
        -----------
        start_obj : Object
            An Object containing the attributes q, r and s, having integer values.
        n : Integer
            The number of moves from start object to fill.
        obj_grp : List, Set or SpriteGroup
            A container containing objects adjacent to each other in a cube coordinate system (tiles in tilemap).
        block_var : String
        
        Raises:
        -------
        TypeError: If obj_a or pbj_b is not an object.
        AttributeError: If obj_a or obj_b is missing q, r or s as an Attribute.
        
        Returns:
        --------
        visited(set): A tuple containing all cube cordinates from obj_a to obj_b inclusive.
        """
        try:
            start =  (start_obj.q, start_obj.r, start_obj.s)
        except AttributeError as ae:
            print(ae)
        
        visited = set() # set, so duplicate values are ignored
        visited.add(start)
        fringes = []
        fringes.append([start])
        

        for k in range(1, n + 1):

            fringes.append([])
            for t_coords in fringes[k-1]:
                for d in range(0,6): # 6 neighbors per hex => 6 items in nbors_lst
                    current_coord = (t_coords[0], t_coords[1], t_coords[2])
                    neighbor = HexLogic.neighbors(current_coord)[d]
                    for obj in obj_grp:
                        if (obj.q, obj.r, obj.s) == neighbor:
                            blocked = getattr(obj, block_var)
                            if not blocked:
                                visited.add(neighbor)
                                fringes[k].append(neighbor)

        return visited
    
    
