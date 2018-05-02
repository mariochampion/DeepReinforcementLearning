#!/usr/bin/env python
''' 
GRIDBLOC function to visualize the board, first as ascii, maybe later to web/js/html output.
'''


class ShowBoard():
  #gbutil.whereami(sys._getframe().f_code.co_name)
  
  def __init__(self, board):		
		''' do the things to visualize runs and blocks, with nums and ... bolds? '''
		
		print "SHOW GAME BOARD"
		print "board.w = ", board.w
		print "board.h = ", board.h	  
		
		

