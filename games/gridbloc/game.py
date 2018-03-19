'''
PURPOSE
the goal here is to mathematically describe the DUAL + OVERLAPPING (or non-even row-count, if you like) grids of gridbloc game, which required both running tiles and blocking tiles, so that arrays of valid choices can be calculated as needed. 

unlike most other board games, there are TWO rounds, and the winner of any one round is ALWAYS the runner, the winner of the game is whomever has the most running points after each player has run (so, 2 rounds in a 2 player game). runners earn points for each NEW tile they occupy during a game, and may return to already scored tiles as a matter of strategy, but wont get an extra point for that move. specifically, a tile can only be scored once per game.

 * The end-round condition is no un-scored tiles available for a runner to reach with a valid move.
 * The end-game condition is the end of round two.
 * The winning condition is the higher run score AFTER end of round two.
 * "w" as a parameter below stands for the Width of a row or RUNNING tiles. NOTE: the blocking tiles are calculated from "w"
 * the upper left RUNNING tile is NEITHER 1 nor 0 (zero). the upper left column top tile is actually 1. a blocking tile ATOP each row uses numbers 1 to w. so then, w+1 is the left border wall for the first row, and the first running tile is w+2.
 * "current_tile" as a parameter below is the NUMBER of the tile, which is NOT a A7 or F2 chess style notation, but a simple integer calculated from row width, according to the formulas which account for interposing blocking tiles.
'''
import numpy as np


### util funcs to move at some point  
### ---------------------------------------

def row_running_len(w):
  '''
  for every tile, there is a left side, then one more right side at the end
  (and of course you can think of this as rights with one left)
  '''
  lenrow = 2 * w + 1
  return lenrow
  
  
def row_blocking_len(w):
  '''
  a row of top or bottom edges, (between runnable tiles) is simply as long as w
  '''
  return w
  

def tile_up(w, current_tile):
  '''
  a running or blocking tile is 3*w+1 from the current_tile
  '''  
  uptile = current_tile - (3*w) + 1
  return uptile
  
def tile_down(w, current_tile):
  '''
  a running or blocking tile is 3*w+1 from the current_tile
  '''  
  downtile = current_tile + (3*w) + 1
  return downtile  

### ---------------------------------------




def build_gameboard(w,h):
  '''
  do a series of functions:
  1. build mastergrid
  2. build wall masterlist
    (sublists: edges, used, nextmoveoptions, best)
  3. build tile masterlist
    (sublists: rowcaps, used, nextmoveoptions, best)
  '''
def build_mastergrid(w,h):
  '''
  w = width
  h = height
  formula involves adding walls and edges, so not just w * h
  return list of tiles in one long array as well as arrays for tiles, walls
  '''
  
  
  return mastergrid
  
  
  
  


def tiles_valid(current_tile):
  '''
  return a LIST of valid tiles, NOT SORTED BY BEST. just legal tiles.
  another func will sort them by best. 
  '''
  
  tiles_valid = [1,2,3]
  
  return tiles_valid
  


  
def blocks_valid():
  '''
  returns LIST of valid blocks, NOT SORTED BY BEST blocks
  another func will sort them by best.
  (will this not be ALL walls/blocks MINUS already walls?)
  i guess then: call the get_blocks_blocked
  '''  
  
  blocks_valid = [1,2,3,4,5,6]
  return blocks_valid
  
  
  