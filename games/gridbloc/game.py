#!/usr/bin/env python

'''
DEV STEPS OF THIS FILE:
1. how does this file relate to the building of arrays which are currently hardcoded into other example game.py files?
2. probably i should just add my custom gridbloc array calculation functions to existing game.py and use function call outs rather than hardcoded arrays.
3. CON: this might slow things down a bit as they will have to be re-calced, but they also might be so easy to calc that who cares
4. alt to 3: calc them ahed of time and then include the outputs as hardcoded, but include a game-setup.py style file for those interested, and for me (i m interested!)
5. determine exact role of Game.gameState Game.actionSpace, GameState.winners (especially this last one as winner is simple the greater of p1.runscore and p2.runscore (or whatever that exact equivalent might be)
6. currentBoard = state.board and currentAV = actionValues #investigate

MVP CLI phases
4. input ct and calcs GOOD moves not just legal moves for runner and blocker - thats a whole other thing

PARAMETERS 
 * "h" = height of grid (number of rows)
 * "w" =  width of a row in RUNNING tiles. 
'''


import sys, random, logging, math
import numpy as np
import gridbloc_utilities as gbutil


#################################
### add some gridbloc setup and calculation functions
#################################

class GridBlocBoard():
  gbutil.whereami(sys._getframe().f_code.co_name)
  
  def __init__(self,w,h):		
		''' desc here '''
		
		self.w = w
		print "GBB self.w = ", w
		
		self.h = h
		print "GBB self.h = ", h
		
		self.tile_max = (self.h * ( (3 * self.w) + 1) ) + self.w
		print "GBB self.tile_max = ", self.tile_max

		self.all_the_tiles = range(1, (self.tile_max+1))
		print "GBB self.all_the_tiles = ", self.all_the_tiles
				
		self.clicked_tiles_walls_list = [] # initially none, useful for MASTER recreation of gameplay
		print "START GBB self.clicked_tiles_walls_list = ", self.clicked_tiles_walls_list
		self.clicked_blocks = [] # initially none
		print "START GBB self.clicked_blocks = ", self.clicked_blocks
		self.clicked_runs = [] # initially none
		print "START GBB self.clicked_runs = ", self.clicked_runs
		
		
		self.vert_tile_distance = 3 * self.w + 1
		print "GBB self.vert_tile_distance = ",self.vert_tile_distance

		self.run_row_len = 2 * self.w + 1
		print "GBB self.run_row_len = ", self.run_row_len

		self.run_tiles_byrow_dict = self._run_tiles_dict_maker() # keyed by rownum
		print "GBB self.run_tiles_byrow_dict = ", self.run_tiles_byrow_dict
		
		self.run_tiles_list = self._run_tiles_list_maker()
		print "GBB self.run_tiles_list = ", self.run_tiles_list
		self.valid_runs = self.run_tiles_list[:] # initially COPY of all running tiles
		print "START GBB self.valid_runs = ", self.valid_runs
		self.unclicked_runs = self.run_tiles_list[:] # initially COPY of all running tiles
		print "START GBB self.unclicked_runs = ", self.unclicked_runs
		
		
		
		###### blocker tile params / value calcs
		self.b_row_h_len = self.w
		print "GBB self.b_row_h_len = ", self.b_row_h_len
		
		self.b_tiles_list = self._block_tiles_list_maker()
		print "GBB self.b_tiles_list = ", self.b_tiles_list
		self.unclicked_blocks = self.b_tiles_list[:] # initially COPY of all blocking tiles
		print "GBB self.unclicked_blocks = ", self.unclicked_blocks
		
		self.b_hortiles_dict = self._b_hortiles_dict_maker()
		self.b_vertiles_dict = self._b_vertiles_dict_maker()
		self.block_tiles_master_dict = self._block_tiles_dict_maker()
		print "GBB self.b_hortiles_dict = ", self.b_hortiles_dict
		print "GBB self.b_vertiles_dict = ", self.b_vertiles_dict
		print "GBB self.block_tiles_master_dict = ", self.block_tiles_master_dict
		
		self.b_row_h_nums = self.w +1
		print "GBB self.b_row_h_nums = ", self.b_row_h_nums
		
		self.b_row_v_nums = self.w +1
		print "GBB self.b_row_v_nums = ", self.b_row_v_nums
		
		self.b_row_v_left_first = self.b_row_h_len + 1
		print "GBB self.b_row_v_left_first = ", self.b_row_v_left_first
		
		self.b_row_v_left_last = self.b_row_v_left_first + ( (self.h - 1)  * self.vert_tile_distance)
		print "GBB self.b_row_v_left_last", self.b_row_v_left_last
		
		self.b_row_v_right_first = (3 * self.b_row_h_len) + 1
		print "GBB self.b_row_v_right_first = ", self.b_row_v_right_first
		
		self.b_row_v_right_last = self.b_row_v_right_first + ( (self.h - 1)  * self.vert_tile_distance)
		print "GBB self.b_row_v_right_last = ", self.b_row_v_right_last

		######## edges
		print "----------- generate edge values ------------------"
		self.edge_top_list = range(1, self.w+1)
		print "GBB edge_top_list", self.edge_top_list
		
		self.edge_bottom_list = list( reversed( range(self.tile_max,(self.tile_max - self.w),-1) ) )
		print "GBB edge_bottom_list", self.edge_bottom_list
		
		self.edge_left_list = range(self.b_row_v_left_first, self.b_row_v_left_last+1, self.vert_tile_distance)
		print "GBB edge_left_list", self.edge_left_list
		
		self.edge_right_list = range(self.b_row_v_right_first, self.b_row_v_right_last+1, self.vert_tile_distance)
		print "GBB edge_right_list", self.edge_right_list
		
		self.edge_walls_list = self._build_edges_list()
		print "GBB self.edge_walls_list = ", self.edge_walls_list
		
		## close edges
		close_all_edges = True # condition this to static or dyanmic config
		if close_all_edges == True: 
		  if self._close_edges() == True: self.edges_closed = True
		print "GBB self.edges_closed = ", self.edges_closed
		
		
		# runnerpower - determines self.valid_runs in calculate_valid_runs()
		# runnerpower - also cheetah, roo, bee, mouse, chicken, frog
		self.runnerpower = "duck" #default/beginner runnerpower
		### TODO -- this might not be calculated properly, looking at visualization...
		### ok it is, but clicked_runs.INDEX() shows too high num on printboard()
		self.runnerpoints = 0 # blocker gets no points, ya know.
		self.round_num = 1
		self.round_num_max = 2 
		self.run_style = "random"
		self.block_style = "random" # h=1 or v=2 tile type
		
		############### wrap up __init__



#################################
### non __init functions. # todo -- move to gbutil?
#################################		

#################################
  def _run_tiles_dict_maker(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    build the ORIGINAL MASTER array / list of running tiles, as dict keyed by row_num.
    there will also be 2 subsets: tiles_validnextmove and tiles_scored
    run_row_tilerange = range(run_row_leftedge, ( run_row_leftedge + (2w-2) ), 2) #step = 2
    '''
    
    run_tiles_byrow_dict = {}
    for row_num in range(1, self.h+1):
      #print "row_num:", str(row_num) 
      run_row_leftedge = self._run_row_left_edge(row_num)
      #print "run_row_leftedge", str(run_row_leftedge)
      #print
      #step by two in the range to SKIP OVER vertical blocker tiles
      a = run_row_leftedge + 1
      b = run_row_leftedge + self.run_row_len
      run_tiles_byrow_dict[row_num] = [ t for t in range(a, b ,2) ]
    return run_tiles_byrow_dict
      


#################################
  def _run_tiles_list_maker(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    ''' just convert the KEYED run tiles dict to a list for when thats easier'''

    # break out the values from run tiles
    run_tiles_list = []
    for k,vs in self.run_tiles_byrow_dict.items():
      for v in vs: 
        run_tiles_list.append(v)
    
    return run_tiles_list


#################################    
  def _run_row_left_edge(self, row_num):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    returns an integer of the left edge vertical tile of that row 
    run_row_leftedge = (nw) + ( (n-1) + (2* w +1) ) + 1 
    '''
    #print "ROW_NUM PASSSED:",str(row_num)

    run_row_leftedge = (row_num * self.w) + ( (row_num - 1) * ( (2 * self.w) + 1) ) + 1    
    return run_row_leftedge




#################################    
  def _run_row_right_edge(self, row_num):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    ''' return int of RIGHT most VERTICAL tile on a run_row '''
    #print "ROW_NUM PASSSED:",str(row_num)
    
    leftedge = self._run_row_left_edge(row_num)
    run_row_rightedge = leftedge + (2 * self.w)
    
    
    return run_row_rightedge


################################# 
  def _get_ct_block_coords(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    pick a starting block or in-game block as well. 
    will pick by input or by policy, but for now... random is default but other styles may be passable
    '''
    
    #print "self.block_style=", self.block_style
    print "IGNORED FOR NOW, DURING CHANGES FROM pickcoords to getcoords"
    #print "self.ct_block =", self.ct_block
    
    # TODO - work backwards from self.ct_block to coordinates
        
    if self.block_style == "random":
      ''' from self.block_tiles_master_dict: ranpick 1=hor 2=vert, then from rownums, then a tile '''
      b_tile_type = random.randint(1,2) # h=1 or v=2 tile type
      
      # from keys in dict[1|2]
      b_tile_row = random.choice( self.block_tiles_master_dict[b_tile_type].keys() ) 
      
      # from values in list
      b_tile_num = random.choice(self.block_tiles_master_dict[b_tile_type][b_tile_row]) 
      
      ct_block_coords = (b_tile_type, b_tile_row, b_tile_num)
      
    elif self.block_style == "close":
      ''' pick from dict based on separator block row UP or DOWN or adjacent '''
      pass
    
    else:
      ''' some other scheme '''
      pass
    
    return ct_block_coords
	  


#################################    
  def _block_tiles_list_maker(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    ''' build MASTER array / list of BLOCKING tiles from existing data. '''
    
    b_tiles_list = list( set(self.all_the_tiles) - set(self.run_tiles_list) )

    return b_tiles_list


#################################    
  def _b_hortiles_dict_maker(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    this is the dict for parts 2 and 3 of currenttile ("ct") tuple of type, row, tilenum
    calculate the horizontal blocker tiles, range with self.w, self.vert_tile_distance, "v"
    '''
    
    b_hortiles_dict = {}
    for row in range(1, self.h + 2):
      if row == 1: firsthor = 1
      else: firsthor = 1 + (self.vert_tile_distance * (row-1))
      
      #print "firsthor = ", firsthor
      b_hortiles_dict[row] = range( firsthor, firsthor+(self.w) )
    
    return b_hortiles_dict
    
    
#################################    
  def _b_vertiles_dict_maker(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    ''' THIS WAS CHANGED to allow for printboard(). needed verttils ACROSS not UP/DOWN
    this is the dict for parts 2 and 3 of currenttile ("ct") tuple of type, row, tilenum
    DEPRECATED --> calculate the horizontal blocker tiles, range with self.w, self.vert_tile_distance, "v"
    '''
    
    b_vertiles_dict = {}
    for row in range(1, self.h + 1):
      if row == 1: firstvert = self.w + 1
      else: firstvert = (self.w + 1) + (self.vert_tile_distance * (row-1))
      
      #print "firstvert = ", firstvert
      b_vertiles_dict[row] = range( firstvert, firstvert + self.run_row_len, 2)
    
    return b_vertiles_dict
    
        
#################################    
  def _block_tiles_dict_maker(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    ''' build block_tiles_master_dict, really just combine existing dicts with type key '''
    
    b_tiles_master_dict = {} # ct = currenttile = tuple of (type, rownum, tilenum)
    b_tiles_master_dict[1] = self.b_hortiles_dict # converted to int 1 for horizontals
    b_tiles_master_dict[2] = self.b_vertiles_dict # converted to int 2 for verticals
    
    return b_tiles_master_dict


#################################    
  def _build_edges_list(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
  
    ''' build edge wall list from the top bottom left right edge lists '''
  
    edge_walls_list = self.edge_top_list + self.edge_left_list + self.edge_right_list + self.edge_bottom_list
    #print "edge_walls_list", edge_walls_list
  
    return edge_walls_list


#################################    
  def _close_edges(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
  
    ''' use list of all for edges to target them for closure '''
  
    #print "self.edge_walls_list", self.edge_walls_list
  
    for edgewall in self.edge_walls_list:
      #print "edgewall", edgewall
    
      if gbutil.click_tile_or_wall(self, edgewall) == True: 
        edges_closed = True 
      else:
        edges_closed = False 
  
    return edges_closed


#################################
def play_a_game(w, h):
  gbutil.whereami(sys._getframe().f_code.co_name)
  ''' desc '''
  
  #setup a new game board
  print "ready a new GridBlocBoard(w,h)"
  gb_board = GridBlocBoard(w,h)
  print "\n###################  __init__ ONE DONE     #####\n"
  gb_board_r2 = GridBlocBoard(w,h)
  gb_board_r2.round_num = 2 # todo - potentially move to Gamestate or similar class
  print "\n###################  __init__ TWO DONE     #####\n"

  # start round one
  print "########################## START ROUND ONE"
  cycle = 0
  while gbutil.run_pick_click_process(gb_board) == True:
    cycle += 1
    print "\n############\nROUND 1 MID-CYCLE", cycle
    if gbutil.block_pick_click_process(gb_board) == False: 
      print "======= ERROR in round 1 ======="
      sys.exit(1)
    gbutil.show_summary(gb_board)
  print "ROUND ONE ENDED"
  

  # start round two
  print "########################## --START ROUND TWO"
  cycle = 0
  while gbutil.run_pick_click_process(gb_board_r2) == True:
    cycle += 1
    print "\n############\nROUND 2 MID-CYCLE", cycle
    if gbutil.block_pick_click_process(gb_board_r2) == False: 
      print "======= ERROR in round 1 ======="
      sys.exit(1)    
    gbutil.show_summary(gb_board_r2)
  
  # do the end game things
  gbutil.game_is_over(gb_board, gb_board_r2)
  
  return True



###################  END GridBlocBoard functions() #######################

    


################################
################################ original file for connect4

class Game:

	def __init__(self):		
		self.currentPlayer = 1
		self.gameState = GameState(np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.int), 1)
		self.actionSpace = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.int)
		self.pieces = {'1':'X', '0': '-', '-1':'O'}
		self.grid_shape = (6,7)
		self.input_shape = (2,6,7)
		self.name = 'connect4'
		self.state_size = len(self.gameState.binary)
		self.action_size = len(self.actionSpace)

	def reset(self):
		self.gameState = GameState(np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.int), 1)
		self.currentPlayer = 1
		return self.gameState

	def step(self, action):
		next_state, value, done = self.gameState.takeAction(action)
		self.gameState = next_state
		self.currentPlayer = -self.currentPlayer
		info = None
		return ((next_state, value, done, info))

	def identities(self, state, actionValues):
		identities = [(state,actionValues)]

		currentBoard = state.board
		currentAV = actionValues

		currentBoard = np.array([
			  currentBoard[6], currentBoard[5],currentBoard[4], currentBoard[3], currentBoard[2], currentBoard[1], currentBoard[0]
			, currentBoard[13], currentBoard[12],currentBoard[11], currentBoard[10], currentBoard[9], currentBoard[8], currentBoard[7]
			, currentBoard[20], currentBoard[19],currentBoard[18], currentBoard[17], currentBoard[16], currentBoard[15], currentBoard[14]
			, currentBoard[27], currentBoard[26],currentBoard[25], currentBoard[24], currentBoard[23], currentBoard[22], currentBoard[21]
			, currentBoard[34], currentBoard[33],currentBoard[32], currentBoard[31], currentBoard[30], currentBoard[29], currentBoard[28]
			, currentBoard[41], currentBoard[40],currentBoard[39], currentBoard[38], currentBoard[37], currentBoard[36], currentBoard[35]
			])

		currentAV = np.array([
			currentAV[6], currentAV[5],currentAV[4], currentAV[3], currentAV[2], currentAV[1], currentAV[0]
			, currentAV[13], currentAV[12],currentAV[11], currentAV[10], currentAV[9], currentAV[8], currentAV[7]
			, currentAV[20], currentAV[19],currentAV[18], currentAV[17], currentAV[16], currentAV[15], currentAV[14]
			, currentAV[27], currentAV[26],currentAV[25], currentAV[24], currentAV[23], currentAV[22], currentAV[21]
			, currentAV[34], currentAV[33],currentAV[32], currentAV[31], currentAV[30], currentAV[29], currentAV[28]
			, currentAV[41], currentAV[40],currentAV[39], currentAV[38], currentAV[37], currentAV[36], currentAV[35]
					])

		identities.append((GameState(currentBoard, state.playerTurn), currentAV))

		return identities


class GameState():
	def __init__(self, board, playerTurn):
		self.board = board
		self.pieces = {'1':'X', '0': '-', '-1':'O'}
		self.winners = [
			[0,1,2,3],
			[1,2,3,4],
			[2,3,4,5],
			[3,4,5,6],
			[7,8,9,10],
			[8,9,10,11],
			[9,10,11,12],
			[10,11,12,13],
			[14,15,16,17],
			[15,16,17,18],
			[16,17,18,19],
			[17,18,19,20],
			[21,22,23,24],
			[22,23,24,25],
			[23,24,25,26],
			[24,25,26,27],
			[28,29,30,31],
			[29,30,31,32],
			[30,31,32,33],
			[31,32,33,34],
			[35,36,37,38],
			[36,37,38,39],
			[37,38,39,40],
			[38,39,40,41],

			[0,7,14,21],
			[7,14,21,28],
			[14,21,28,35],
			[1,8,15,22],
			[8,15,22,29],
			[15,22,29,36],
			[2,9,16,23],
			[9,16,23,30],
			[16,23,30,37],
			[3,10,17,24],
			[10,17,24,31],
			[17,24,31,38],
			[4,11,18,25],
			[11,18,25,32],
			[18,25,32,39],
			[5,12,19,26],
			[12,19,26,33],
			[19,26,33,40],
			[6,13,20,27],
			[13,20,27,34],
			[20,27,34,41],

			[3,9,15,21],
			[4,10,16,22],
			[10,16,22,28],
			[5,11,17,23],
			[11,17,23,29],
			[17,23,29,35],
			[6,12,18,24],
			[12,18,24,30],
			[18,24,30,36],
			[13,19,25,31],
			[19,25,31,37],
			[20,26,32,38],

			[3,11,19,27],
			[2,10,18,26],
			[10,18,26,34],
			[1,9,17,25],
			[9,17,25,33],
			[17,25,33,41],
			[0,8,16,24],
			[8,16,24,32],
			[16,24,32,40],
			[7,15,23,31],
			[15,23,31,39],
			[14,22,30,38],
			]
		self.playerTurn = playerTurn
		self.binary = self._binary()
		self.id = self._convertStateToId()
		self.allowedActions = self._allowedActions()
		self.isEndGame = self._checkForEndGame()
		self.value = self._getValue()
		self.score = self._getScore()

	def _allowedActions(self):
		allowed = []
		for i in xrange(len(self.board)):
			if i >= len(self.board) - 7:
				if self.board[i]==0:
					allowed.append(i)
			else:
				if self.board[i] == 0 and self.board[i+7] != 0:
					allowed.append(i)

		return allowed

	def _binary(self):

		currentplayer_position = np.zeros(len(self.board), dtype=np.int)
		currentplayer_position[self.board==self.playerTurn] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-self.playerTurn] = 1

		position = np.append(currentplayer_position,other_position)

		return (position)

	def _convertStateToId(self):
		player1_position = np.zeros(len(self.board), dtype=np.int)
		player1_position[self.board==1] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-1] = 1

		position = np.append(player1_position,other_position)

		id = ''.join(map(str,position))

		return id

	def _checkForEndGame(self):
		if np.count_nonzero(self.board) == 42:
			return 1

		for x,y,z,a in self.winners:
			if (self.board[x] + self.board[y] + self.board[z] + self.board[a] == 4 * -self.playerTurn):
				return 1
		return 0


	def _getValue(self):
		# This is the value of the state for the current player
		# i.e. if the previous player played a winning move, you lose
		for x,y,z,a in self.winners:
			if (self.board[x] + self.board[y] + self.board[z] + self.board[a] == 4 * -self.playerTurn):
				return (-1, -1, 1)
		return (0, 0, 0)


	def _getScore(self):
		tmp = self.value
		return (tmp[1], tmp[2])




	def takeAction(self, action):
		newBoard = np.array(self.board)
		newBoard[action]=self.playerTurn
		
		newState = GameState(newBoard, -self.playerTurn)

		value = 0
		done = 0

		if newState.isEndGame:
			value = newState.value[0]
			done = 1

		return (newState, value, done) 




	def render(self, logger):
		for r in range(6):
			logger.info([self.pieces[str(x)] for x in self.board[7*r : (7*r + 7)]])
		logger.info('--------------')


#################################
#################################
def main(args):
  gbutil.whereami(sys._getframe().f_code.co_name)
  
  print "in main -- args=", args
  w = int(args[0])
  h = int(args[1])
  print "w = ", w, " h = ", h
  
  
  ######### play many games in loop for data/log aggregation
  
  for fame in range(1,2): #play a game or 20
    print "--------------------PLAY FOR FAME:", fame
    play_a_game(w, h) 
 
  # then end it all!
  sys.exit(1)
  


  
  #################################
# boilerplate kicker offer (yes thats a tech term!)   
if __name__ == '__main__':
  
  print "GRIDBLOC SETUP CLI VERSION"
  print
  args = sys.argv[1:]
  try:
    if len(args)==2:
      print "TRY args", args 
    else:
      print "need width AND height as parameters. setting to randoms 3 to 10"
      w = random.randint(3,11)
      h = random.randint(3,11)
      args = [w,h]
  except:
    print "something wrong in __name__ \ngoodbye"
    sys.exit(1)
  
  main(args)
  
  
  
  
  