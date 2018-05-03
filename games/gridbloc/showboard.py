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
		'''
		 .... ---- .... .... .... .... 
		|    :    :    :    : 99 |    :
		...........----................
		|    :    :    : 100|    |    :
		 .... .... .... .... .... .... 
		
		
		'''
		
		print "SHOW GAME BOARD"
		print "board.w = ", board.w
		print "board.h = ", board.h
		board.hor_open = "....."
		board.hor_closed = ".----"
		board.ver_open = ":    "
		board.ver_closed = "|    "
		
		printboard(board)

		
#############








def printboard(board):
	gbutil.whereami(sys._getframe().f_code.co_name)
	''' desc '''
	print "start board\n"
	print board.hor_open+board.hor_open+board.hor_open
	print board.ver_open+board.ver_open+board.ver_open+board.ver_closed

	print board.hor_closed+board.hor_open+board.hor_open
	print board.ver_open+board.ver_open+board.ver_open+board.ver_closed	

	print board.hor_open+board.hor_open+board.hor_open
	print board.ver_closed+board.ver_open+board.ver_closed+board.ver_closed
	
	print board.hor_open+board.hor_open+board.hor_open
	
	print
	print

	
	
	
	
	
	
			

