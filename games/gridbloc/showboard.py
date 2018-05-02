#!/usr/bin/env python
''' 
GRIDBLOC function to visualize the board, first as ascii, maybe later to web/js/html output.
'''

import sys
import gridbloc_utilities as gbutil


#################################
### add some gridbloc visualization functions
#################################


class ShowBoard():
  #gbutil.whereami(sys._getframe().f_code.co_name)
  
  def __init__(self, board):		
		''' do the things to visualize runs and blocks, with nums and ... bolds? '''
		
		print "SHOW GAME BOARD"
		print "board.w = ", board.w
		print "board.h = ", board.h
		board.cell_top = " ---- "
		board.cell_verts = "| 22 |"
		board.cell_bttm = " ____"
		
		printboard(board)

		
#############





def printboard(board):
	gbutil.whereami(sys._getframe().f_code.co_name)
	''' desc '''
	print "start board\n"
	print board.cell_top
	print board.cell_verts
	print board.cell_bttm
	
	
	
	
	
	
			

