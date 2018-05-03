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
		printboard(board)

		
#############








def printboard(board):
	gbutil.whereami(sys._getframe().f_code.co_name)
	''' desc '''
	print( "sample board\n" )
	print( board.hor_open+board.hor_open+board.hor_open )
	print( board.ver_open+board.ver_open+board.ver_open+board.ver_closed )

	print( board.hor_closed+board.hor_open+board.hor_open )
	print( board.ver_open+board.ver_open+board.ver_open+board.ver_closed )

	print( board.hor_open+board.hor_open+board.hor_open )
	print( board.ver_closed+board.ver_open+board.ver_closed+board.ver_closed )
	
	print( board.hor_closed+board.hor_closed+board.hor_closed )
	
	print( )
	print( )
	print( "unmarked board "+ str(board.w) + " by " + str(board.h) )
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



