import numpy as np


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
  return list of tiles in one long array as well as arrays for tiles, walls
  '''
  
  tiles_all = [1,2,3,4,5,6,7,8,9]
  



def get_tiles_valid(current_tile):
  '''
  return a LIST of valid tiles, NOT SORTED BY BEST. just legal tiles.
  another func will sort them by best. 
  '''
  
  tiles_valid = [1,2,3]
  
  return tiles_valid
  
  
def get_blocks_valid():
  '''
  returns LIST of valid blocks, NOT SORTED BY BEST blocks
  another func will sort them by best.
  (will this not be ALL walls/blocks MINUS already walls?)
  i guess then: call the get_blocks_blocked
  '''  