#!/usr/bin/env python
''' 
GRIDBLOC function to visualize the board, first as ascii, maybe later to web/js/html output.
'''
from __future__ import print_function
import sys
import gridbloc_utilities as gbutil


#################################
### add some gridbloc visualization functions
#################################


class ShowBoard():
  #gbutil.whereami(sys._getframe().f_code.co_name)
  
  def __init__(self, board):		
		''' do the things to visualize runs and blocks, with nums and ... bolds? '''
		'''
		 .... ---- .... .... .... .... 
		|    :    :    :    : 99 |    :
		...........----................
		|    :    :    : 100|    |    :
		 .... .... .... .... .... .... 

		  ---- ---- ----
     |    :    :    |    
     ...............
     |    :    :    |    
     ...............
     |    :    :    |    
      ---- ---- ----
		
		'''
		
		print( "SHOW GAME BOARD" )
		print( "board.w = ", board.w )
		print( "board.h = ", board.h )
		board.hor_open = "....."
		board.hor_closed = " ----"
		board.ver_open = ":    "
		board.ver_closed = "|    "
		board.cell_spaces = 4

		# go print to screen
		printboard_unplayed(board)
		
		# version two -- played data an calc'ed differently
		printboard(board)

		
#############


def printboard_unplayed(board):
	gbutil.whereami(sys._getframe().f_code.co_name)
	''' desc '''

	print( "unplayed board "+ str(board.w) + " by " + str(board.h) )
	#top edge
	for a in range(board.w):
	  print(board.hor_closed, end="")
	print()
	#inner loop
	for b in range(board.h):
	  #verts
	  for c in range(board.w+1):
	    if c == 0 or c == board.w:
	      print(board.ver_closed, end="")
	    else:
	      print(board.ver_open, end="")	
	  print()
	  #horizontals
	  for d in range(board.w):
	    if b == board.h-1:
	      print(board.hor_closed, end="")
	    else:
	      print(board.hor_open, end="")	      
	  
	  
	  print()


#################################
def printboard(board):
  gbutil.whereami(sys._getframe().f_code.co_name)
  ''' desc '''
  
  ## TODO
	# print the tilenums rather than the symbols
	# then replace num, if in board.clicked_runs or board.clicked_blocks with symbol
	# replace with index of board.clicked_runs, to recreate steps
	
  print( "board.clicked_runs", board.clicked_runs)
  print( "board.clicked_blocks", board.clicked_blocks)
  print( "board.block_tiles_master_dict", board.block_tiles_master_dict)
  print( "PLAYED BOARD - draft 1" )
  print()
  for r in range(1, (2 * board.h + 2)):
    if r % 2 == 0: 
      v_row(board, r) # evens
    else: 
      h_row(board, r)  # odds


  print()
	
	

#################################
def h_row(board, r):
  gbutil.whereami(sys._getframe().f_code.co_name)
  ''' desc '''
  
  print("(printboard num) hor r = ", r)
  rownum = range(1, 2 * board.h + 3,2 ).index(r) + 1
  print("rownum = ", rownum)
  print("self.b_hortiles_dict ", board.b_hortiles_dict)
  print( "board.b_hortiles_dict[rownum] tiles IN clicked?", board.b_hortiles_dict[rownum]) 
  print()
  return	
	

#################################
def v_row(board, r):
  gbutil.whereami(sys._getframe().f_code.co_name)
  ''' desc '''
  
  print("(printboard num) ver r = ", r)
  rownum = range(0, 2 * board.h + 3, 2).index(r)
  print("rownum = ", rownum)
  print("self.b_vertiles_dict ", board.b_vertiles_dict) 
  print()
  return	








