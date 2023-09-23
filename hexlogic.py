"""
Created on Fri Sep  9 07:19:00 2022

These functions assume you're using objects to represent tiles, units, items, 
etc on your map that are based on a rectangular shape, having a width and height,
the hexagon being drawn onto it, an example for a 64x64 tile is provided. The
logic was written for and tested with pygame sprite objects.

Contains all hextile logic, specified as logic handling the relationship 
between cartesian coordinates and cube coordinates, for the purpose of defining 
the relative position of hexagon tiles on the screen. In addition it provides
calculations in regards to hextile map related formulas and algorithms.
I plan on adding hextile specific pathfinding in the future.

Dependencies:
-------------
settings
    A python file containing the constants TILE_WIDTH and TILE_HEIGHT.
    
Functions:
----------
linint(a : int, b : int, t : float) -> float:
    Linear interpolation returns point at t of distance between a and b.
    
cartesian_linint(xy_a:tuple, xy_b:tuple, t:float) -> tuple:
    Linear interpolation returns point at t of distance between a and b on
    a cartesian coordinates system.
    
cube_linint(obj_a:object, obj_b:object, t:float) -> tuple:
    Returns the hextile coordinates of a point situated at t part of the way 
    from obj_a to obj_b.
    
round_hex(qrs:tuple) -> tuple:
    Rounds each of the coordinates to the nearest integer.
    
get_qrs(obj:object) -> tuple:
    Returns values of attributes q, r, s of obj.
    
set_qrs(obj:object, q:int, r:int, s:int) -> None:
    Set q r and s attribute of obj to specified values.
    
hex_to_pixel(qrs:tuple) -> tuple:
    Converts cube coordinates to pixel coordinates.
    
pixel_to_hex(xy:tuple) -> tuple:
    Converts pixel coordinates to cube coordinates.
    
neighbors(qrs:tuple) -> tuple:
    Return a list of coordinates of neighboring hexagons.
    
distance(obj_a:object, obj_b:object) -> int:
    Returns distance from one object to another in a cube coordinate system.
    
in_range(obj:object, n:int) -> set:
    Returns a set containing the cube coordinates of every hexagon in 
    distance n from obj.
    
line_draw(obj_a:object, obj_b:object) -> tuple:
    Draws a line from one hexagon to another, returns a tuple containing 
    the hexagons with the center closest to the line.
    
dist_lim_flood_fill(start_obj:object, n:int, obj_grp:(list, set, pg.sprite.Group), block_var:str) -> set:
    All cube coordinates within n distance from an object, factoring in block_var (variable if True blocks object).

@author: Maximilian Hauser
@references: redblobgames.com (Amit Patel)
https://www.redblobgames.com/grids/hexagons/
https://www.redblobgames.com/grids/hexagons/implementation.html
https://www.redblobgames.com/grids/hexagons/codegen/output/lib.py
"""


# import section ------------------------------------------------------------ #
# libraries ----------------------------------------------------------------- #
import unittest
from unittest.mock import Mock
import numpy as np
import pandas as pd

# misc ---------------------------------------------------------------------- #
from settings import TILE_WIDTH, TILE_HEIGHT


# Hexlogic functions -------------------------------------------------------- #
def linint(a:int, b:int, t:float) -> float:
    """
    Linear interpolation returns point at t of distance between a and b.
    
    Parameters:
    -----------
    a : integer
        A real numeric value, representing a point on a line.
        
    b : integer
        A real numeric value, representing a point on a line.
        
    t : float
        Float denominating the distance between a and b in percent.
        
    Raises:
    -------
    TypeError: If a, b or t is not numeric.
        
    Returns:
    --------
    linint(float): Linear interpolation t part of the way from a to b.
    """
    linint = a + (b - a) * t
            
    return linint
    
    
def cartesian_linint(xy_a:tuple, xy_b:tuple, t:float) -> tuple:
    """
    Linear interpolation returns point at t distance between a and b in
    a cartesian coordinates system.
        
    Parameters:
    -----------
    xy_a : tuple
        A tuple consisting of an integer for the x and y value.
        
    xy_b : tuple
        A tuple consisting of an integer for the x and y value.
        
    t : float
        Float denominating the distance between point a and b in percent.
        
    Raises:
    -------
    ValueError: If xy_a or xy_b is not a tuple.
    UnboundLocalError:
        If one of the tuples xy_a or xy_b contains more than 2 values
        or either xy_a or xy_b is not a tuple.
        
    Returns:
    --------
    cartesian_linint(tuple): Linear interpolation t part of the way from a to b.
    """
    x_a, y_a = xy_a
    x_b, y_b = xy_b
        
    x = linint(x_a, x_b, t)
    y = linint(y_a, y_b, t)
        
    cartesian_linint = (x, y)
        
    return cartesian_linint
    

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
        Float denominating the distance between point a and b in percent.
        
    Raises:
    -------
    AttributeError: If one of the objects is missing an q, r or s attribute.
        
    Returns:
    --------
    linint_coords(tuple): The hextile coordinates of a point situated at the t part of the way from obj_a to obj_b.
    """
    a_q = getattr(obj_a, "q")
    b_q = getattr(obj_b, "q")
    a_r = getattr(obj_a, "r")
    b_r = getattr(obj_b, "r")
    a_s = getattr(obj_a, "s")
    b_s = getattr(obj_b, "s")
        
    q = linint(a_q, b_q, t)
    r = linint(a_r, b_r, t)
    s = linint(a_s, b_s, t)
        
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
    ValueError: If the input tuple is empty.
    UnboundLocalError: If qrs contains more than 3 values or is not a tuple.
        
    Returns:
    --------
    rounded_qrs(tuple): The input tuple, each element rounded to the nearest integer. 
    """

    q_f, r_f, s_f = qrs
        
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
    AttributeError: If obj is missing q, r or s as attribute.
        
    Returns:
    --------
    qrs(tuple): The values of attributes q, r, s of obj as tuple.
    """

    q = getattr(obj, "q")
    r = getattr(obj, "r")
    s = getattr(obj, "s")
            
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
    TypeError: If q, r or s is not an integer.
        
    Returns:
    --------
    None
    """
    q_isint = isinstance(q, int)
    r_isint = isinstance(r, int)
    s_isint = isinstance(s, int)
    
    if q_isint and r_isint and s_isint:
        setattr(obj, "q", q)
        setattr(obj, "r", r)
        setattr(obj, "s", s)
        
    else:
        raise TypeError
    

def hex_to_pixel(qrs:tuple) -> tuple:
    """
    Converts cube coordinates to pixel coordinates.
    
    Parameters:
    -----------
    qrs : Tuple
        A Tuple containing 3 real numerical values.
        
    Raises:
    -------
    ValueError: If tuple does contain less than 3 variables.
    UnboundLocalError: If qrs contains more than 3 values or is not a tuple.
        
    Returns:
    --------
    xy(tuple): The input coordinates of hexagon qrs converted to a 2-axis coordinates system xy.
    """
    q,r,s = qrs
        
    x = ((4/3)*q - (2/3)*r - (2/3)*s) * TILE_WIDTH * 0.375
    y = (r - s) * TILE_HEIGHT * 0.5
        
    xy = (x, y)
        
    return xy
    

def pixel_to_hex(xy:tuple) -> tuple:
    """
    Converts pixel coordinates to cube coordinates.
        
    Parameters:
    -----------
    xy : Tuple
        A Tuple containing 2 real numerical values.
        
    Raises:
    -------
    TypeError: If x or y is not numeric.
    ValueError: If tuple does contain less than 3 variables.
    UnboundLocalError: If xy contains more than 2 values or is not a tuple.
        
    Returns:
    --------
    qrs(tuple): The input cartesian coordinates tuple of xy converted to a hexagon coordinates system qrs.
    """

    x, y = xy
        
    q = (x / 2) / TILE_WIDTH * (8 / 3)
    r = (y / 2 - x / 4) / TILE_HEIGHT * 2
    s = -q-r
        
    qrs = (q,r,s)
        
    return qrs
    

def neighbors(qrs:tuple) -> tuple:
    """
    Returns a tuple of coordinates of neighboring hexagons.
        
    Parameters:
    -----------
    qrs : Tuple
        A Tuple containing 3 real numerical values.
        
    Raises:
    -------
    TypeError: If q, r or s is not numeric.
    ValueError: If tuple does contain less than 3 variables.
    UnboundLocalError: If qrs contains more than 3 values or is not a tuple.
        
    Returns:
    --------
    nbors(set): A set containing all cube coordinates neighboring qrs.
    """

    q, r, s = qrs
        
    nbors = ((q+1,r,s-1), (q+1,r-1,s), (q,r-1,s+1), (q-1,r,s+1), (q-1,r+1,s), (q,r+1,s-1))
        
    return nbors
    

def distance(obj_a:(object, tuple), obj_b:(object, tuple), is_obj:bool=True) -> int:
    """
    Returns distance from one object to another in a cube coordinate system.
        
    Parameters:
    -----------
    obj_a : Object
        An Object containing the attributes q, r and s, having numerical values.
        
    obj_b : Object
        An Object containing the attributes q, r and s, having numerical values.
        
    Raises:
    -------
    AttributeError: If obj_a or obj_b is missing q, r or s as an attribute.
        
    Returns:
    --------
    ab_dist(int): The distance between obj_a and obj_b in hexagon tiles.
    """
    
    if is_obj:
        a_q = getattr(obj_a, "q")
        a_r = getattr(obj_a, "r")
        a_s = getattr(obj_a, "s")
        b_q = getattr(obj_b, "q")
        b_r = getattr(obj_b, "r")
        b_s = getattr(obj_b, "s")
    else:
        a_q, a_r, a_s = obj_a
        b_q, b_r, b_s = obj_b
        
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
        An Object containing the attributes q, r and s, having numerical values.
        
    n : Integer
        An Integer limiting the distance 
        
    Raises:
    -------
    TypeError: If n is not numeric.
    AttributeError: If obj is missing q, r or s as an Attribute.
        
    Returns:
    --------
    hex_in_range(set): A set containing all cube coordinates within distance n from obj.
    """

    o_q = getattr(obj, "q")
    o_r = getattr(obj, "r")
    o_s = getattr(obj, "s")

    hex_in_range = set()
        
    for q in range(-n, n+1):
        for r in range(-n, n+1):
            for s in range(-n, n+1):
                if q + r + s == 0:
                    hex_in_range.add((o_q+q, o_r+r, o_s+s))
                
    return hex_in_range
    

def line_draw(obj_a:object, obj_b:object) -> tuple:
    """
    Draws a line from one hexagon to another, returns a tuple containing the 
    hexagons with the center closest to the line.
        
    Parameters:
    -----------
    obj_a : Object
        An Object containing the attributes q, r and s, having numerical values.
        
    obj_a : Object
        An Object containing the attributes q, r and s, having numerical values.
        
    Raises:
    -------
    AttributeError: If obj_a or obj_b is missing q, r or s as an Attribute.
        
    Returns:
    --------
    hex_line_coords(tuple): A tuple containing all cube cordinates from obj_a to obj_b inclusive.
    """
    ab_dist = distance(obj_a, obj_b)
        
    hex_line_lst = list()
        
    for i in range(0, ab_dist + 1):
        
        try:
            qrs_f = cube_linint(obj_a, obj_b, 1.0/ab_dist * i)
            
        except ZeroDivisionError:
            qrs_f = cube_linint(obj_a, obj_b, 0)
            
        item = round_hex(qrs_f)
        hex_line_lst.append(item)
    
    hex_line_coords = tuple(hex_line_lst)
        
    return hex_line_coords
    

def dist_lim_flood_fill(start_obj:object, n:int, obj_grp:(list, set), block_var:str=None) -> set:
    """
    All cube coordinates within n distance from an object, factoring in block_var 
    (variable if True blocks object traversability).
        
    Parameters:
    -----------
    start_obj : Object
        An Object containing the attributes q, r and s, having integer values.
        
    n : Integer
        The number of moves from start object to fill.
        
    obj_grp : List, Set or SpriteGroup
        A container containing objects adjacent to each other in a cube coordinate system (tiles in tilemap).
        
    block_var : String, optional
        Variable name of the variable, that objects in obj_grp should contain to
        block consideration as viable tile to traverse.
        
    Raises:
    -------
    AttributeError: If obj_a or obj_b is missing q, r or s as an Attribute.
        
    Returns:
    --------
    visited(set): A set containing all cube cordinates within distance n 
    from start_obj.
    """

    start = (start_obj.q, start_obj.r, start_obj.s)
        
    visited = set()
    visited.add(start)
    fringes = []
    fringes.append([start])
    
    if n > 0:
        for i in range(1,n+1):
            fringes.append([])
            for coords in fringes[i-1]:
                for j in range(0,6):
                    nbor_coords = neighbors(coords)[j]
                    # get corresponding object to nbor_coords from obj_grp -- #
                    nbor_obj = None
                    for obj in obj_grp:
                            if (obj.q, obj.r, obj.s) == nbor_coords:
                                nbor_obj = obj
                    blocked = getattr(nbor_obj, block_var, True)
                    if nbor_coords not in visited:
                        if not blocked:
                            visited.add(nbor_coords)
                            fringes[i].append(nbor_coords)
    
    return visited


def create_graph_matrix(tile_grp:(list, set)) -> pd.DataFrame:
    """
    Creates a pandas dataframe, containing a directed, weighted graph.
        
    Parameters:
    -----------
    tile_grp : List, Set or SpriteGroup
        A container containing objects adjacent to each other in a cube coordinate system (tiles in tilemap).
        
    Raises:
    -------
    AttributeError:
    TypeError:
        
    Returns:
    --------
    matrix_df(pd.DataFrame): Two-dimensional, directed, weighted graph.
    """
    # individual tile coords for column/index names --------------------- #
    idx = list()
    
    for tile in tile_grp:
        idx.append((tile.q, tile.r, tile.s))
    
    # creating a set with all connections ----------------------------------- #
    edges = set()
    
    for tile in tile_grp:
        tile_qrs = (tile.q, tile.r, tile.s)
        t_nbors_set = neighbors((tile_qrs[0], tile_qrs[1], tile_qrs[2]))
        for nbor in t_nbors_set:
            nbor_qrs = (nbor[0], nbor[1], nbor[2])
            for t in tile_grp:
                if t.q == nbor[0] and t.r == nbor[1] and t.s == nbor[2]:
                    if t.block_move is False and tile.block_move is False:
                        edges.add((tile_qrs, nbor_qrs, tile.movement_cost, t.movement_cost))

    map_matrix = np.identity(len(idx))
    
    matrix_df = pd.DataFrame(map_matrix, index=idx, columns=idx)
    
    for edge in edges:
        # movement_cost defined by the tile moved onto ---------------------- #
        # movement_cost if possible from edge[0] to edge[1] ----------------- #
        matrix_df.at[edge[0], edge[1]] = edge[3]
        # movement_cost if possible from edge[1] to edge[0] ----------------- #
        matrix_df.at[edge[1], edge[0]] = edge[2]
        
    
    matrix_df = matrix_df.astype("int64")
    
    return matrix_df   

# graph based path finding algorithms --------------------------------------- #
def breadth_first_search(start:tuple, goal:tuple, graph_matrix_df:pd.DataFrame) -> list:
    """
    Algorithm for searching a tree data structure for a node that satisfies a 
    given property. It starts at the tree root and explores all nodes at the 
    present depth prior to moving on to the nodes at the next depth level.
    
    Parameters:
    -----------
    
    Raises:
    -------
    
    Returns:
    --------
    """
    frontier = list()
    frontier.append(start)
    came_from = dict() # path A->B is stored as came_from[B] == A
    came_from[start] = None

    while frontier:
        current = frontier.pop(0)
        
        if current == goal:
            break
        else:
            for nbor in neighbors(current):
                if nbor not in came_from.keys():
                    # movement_cost from row to column not 0 ---------------- #
                    if nbor in graph_matrix_df.index.tolist():
                        if graph_matrix_df.at[nbor, current] != 0:
                            frontier.append(nbor)
                            came_from[nbor] = current
    
    # follow the path from goal to start in came_from ----------------------- #
    current = goal 
    path = list()
    while current != start: 
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    
    return path


def dijkstras_algorithm(start:tuple, goal:tuple, graph_matrix_df:pd.DataFrame) -> list:
    """
    Algorithm for searching a tree data structure for a node that satisfies a 
    given property. It starts at the tree root and explores the nodes based on 
    the cost of exploring each arm.
    
    Parameters:
    -----------
    
    Raises:
    -------
    
    Returns:
    --------
    """
    frontier = list()
    frontier.append((start, 0))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    
    # while not all tiles have been procesed, pop first tile from list ------ #
    while frontier:
        current = frontier.pop(0)
        
        # if current qrs_coords equal goal coords, break out of loop -------- #
        if current[0] == goal:
            break
        # else execute loop ------------------------------------------------- #
        else:
            for nbor in neighbors(current[0]):
                if nbor in graph_matrix_df.index.tolist():
                    if graph_matrix_df.at[nbor, current[0]] != 0:
                        new_cost = cost_so_far[current[0]] + graph_matrix_df.at[nbor, current[0]]
                        if nbor not in cost_so_far or new_cost < cost_so_far[nbor]:
                            cost_so_far[nbor] = new_cost
                            came_from[nbor] = current[0]
                            frontier.append((nbor, new_cost))
                            frontier.sort(key= lambda x:x[1] in frontier)
                    
    # follow the path from goal to start in came_from ----------------------- #
    current = goal 
    path = list()
    while current != start: 
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    
    return path
               

def a_star_algorithm(start:tuple, goal:tuple, graph_matrix_df:pd.DataFrame) -> list:
    """
    Modified version of Dijkstra’s Algorithm that is optimized for a single 
    destination. It prioritizes paths that seem to be leading closer to a goal.
    
    Parameters:
    -----------
    
    Raises:
    -------
    
    Returns:
    --------
    """
    frontier = list()
    frontier.append((start, 0))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    
    # while not all tiles have been procesed, pop first tile from list ------ #
    while frontier:
        current = frontier.pop(0)
        
        # if current qrs_coords equal goal coords, break out of loop -------- #
        if current[0] == goal:
            break
        # else execute loop ------------------------------------------------- #
        else:
            for nbor in neighbors(current[0]):
                if nbor in graph_matrix_df.index.tolist():
                    if graph_matrix_df.at[nbor, current[0]] != 0:
                        new_cost = cost_so_far[current[0]] + graph_matrix_df.at[nbor, current[0]]
                        if nbor not in cost_so_far or new_cost < cost_so_far[nbor]:
                            cost_so_far[nbor] = new_cost
                            came_from[nbor] = current[0]
                            priority = new_cost + distance(goal, nbor, is_obj=False)
                            frontier.append((nbor, priority))
                            frontier.sort(key= lambda x:x[1] in frontier)
                    
    # follow the path from goal to start in came_from ----------------------- #
    current = goal 
    path = list()
    while current != start: 
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    
    return path
        
# unittests ----------------------------------------------------------------- #
# TestLinint ---------------------------------------------------------------- #
class TestLinint(unittest.TestCase):
    
    def test_error(self):
        with self.assertRaises(TypeError):
            linint(1, "2", 0.5)
            linint("1", 2, 0.5)
            linint(1, 2, "0.5")
            
    def test_inout(self):
        self.assertEqual(linint(1, 2, 0.5), 1.5, "linint(1, 2, 0.5), 1.5, failed")

# TestCartesianLinint ------------------------------------------------------- #
class TestCartesianLinint(unittest.TestCase):
    
    def test_error(self):
        with self.assertRaises(ValueError):
            cartesian_linint("(-3,1)", (2,3), 0.5)
            cartesian_linint((-3,1), "(2,3)", 0.5)
            cartesian_linint((-3,1), (2,3), "0.5")
            cartesian_linint((-3,1,1), (2,3), 0.5)
            cartesian_linint((-3,1), (2,3,0), 0.5)
        with self.assertRaises(TypeError):
            cartesian_linint((-1), (2,3), 0.5)
            cartesian_linint((-3,1), (3), 0.5)
            cartesian_linint({"1":-3,"2":1}, (3), 0.5)
            cartesian_linint({"1":-3,"2":1}, (3), (0.5))
            
    def test_inout(self):
        self.assertEqual(cartesian_linint((-3,1), (2,3), 0.5), (-0.5, 2), "cartesian_linint((-3,1), (2,3), 0.5), (-0.5,2), failed")

# TestCubeLinint ------------------------------------------------------------ #
class TestCubeLinint(unittest.TestCase):
    
    def setUp(self):
        self.object_a = Mock()
        self.object_a.q = 1
        self.object_a.r = -2
        self.object_a.s = 1
        self.object_b = Mock()
        self.object_b.q = 3
        self.object_b.r = -2
        self.object_b.s = -1
        self.object_c = Mock()
        self.object_c.q = 3
        self.object_c.r = -2
        del self.object_c.s
        self.object_d = Mock()
        self.object_d.q = "3"
        self.object_d.r = -2
        self.object_d.s = -1
        
    def test_error(self):
        with self.assertRaises(TypeError):
            cube_linint(self.object_a, self.object_d, 0.5)
            cube_linint(self.object_a, self.object_b, "0.5")
        with self.assertRaises(AttributeError):
            cube_linint(self.object_a, self.object_c, 0.5)
            
    def test_inout(self):
        self.assertEqual(cube_linint(self.object_a, self.object_b, 0.5), (2, -2, 0), "cube_linint((0,-1,1), (0,1,-1), 0.5), (0,0,0), failed")
        
    def tearDown(self):
        self.object_a.dispose()
        self.object_b.dispose()
        self.object_c.dispose()
        self.object_d.dispose()

# TestRoundHex -------------------------------------------------------------- #
class TestRoundHex(unittest.TestCase):
    
    def test_error(self):
        with self.assertRaises(TypeError):
            round_hex((0,-1.1,"1.3"))
            round_hex((0,"-1.1",1.3))
            round_hex(("0",-1.1,1.3))
        with self.assertRaises(ValueError):
            round_hex(())
            round_hex((0,-1.1,1.3,4))
    
    def test_inout(self):
        self.assertEqual(round_hex((0,-1.1,1.3)), (0,-1,1), "round_hex((0,-1.1,1.3)), (0,-1,1), failed")

# TestGetqrs ---------------------------------------------------------------- #
class TestGetqrs(unittest.TestCase):
    
    def setUp(self):
        self.object_a = Mock()
        self.object_a.q = 1
        self.object_a.r = 1
        self.object_a.s = -2
        self.object_b = Mock()
        self.object_b.q = 1
        self.object_b.r = 1
        del self.object_b.s
        
    def test_error(self):
        with self.assertRaises(AttributeError):
            get_qrs(self.object_b)
    
    def test_inout(self):
        self.assertEqual(get_qrs(self.object_a), (1,1,-2), "get_qrs(object), (1,1,-2), failed")
        
    def tearDown(self):
        self.object_a.dispose()
        self.object_b.dispose()

# TestSetqrs ---------------------------------------------------------------- #
class TestSetqrs(unittest.TestCase):
    
    def setUp(self):
        self.object = Mock()
        del self.object.q
        del self.object.r
        del self.object.s
        
    def test_error(self):
        with self.assertRaises(TypeError):
            set_qrs(self.object, 1,"1",-2)
        
    def test_inout(self):
        set_qrs(self.object, 1,1,-2)
        has_q = hasattr(self.object, "q")
        has_r = hasattr(self.object, "r")
        has_s = hasattr(self.object, "s")
        self.assertTrue(has_q, ", failed")
        self.assertTrue(has_r, ", failed")
        self.assertTrue(has_s, ", failed")
        self.assertIs(self.object.q, 1, ", failed")
        self.assertIs(self.object.r, 1, ", failed")
        self.assertIs(self.object.s, -2, ", failed")
        
    def tearDown(self):
        self.object.dispose()

# TestHexToPixel ------------------------------------------------------------ #
class TestHexToPixel(unittest.TestCase):
    
    def test_error(self):
        with self.assertRaises(ValueError):
            hex_to_pixel((1,1))
            hex_to_pixel((1,"1",-2))
            hex_to_pixel([1,1,-2])
            hex_to_pixel((1,1,-2,3))
    
    def test_inout(self):
        self.assertEqual(hex_to_pixel((1,1,-2)), (48, 96), "hex_to_pixel((1,1,-2)), (48, 96), failed")

# TestPixelToHex ------------------------------------------------------------ #
class TestPixelToHex(unittest.TestCase):
    
    def test_error(self):
        with self.assertRaises(TypeError):
            pixel_to_hex([48, 96])
            pixel_to_hex((48, "96"))
    
    def test_inout(self):
        self.assertEqual(round_hex(pixel_to_hex((48, 96))), (1,1,-2), "pixel_to_hex((48, 96)), (1,1,-2), failed")

# TestNeighbors ------------------------------------------------------------- #
class TestNeighbors(unittest.TestCase):
    
    def test_error(self):
        with self.assertRaises(TypeError):
            neighbors((1,1,"-2"))
            neighbors([1,1,-2])
        with self.assertRaises(ValueError):
            neighbors((1,1,-2,2))
            neighbors((1,1))
    
    def test_inout(self):
        self.assertEqual(neighbors((1,1,-2)), ((2,1,-3), (2,0,-2), (1,0,-1), (0,1,-1), (0,2,-2), (1,2,-3)), "neighbors((1,1,-2)), ((2,1,-3), (2,0,-2), (1,0,-1), (0,1,-1), (0,2,-2), (1,2,-3)), failed")

# TestDistance -------------------------------------------------------------- #
class TestDistance(unittest.TestCase):
    
    def setUp(self):
        self.object_a = Mock()
        self.object_a.q = 1
        self.object_a.r = -2
        self.object_a.s = 1
        self.object_b = Mock()
        self.object_b.q = 3
        self.object_b.r = -2
        self.object_b.s = -1
        self.object_c = Mock()
        self.object_c.q = 3
        self.object_c.r = -2
        del self.object_c.s
        self.object_d = Mock()
        self.object_d.q = 3
        self.object_d.r = "-2"
        self.object_d.s = -1
        
    def test_error(self):
        with self.assertRaises(AttributeError):
            distance(self.object_a, self.object_c)
        with self.assertRaises(TypeError):
            distance(self.object_a, self.object_d)
    
    def test_inout(self):
        self.assertEqual(distance(self.object_a, self.object_b), 2, "distance(self.object_a, self.object_b), 2, failed")
        
    def tearDown(self):
        self.object_a.dispose()
        self.object_b.dispose()
        self.object_c.dispose()
        self.object_d.dispose()

# TestInRange --------------------------------------------------------------- #
class TestInRange(unittest.TestCase):
    
    def setUp(self):
        self.object_a = Mock()
        self.object_a.q = 1
        self.object_a.r = -1
        self.object_a.s = 0
        self.object_b = Mock()
        self.object_b.q = 3
        self.object_b.r = -2
        del self.object_b.s
        self.object_c = Mock()
        self.object_c.q = 3
        self.object_c.r = "-2"
        self.object_c.s = -1
        
    def test_error(self):
        with self.assertRaises(AttributeError):
            in_range(self.object_b, 1)
        with self.assertRaises(TypeError):
            in_range(self.object_c, 1)
        
    def test_inout(self):
        # test number of tiles in returned set ------------------------------ #
        self.assertEqual(len(in_range(self.object_a, 0)), 1, "len(in_range(object, 0)), 1, failed")
        self.assertEqual(len(in_range(self.object_a, 1)), 7, "len(in_range(object, 1)), 7, failed")
        self.assertEqual(len(in_range(self.object_a, 2)), 19, "len(in_range(object, 2)), 19, failed")
        self.assertEqual(len(in_range(self.object_a, 3)), 37, "len(in_range(object, 3)), 37, failed")
        self.assertEqual(len(in_range(self.object_a, 4)), 61, "len(in_range(object, 4)), 61, failed")
        # test returned coordinatess vs expected ---------------------------- #
        self.assertEqual(in_range(self.object_a, 1), {(1,-1,0), (1,0,-1), (0,0,0), (0,-1,1), (1,-2,1), (2,-2,0), (2,-1,-1)}, "in_range(self.object, 1), {(1,-1,0), (1,0,-1), (0,0,0), (0,-1,1), (1,-2,1), (2,-2,0), (2,-1,-1)}, failed")
        
    def tearDown(self):
        self.object_a.dispose()
        self.object_b.dispose()
        self.object_c.dispose()

# TestLineDraw -------------------------------------------------------------- #
class TestLineDraw(unittest.TestCase):
    
    def setUp(self):
        self.object_a = Mock()
        self.object_a.q = 1
        self.object_a.r = -2
        self.object_a.s = 1
        self.object_b = Mock()
        self.object_b.q = 3
        self.object_b.r = -2
        self.object_b.s = -1
        self.object_c = Mock()
        self.object_c.q = 3
        self.object_c.r = -2
        del self.object_c.s
        self.object_d = Mock()
        self.object_d.q = 3
        self.object_d.r = "-2"
        self.object_d.s = -1
        
    def test_error(self):
        with self.assertRaises(AttributeError):
            line_draw(self.object_a, self.object_c)
        with self.assertRaises(TypeError):
            line_draw(self.object_a, self.object_d)
        
    def test_inout(self):
        self.assertEqual(line_draw(self.object_a, self.object_b), ((1, -2, 1), (2, -2, 0), (3, -2, -1)), "line_draw(self.object_a, self.object_b), ((1, -2, 1), (2, -2, 0), (3, -2, -1)), failed")
        
    def tearDown(self):
        self.object_a.dispose()
        self.object_b.dispose()
        self.object_c.dispose()
        self.object_d.dispose()

# TestDistLimFloodFill ------------------------------------------------------ #
class TestDistLimFloodFill(unittest.TestCase):
    
    def setUp(self):
        # start_obj --------------------------------------------------------- #
        self.start_obj = Mock()
        self.start_obj.q = 0
        self.start_obj.r = 0
        self.start_obj.s = 0
        self.start_obj.block = False
        # err_objects ------------------------------------------------------- #
        self.err_object_a = Mock()
        self.err_object_a.q = 0
        self.err_object_a.r = "0"
        self.err_object_a.s = 0
        self.err_object_b = Mock()
        self.err_object_b.q = 0
        self.err_object_b.r = 0
        del self.err_object_b.s
        # obj_grp containing all objects with 2 dist from start ------------- #
        self.obj_grp = set()
        # coords of all objects with distance 2 from start_obj -------------- #
        all_coords = in_range(self.start_obj, 2)
        # coords of objects to be blocked ----------------------------------- #
        block_coords = {(1,-2,1), (1,-1,0), (1,0,-1), (0,2,-2), (-1,0,1)}
        # add objects to obj_grp -------------------------------------------- #
        for coords in all_coords:
            obj = Mock()
            obj.q = coords[0]
            obj.r = coords[1]
            obj.s = coords[2]
            if (obj.q, obj.r, obj.s) in block_coords:
                obj.block = True
            else:
                obj.block = False
            self.obj_grp.add(obj)
            
    def test_error(self):
        with self.assertRaises(AttributeError):
            dist_lim_flood_fill(self.err_object_b, 2, self.obj_grp, "block")
        with self.assertRaises(TypeError):
            dist_lim_flood_fill(self.err_object_a, 2, self.obj_grp, "block")
        
    def test_inout(self):
        self.assertEqual(dist_lim_flood_fill(self.start_obj, 2, self.obj_grp, "block"), {(0,-2,2),(-1,-1,2),(0,-1,1),(0,0,0),(-2,1,1),(-2,2,0),(-1,1,0),(-1,2,-1),(0,1,-1),(1,1,-2)}, "dist_lim_flood_fill(self.start_obj, 2, self.obj_grp, 'block'), {(0,-2,2),(-1,-1,2),(0,-1,1),(0,0,0),(-2,1,1),(-2,2,0),(-1,1,0),(-1,2,-1),(0,1,-1),(1,1,-2)}, failed")
    
    def tearDown(self):
        self.start_obj.dispose()
        self.err_object_a.dispose()
        self.err_object_b.dispose()
        for obj in self.obj_grp:
            obj.dispose()
        del self.obj_grp

# run unittests ------------------------------------------------------------- #
unittest.main()

