
#!/usr/bin/env python
'''
PURPOSE
the goal here is to mathematically describe the DUAL + OVERLAPPING grids of gridbloc game, which required both running tiles and blocking tiles, so that arrays of valid choices can be calculated as needed. (the grid could, alternately, be said to have non-equal row-lengths (ie, diff num of columns), if you like.) the grid for running tiles is pretty classic, just cap all 4 edges (in an rectangular grid version) of each running tile with a tile to block and you see the dual/overlapping/interposed grid system of gridbloc.

unlike most other board games, there are TWO rounds, and the winner of the game is whomever has the most points after each player has run (so, 2 rounds in a 2 player game). runners earn points for each NEW tile they occupy during a game, and may return to already scored tiles as a matter of strategy, but wont get an extra point for that move. specifically, a tile can only be scored once per game, and blockers dont earn points, they just try to limit the points the runner earns by blocking them in.

IMPORTANT CONDITIONS
 * runner moves first, blocker moves next. that is one turn.
 * The end-round condition occurs when no un-scored tiles available for a runner to reach with a valid move.
 * at the end of a round, the players swap roles. new runner makes first move.
 * The end-game condition occurs at the end of round two.
 * The winner has the higher run score AFTER end of round two.


DEV STEPS OF THIS FILE:
1. how does this file relate to the building of arrays which are currently hardcoded into other example game.py files?
2. probably i should just add my custom gridbloc array calculation functions to existing game.py and use function call outs rather than hardcoded arrays.
3. CON: this might slow things down a bit as they will have to be re-calced, but they also might be so easy to calc that who cares
4. alt to 3: calc them ahed of time and then include theoutputs as hardcoded, but include a game-setup.py style file for thsose interested, and for me (i m interested!)
5. determine exact role of Game.gameState Game.actionSpace, GameState.winners (especially this last one as winner is simple the greater of p1.runscore and p2.runscore (or whatever that exact equivalent might be)
6. currentBoard = state.board and currentAV = actionValues #investigate
7. allow for a watch out for borders, so when row1 cannot goup, and edgeright, cannot go right, etc

MVP CLI phases
1. input w and h and it calcs gamestate and tile options arrays
2. input ct param and it calcs the legal moves arrays for runner and blocker
3. input ct and calcs GOOD moves not just legal moves for runner and blocker


PARAMETERS 
 * "h" = height of grid (number of rows)
 * "w" =  width of a row in RUNNING tiles. 

NOTE: blocking tiles (hor and vert, inclduing edge walls etc) will be calculated calculated from w & h 
 * "n" is the row number (n=3 is the 3rd row, etc)
 * "ct" is the NUMBER of the current_tile, which is NOT a A7 or F2 chess style notation, but a simple integer calculated from row width, according to the formulas which account for interposing blocking tiles.
 * the upper left RUNNING tile is NEITHER 1 nor 0 (zero). the upper left column top tile is actually 1, as a blocking tile ATOP each row uses numbers 1 to w. so then, w+1 is the left border wall for the first row, and the first running tile is w+2.


SOME FORMULAS
# NOTE: need to calculate "ct" when starting, from the available runner options. then track as runner moves, using the formulas.
# NOTE: "n" is calculated from ct and w, then track as runner moves, using the formulas.

 
 * close_edges() # function to identify all edge tiles to prevent edge-wrap/pacman movement. (for now!)
 
 * ct_run_available_all = []
 * ct_run_available_nextmove = []
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
		self.w = w
		print "GBB self.w = ", w
		
		self.h = h
		print "GBB self.h = ", h
		
		self.row_len = self._row_len_calc()
		print "GBB self.row_len = ", self.row_len
		
		self.run_tiles_master_dict = self._run_tiles_master() # keyed by rownum
		print "GBB self.run_tiles_master_dict = ", self.run_tiles_master_dict
		
		self.pickstyle = "random"
		self.ct_run = self._tilepick_run()
		print "GBB self.ct_run = ", self.ct_run
		
		self.row_num = self._row_num_from_ct() #formerly "n"
		print "GBB self.row_num = ", self.row_num
		
		self.run_row_leftedge = self._run_row_left_edge(self.row_num)
		print "GBB self.run_row_leftedge = ", self.run_row_leftedge
		
		## blocker tile params / value calcs
		self.b_row_h_len = self.w
		print "GBB self.b_row_h_len = ", self.b_row_h_len
		
		self.b_row_h_start = self._block_row_hor_starter()
		print "GBB self.b_row_h_start = ", self.b_row_h_start
		
		self.b_row_h_end = self._block_row_hor_ender()
		print "GBB self.b_row_h_end = ", self.b_row_h_end
		
		self.b_row_h_list = self._block_row_hor_list()
		print "GBB self.b_row_h_list = ", self.b_row_h_list
		
		self.b_row_v_start = self._block_row_vert_starter()
		print "GBB selfb_row_v_startrow_len = ", self.b_row_v_start
		
		self.b_row_v_end = self._block_row_vert_ender()
		print "GBB self.b_row_v_end = ", self.b_row_v_end
		
		self.b_row_v_list = self._block_row_vert_list()
		print "GBB self.b_row_v_list = ", self.b_row_v_list
		
		self.b_row_h_nums = self.w +1
		print "GBB self.b_row_h_nums = ", self.b_row_h_nums
		
		self.b_row_v_nums = self.w +1
		print "GBB self.b_row_v_nums = ", self.b_row_v_nums
		
		self.edge_walls_list = get_edges_list(self)
		print "GBB self.edge_walls_list = ", self.edge_walls_list
		
		close_edges = True #todo -- move this to config by input or static
		if close_edges == True: 
		  close_edges()

		
		
  # also called run_row_length()
  def _row_len_calc(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    for every tile, there is a left side, then one more right side at the end
    (or, of course you can think of this as rights with one left)
    '''
    
    row_len = 2 * self.w + 1
    return row_len


#################################
  def _run_tiles_master(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    build the ORIGINAL MASTER array / list of running tiles, as dict keyed by row_num.
    there will also be 2 subsets: tiles_validnextmove and tiles_scored
    run_row_tilerange = range(run_row_leftedge, ( run_row_leftedge + (2w-2) ), 2) #step = 2
    '''
    
    
    run_tiles_master_dict = {}
    for row_num in range(1, self.h+1):
      print "row_num:", str(row_num) 
      run_row_leftedge = self._run_row_left_edge(row_num)
      print "run_row_leftedge", str(run_row_leftedge)
      #step by two in the range to SKIP OVER vertical blocker tiles
      a = run_row_leftedge + 1
      b = run_row_leftedge + self.row_len
      run_tiles_master_dict[row_num] = [ t for t in range(a, b ,2) ]
    return run_tiles_master_dict
      

#################################    
  def _run_row_left_edge(self, row_num):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    returns an integer of the gridsquare number of the left edge tile of that row (which actually starts with the left-edge wall, so there is a + 1 to that)
    run_row_leftedge = (nw) + ( (n-1) + (2* w +1) ) + 1 ## should be run row LEFT EDGE
    '''
    print "ROW_NUM PASSSED:",str(row_num)
    
    
    run_row_leftedge = (row_num * self.w) + ( (row_num - 1) * ( (2 * self.w) + 1) ) + 1
    return run_row_leftedge
    
    
#################################  
  def _tilepick_run(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    '''
    placeholder to pick a tile -- starting tile and in-game as well. 
    will pick by input or by policy, but for now... random is default but other styles mat be passable
    '''
    # make more complete switch/case for other pick styles
    print "self.pickstyle=", self.pickstyle
    
    if self.pickstyle == "random":
      list_tilepick = random.choice(list(self.run_tiles_master_dict))
      print "list_tilepick", str(list_tilepick)
      tilepick = random.choice( list(self.run_tiles_master_dict[list_tilepick]) )
    else:
      list_tilepick = random.choice(list(self.run_tiles_master_dict))
      tilepick = random.choice( list(self.run_tiles_master_dict[list_tilepick]) )
          
    return tilepick
    

#################################        
  def _row_num_from_ct(self):
	gbutil.whereami(sys._getframe().f_code.co_name)
	
	row_num = math.floor(self.ct_run / self.row_len) # TODO--- this not right. run tile just look in masterdict?
	return row_num


#################################  
  def _tile_up_from_ct(self, this_tile = False):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    vert_tile = 3w+1 ## to current tile, add this value for below tile, and subtract for above tile.
    this_tile allows for NOT The current tile, but some arbitrary tile to be passed
    '''
    
    if this_tile == False:
      tile_up = self.ct_run - (3 * self.w + 1)
    else:
      tile_up = this_tile - (3 * self.w + 1)
    
    return tile_up


#################################
  def _tile_down_from_ct(self, this_tile = False):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    vert_tile = 3w+1 ## to current tile, add this value for below tile, and subtract for above tile.
    this_tile allows for NOT The current tile, but some arbitrary tile to be passed
    '''
    if this_tile == False:
      tile_dn = self.ct_run + (3 * self.w + 1)
    else:
      tile_dn = this_tile + (3 * self.w + 1)
    
    return tile_dn
    
#################################
  def _b_row_h_highest(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    _b_row_h_highest = b_row_h_start of last row + 3w
    '''
    last_row_h_starter = _block_row_hor_starter( self.h + 1 )
    _b_row_h_highest = last_row_h_starter + (3 * self.w)
    return _b_row_h_highest




#################################    
  def _block_row_hor_starter(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    _block_row_hor_starter = ((n-1)(2w+1)) + ((n-1)(w)) + 1
    n = self.row_num
    '''
    print "_block_row_hor_STARTER self.row_num= ", self.row_num
    b_row_h_start = ( (self.row_num-1)*(2 * self.w + 1) ) + ( (self.row_num-1)*(self.w) ) + 1
    return b_row_h_start




#################################    
  def _block_row_hor_ender(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    _block_row_hor_ender = b_row_h_start + b_row_h_len -1
    '''
    print "_block_row_hor_ENDER self.row_num= ", self.row_num
    b_row_h_end = self.b_row_h_start + self.b_row_h_len -1
    return b_row_h_end
    
  
#################################    
  def _block_row_hor_list(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    _block_row_hor_list = range(self.b_row_h_start, (self.b_row_h_len - 1 )
    '''
    print "self.b_row_h_start,", int(self.b_row_h_start)
    print "self.b_row_h_len", self.b_row_h_len
    b_row_h_list = range( int(self.b_row_h_start), int(self.b_row_h_start) + self.b_row_h_len )
    return b_row_h_list


#################################    
  def _block_row_vert_starter(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    _block_row_vert_starter = run_row_leftedge -1
    '''
    b_row_v_start = (self.run_row_leftedge - 1)
    return b_row_v_start
     

#################################    
  def _block_row_vert_ender(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    _block_row_vert_ender = block_row_vert_starter + 2w
    '''
    b_row_v_end = self.b_row_v_start + (2 * self.w)
    return b_row_v_end


#################################    
  def _block_row_vert_list(self):
    gbutil.whereami(sys._getframe().f_code.co_name)
    
    '''
    _block_row_vert_list = range(block_row_vert_starter, block_row_vert_ender, 2) #w/step = 2
    '''
    b_row_v_list = range(int(self.b_row_v_start), int(self.b_row_v_end), 2) 
    return b_row_v_list


#################################    
def get_edges_list(self):
  gbutil.whereami(sys._getframe().f_code.co_name)
  
  '''
  this function pre-selects the edge tiles (blocker tiles) to close the map 
  and prevent edge-wrap / pacman style moves (altho these may come in later)
  steps: 1. HOR edges, top and bottom 2. vert edges, left and right
  useful params: w, h, row_num,b_row h and v starts and ends 
  '''
  edge_top = range(self.w, self.w)
  edge_bottom_last = _b_row_h_highest(self)
  edge_bottom = list( reversed( range(edge_bottom_last,(edge_bottom_last - self.w),-1) ) )
  b_row_v_first = self.w + 1
  b_row_v_last = b_row_v_first + (2 * self.w)
  edge_left = [_tile_down_from_ct(self, b_row_v_first) for v in self.b_row_v_nums  ]
  edge_right = [_tile_down_from_ct(self, b_row_v_last) for v in self.b_row_v_nums  ] 

  edge_walls = edge_top + edge_bottom + edge_left + edge_right
  
  return edge_walls_list


#################################    
def click_tile_or_wall(thistile):
  gbutil.whereami(sys._getframe().f_code.co_name)
  
  '''
  do the things that click a tile or wall, like check for validity, probably, then add to the right array / list / dict
  '''
  pass





#################################    
def close_edges(self):
  gbutil.whereami(sys._getframe().f_code.co_name)
  
  '''
  use list of all for edges to target them for closure
  '''
  
  # hmm, some function click each edge_wall in list
  for edge in edge_walls_list:
    click_tile_or_wall(edge)
	







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



def main(args):
  gbutil.whereami(sys._getframe().f_code.co_name)
  
  print "in main -- args=", args
  w = int(args[0])
  h = int(args[1])
  print "w = ", w, " h = ", h
  
  #setup a new game board
  print "ready from new GridBlocBoard(w,h)"
  gb_board = GridBlocBoard(w,h)
  
  
  


  
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
      print "need width AND height as parameters. setting to defaults (5)"
      args = [5,5]
  except:
    print "something wrong in __name__ \ngoodbye"
    sys.exit(1)
  
  main(args)
  
  
  
  
  