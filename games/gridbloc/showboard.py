#!/usr/bin/env python
''' 
GRIDBLOC function to visualize the board, first as ascii, maybe later to web/js/html output.
'''
from __future__ import print_function
import sys
import gridbloc_utilities as gbu


#################################
### add some gridbloc visualization functions
#################################


class ShowBoard():
  #gbu.whereami(sys._getframe().f_code.co_name)
  
  def __init__(self, board):		
		''' do the things to visualize runs and blocks, with nums and ... v ----?
		 ----- ----- ----- -----
		|     |     |     |  1  |     
		 ----- -----...... -----
		|  10 |  9  |  2  |  8  |     
		 -----...... -----......
		|     |  6  |  7  |  3  |     
		 ----- ----- ----- -----
		|     |  5  |  4  |     |     
		 ----- ----- ----- -----
		'''
		
		board.hor_open = "......"
		board.hor_closed = " -----"
		board.ver_open = ":"
		board.ver_closed = "|"
		board.defpad = "     " # 5 spaces
		board.repeat1 = "."
		board.repeat2 = ":"
		board.repeat3 = "*"
		board.repeat4 = "+"
		
		
		# go print to screen
		#printboard_unplayed(board)
		
		# version two -- played data an calc'ed differently
		printboard(board)

		
############# end __init__

#################################
def printboard_unplayed(board):
	gbu.whereami(sys._getframe().f_code.co_name)
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
	      print(board.ver_open+board.ver_padd, end="")	
	  print()
	  #horizontals
	  for d in range(board.w):
	    if b == board.h-1:
	      print(board.hor_closed, end="")
	    else:
	      print(board.hor_open+board.ver_padd, end="")	      
	  print()


#################################
def printboard(board):
  gbu.whereami(sys._getframe().f_code.co_name)
  ''' print gridbloc game board, showing un|clicked tiles & walls'''
  
  #print( "board.clicked_runs", board.clicked_runs)
  print( "board.clicked_blocks", board.clicked_blocks)
  #print( "board.block_tiles_master_dict", board.block_tiles_master_dict)
  print( "PLAYED BOARD - in color! - d2" )
  print()
  # (2 * board.h + 2) == the number of rows in a gameboard, including top & bottom edges
  for r in range(1, (2 * board.h + 2)):
    if r % 2 == 0: 
      v_row(board, r) # evens
    else: 
      h_row(board, r)  # odds

  print()
  return
	
	

#################################
def h_row(board, r):
  gbu.whereami(sys._getframe().f_code.co_name)
  ''' build a row of horizontal blockers (like the top or bottom edge '''
  
  #find index in range of odd numbers, use as b_hortiles_dict index
  rownum = range(1, 2 * board.h + 3,2 ).index(r) + 1
  hor_row = board.b_hortiles_dict[rownum]
  for hwall in range(board.w):
    if hor_row[hwall] in board.clicked_blocks:
      # if latest block, make color, else leave as white
      latest = len(board.clicked_blocks)-1
      if board.clicked_blocks.index(hor_row[hwall])== latest :
        print(gbu.color.green + board.hor_closed + gbu.color.white,end="")
      else:
        print(board.hor_closed,end="")
    else:
      print(board.hor_open,end="")

  print()
  return	
	

#################################
def v_row(board, r):
  gbu.whereami(sys._getframe().f_code.co_name)
  ''' build a row of vertical blockers, AND the un|clicked cell space to its right.'''
  
  #find index in range of even numbers, use as b_vertiles_dict index
  rownum = range(0, 2 * board.h + 3, 2).index(r)
  ver_row = board.b_vertiles_dict[rownum]
  for vwall in range(board.w+1):
    thistile = ver_row[vwall]+1 #get tilenum
    leftpadb,ritepadb = setpadding(thistile)
    tileclicked = False
    
    #check if clicked run next to this vertical wall
    if thistile in board.clicked_runs:
      tileclicked = True
      lastclick = board.clicked_runs[-1] #this is a tilenum
      repeater = thisrun_repeat(board, thistile) # indicate if repeat run to this tile
      thisrun = board.clicked_points.index(thistile) + 1 # get running step number
      thisrun = str(thisrun)+repeater
      leftpad,ritepad = setpadding(thisrun)# adjust for digit count to keep cols in line      
    
    ## CLICKED WALL
    if ver_row[vwall] in board.clicked_blocks:
      latest = len(board.clicked_blocks)-1
      ## CLICKED TILE / RUN ADJACENT
      if tileclicked == True:
        if board.clicked_blocks.index(ver_row[vwall])== latest :
          ## MOST RECENT BLOCK WALL
          if thistile == lastclick:
            ## MOST RECENT RUN TO TILE
            print( gbu.color.green + board.ver_closed + gbu.color.white + leftpad + gbu.color.green + str(thisrun) + gbu.color.white + ritepad, end="")
          else:
            print( gbu.color.green + board.ver_closed + gbu.color.white + leftpad + str(thisrun) + ritepad, end="")
        else:
          if thistile == lastclick:
            ## MOST RECENT RUN TO TILE
            print( board.ver_closed + leftpad + gbu.color.green + str(thisrun) + gbu.color.white + ritepad, end="")
          else:
            print( board.ver_closed + leftpad + str(thisrun)+ ritepad, end="")
     
      ## UNCLICKED TILE    
      else:
        if thistile in board.run_tiles_list:
         if board.clicked_blocks.index(ver_row[vwall])== latest :
           print( gbu.color.green + board.ver_closed + gbu.color.white + leftpadb + gbu.color.gray + str(thistile)+ gbu.color.white + ritepadb, end="")
         else:
           print( board.ver_closed + leftpadb + gbu.color.gray + str(thistile)+ gbu.color.white + ritepadb, end="")
        else:
          print(board.ver_closed + board.defpad,end="")         

    ## UNCLICKED WALL      
    else:
      if tileclicked == True:
        if thistile == lastclick:
          ## MOST RECENT RUN
          print( board.ver_open + leftpad + gbu.color.green + str(thisrun) + gbu.color.white + ritepad, end="")
        else:
          print( board.ver_open + leftpad + str(thisrun) + ritepad, end="")
      
      else:
        if thistile in board.run_tiles_list:
          print( board.ver_open + leftpadb + gbu.color.gray + str(thistile)+ gbu.color.white + ritepadb, end="")
        else:
          print(board.ver_open + board.defpad,end="")
  
  print()
  return	


#################################
def setpadding(thisrun):
  gbu.whereami(sys._getframe().f_code.co_name)
  ''' adjust some spacing when step numbers present to keep COLs in line '''

  if len(str(thisrun)) == 1 : 
    leftpad = "  "
    ritepad = "  "
  if len(str(thisrun)) == 2 : 
    leftpad = "  "
    ritepad = " "
  if len(str(thisrun)) > 2 : 
    leftpad = " "
    ritepad = " "
  
  return (leftpad,ritepad)


#################################
def thisrun_repeat(board, thistile):
  gbu.whereami(sys._getframe().f_code.co_name)
  ''' add a "." to run num to show when back to tile. legal but gets no new point '''
  
  if board.clicked_runs.count(thistile) == 2: return board.repeat1
  elif board.clicked_runs.count(thistile) == 3: return board.repeat2
  elif board.clicked_runs.count(thistile) == 4: return board.repeat3
  elif board.clicked_runs.count(thistile) > 4: return board.repeat4  
  else: return ""

  
  
  
  

  

