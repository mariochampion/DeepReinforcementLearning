#!/usr/bin/env python
''' 
GRIDBLOC support functions.
'''


## GLOBAL implorts/vars (mostly for use in this file?)
import sys, random, math
from showboard import ShowBoard

## some global configs
show_whereami = False # a debug print line to track function flow
close_all_edges = True # true prevents pacman wraparound. keep True until much more development


##################################	
## just a debug placefinder to help trace actions
def whereami(funcname):
  if show_whereami == True:
    print
    print "-------------", funcname, " ------------------" 
    print
    

#################################  
def show_summary(self):
  print "\n-------- summary ----------\n"
  print "self.round_num", self.round_num
  print "END GBB self.runnerpoints =",self.runnerpoints
  print "END GBB self.ct_run = ", self.ct_run
  #print "END GBB self.clicked_tiles_walls_list = ", self.clicked_tiles_walls_list
  print "END GBB self.clicked_runs = ", self.clicked_runs
  print "END GBB self.clicked_points = ", self.clicked_points
  print "END GBB self.valid_runs = ", self.valid_runs
  print "END GBB self.lr_vr = ", self.lr_vr  
  print "END GBB self.lr_vp = ", self.lr_vp
  #print "END GBB self.unclicked_runs =", self.unclicked_runs
  #print
  #print "END GBB self.ct_block = ", self.ct_block
  #print "END GBB self.clicked_blocks = ", self.clicked_blocks
  #print "END GBB self.unclicked_blocks =", self.unclicked_blocks
  ShowBoard(self)
  print "-------- end summary ----------\n\n"     
  
  
#################################    
def block_row_hor_list(self, this_b_row):
  whereami(sys._getframe().f_code.co_name)
  
  ''' create list of horizontal blocker tiles on THIS B ROW '''
  
  if this_b_row == False: return False # nothing to do
  if self.b_tile_type == 2: return False
  
  if self.b_tile_type == 1:
    #print "tiletype HORIZONTAL = ", this_b_row
    b_row_h_list = self.b_hortiles_dict[this_b_row]
        
  #print "this_b_row", this_b_row, "for b_row_h_list", b_row_h_list

  return b_row_h_list  



#################################    
def block_row_vert_list(self, this_b_col):
  whereami(sys._getframe().f_code.co_name)
  
  ''' create list of VERTICAL blocker tiles in this run row '''
    
  if this_b_col == False: return False # nothing to do
  if self.b_tile_type == 1: return False # mistaken call -- do nothing
    
  if self.b_tile_type == 2: 
    #print "tiletype VERTICAL col =", this_b_col
    b_row_v_list = self.b_vertiles_dict[this_b_col]  
  
  #print "end: this_b_col",this_b_col,"has b_row_v_list", b_row_v_list
  
  return b_row_v_list

#################################  
def vert_tile(self, direction, this_tile = False,):
  whereami(sys._getframe().f_code.co_name)
  '''
  vert_tile = 3w+1 ## to current tile, add this value for below tile, and subtract for above tile.
  this_tile allows for NOT just the current tile, but some arbitrary tile to be passed
  '''
  
  if direction == "up":
    vert_tile = this_tile - self.vert_tile_distance
  if direction == "dn":
    vert_tile = this_tile + self.vert_tile_distance
      
  return vert_tile
  
  
#################################    
def run_row_starter(self, row_num):
  whereami(sys._getframe().f_code.co_name)
  ''' just add one to _run_row_left_edge(self, row_num)'''
    
  run_row_starter = self._run_row_left_edge(row_num) + 1
  #print "run_row_starter", run_row_starter
  return run_row_starter
   
    
#################################    
def run_row_from_tilenum(self, runtile):
  whereami(sys._getframe().f_code.co_name)
  ''' look thru self.run_tiles_byrow_dict for tile's runrow'''

  #print "self.run_tiles_byrow_dict", self.run_tiles_byrow_dict
  #print "runtile", runtile
  for row, tiles in self.run_tiles_byrow_dict.items():
    #print "row", row
    for tile in tiles:
      #print "tile:", tile
      if runtile == tile:
        #print "returning this run row! ", row 
        return row
    
  return false  
  
  
#################################  
#################################  
def run_pick_click_process(self):
  whereami(sys._getframe().f_code.co_name)
  
  ''' wrapper for run functions '''

  # check for any valid runs, if not, round over
  if is_run_or_block_available(self, "run") == False:
    if round_is_over(self) == True:
      if is_game_over(self) == True: #check round_num
        return False
  else:
    self.ct_run = tilepick_run(self) 
    print "RPC self.ct_run = ", self.ct_run
		
    # PROCESS THE RUN 
    if click_tile_or_wall(self, self.ct_run) == False:
      return False # bail out of this process, something went wrong
		  		
    # SET SOME VALUES BASED ON CT_RUN
    # self.run_row_num -- formerly "n" as in R(subscript n)
    self.run_row_num = int( math.ceil( float(self.ct_run) / float((3 * self.w) + 1) ) )
    #print "RPC self.run_row_num = ", self.run_row_num
    self.run_row_leftedge = int(self._run_row_left_edge(self.run_row_num))
    #print "RPC self.run_row_leftedge = ", self.run_row_leftedge
    ShowBoard(self)
  
    # if return false, catch that in main(), where this is called
    return True


#################################  
def block_pick_click_process(self):
  whereami(sys._getframe().f_code.co_name)
  
  ''' wrapper for block functions '''
  
  if is_run_or_block_available(self, "block") == False:
    if round_is_over(self) == True:
      if is_game_over(self) == True: #check round_num
        return False
  else:
    self.ct_block = tilepick_block(self)
    print "GBB self.ct_block = ", self.ct_block
  
    # PROCESS THE BLOCK 
    if click_tile_or_wall(self, self.ct_block) == False:
      return False # bail out of this process, something went wrong
  
    # need to update valid runs again, with block
    self.valid_runs = calculate_valid_runs(self, self.ct_run, False) 
      
    # calculate longrange_points (and runs)
    self.longrange_runs, self.longrange_points = calculate_longrangers(self)
    
    print "lrvr", self.longrange_runs
    print "lrvp", self.longrange_points
    
    # what conditional?
    if 1 ==1:
      return True
    else:
      return False
    


################################# 
def is_run_or_block_available(self, r_or_b):
  whereami(sys._getframe().f_code.co_name)

  ''' just check length of valid_runs or unclicked_blocks. if zero, then round is over '''
  
  if r_or_b == "run": 
    availability = len(self.valid_runs)
    ## TODO - 
    # 1. if ALL valid runs already scored AND CANNOT get to new unscored, THEN availability = 0
    # BUT this requires CHAINS of lookup from each valid tile, how many? all and NONE are unscored
    # right? so is this required or is this getting deterministic and anti-A.G.0 style?
    availability = len(self.lr_vp)
    
  
  if r_or_b == "block": availability = len(self.unclicked_blocks)
  print "available?", r_or_b
  
  if availability > 0:
    print "yes, some"
    return True
  else:
    print "no, none"
    return False


#################################  
def tilepick_run(self):
  whereami(sys._getframe().f_code.co_name)
  
  '''
  placeholder to pick a tile -- starting tile and in-game as well. 
  will pick by input or by policy, but for now... random is default but other styles may be passable
  '''
  
  # make more complete switch/case for other pick styles
  #print "self.run_style=", self.run_style
  #print "AT THIS STAGE: self.valid_runs=", self.valid_runs
  
  if self.run_style == "random":      
    ct_run = random.choice(self.valid_runs)
  
  else:
    # implement other methods for choosing, but for now...
    ct_run = random.choice(self.valid_runs)
    
  #print "THIS RUN ct_run", ct_run
  
  return ct_run


#################################  
def tilepick_block(self):
  whereami(sys._getframe().f_code.co_name)
  
  '''
  placeholder to pick a tile -- starting tile and in-game as well. 
  will pick by input or by policy, but for now... random is default but other styles may be passable
  '''
  
  # make more complete switch/case for other pick styles
  #print "self.block_style=", self.block_style
  #print "AT THIS STAGE: self.unclicked_blocks=", self.unclicked_blocks
  
  if self.block_style == "random":      
    ct_block = random.choice(self.unclicked_blocks)
    
  else:
    # implement other methods for choosing, but for now...
    ct_block = random.choice(self.unclicked_blocks)
    
  #print "THIS BLOCK ct_block", ct_block
        
  return ct_block



#################################    
def click_tile_or_wall(self, clickthistile):
  whereami(sys._getframe().f_code.co_name)
  
  ''' click a tile or wall, check for validity, probably, by adding to clicked_walls[] '''
  
  # if run_tile add to clicked_runs, if block_tile add to clicked_blocks
  
  if clickthistile in self.run_tiles_list:
    print "logging RUN at ", clickthistile
    self.clicked_runs.append(clickthistile)
    if clickthistile in self.unclicked_runs:
      self.unclicked_runs.remove(clickthistile) # can repeat a spot, but no point
      if clickthistile not in self.clicked_points:
        self.clicked_points.append(clickthistile)
        self.runnerpoints += 1
    

  if clickthistile in self.b_tiles_list:
    print "logging BLOCK at ", clickthistile
    if clickthistile not in self.clicked_blocks:
      # a valid block
      self.clicked_blocks.append(clickthistile)
      self.unclicked_blocks.remove(clickthistile)
      
      
    else:
      # an already blocked block
      return False # used by calling funcs (run_process(), block_process(), close_edges()
    
    
  # update master list
  self.clicked_tiles_walls_list.append(clickthistile) 

  # used by calling funcs (run_process(), block_process(), close_edges()
  if clickthistile in self.clicked_tiles_walls_list: 
    clicksuccess = True 
  else:
    clicksuccess = False
  
  return clicksuccess



################################# 
def calculate_valid_runs(self, fromthistile, basetile=False):
  whereami(sys._getframe().f_code.co_name)
  
  ''' click a tile or wall, check for validity, probably, by adding to clicked_walls[] '''
  
  # get all THEORETICAL options
  theory_runs = find_theoretical_runs(self, fromthistile) 
  
  # limit theory runs to ACTUAL tiles
  print "CVR PRE CHK theory_runs", theory_runs
  print "CVR self.run_tiles_list", self.run_tiles_list
  # now check for existing in master list at self.run_tiles_list
  actual_runs = sorted( list( set(theory_runs) & set(self.run_tiles_list) ) )
  print "CVR POST CHK actual_runs", actual_runs
  
  #remove blocked runs from actuals available
  unblocked_runs = []
  for move_to in actual_runs:
    #print "CVR move_to", move_to
    if basetile == False:
      #print "CVR - basetile false"
      if run_is_unblocked(self, move_to) == True: 
        unblocked_runs.append(move_to) # if blocked, remove from options
    else:
      #print "CVR - basetile TRUE! ",basetile 
      if run_is_unblocked(self, move_to, basetile) == True: 
        unblocked_runs.append(move_to) # if blocked, remove from options
      
  # final check of calculated options
  '''
  if fromthistile not in unblocked_runs:
    self.valid_runs = [] # not needed, but better for human eyes
    self.valid_runs = unblocked_runs[:] # make a copy
    cvr_success = True # used by calling func block_process()
  else:
    cvr_success = False # used by calling func block_process()
  
  print "CVR self.valid_runs", self.valid_runs
  '''

  return unblocked_runs



################################# 
def calculate_longrangers(self):
  whereami(sys._getframe().f_code.co_name)
  ''' from list of tiles (say, valid_runs) create dicts/lists of further valid runs and points
  this will be used to check if runner is in BLOC of used tiles, thus round over'''
  
  # TODO - go more than validruns, but recurse for ALL unique LRVRs
  print "calculate_longrangers"
  self.lr_vr = {} # long range valid runs
  self.lr_vp = [] # long range valid points
  #calc valid runs
  for vr in self.valid_runs:
    #calculate_valid_runs(self, vr)
    print "+++++++++ LRVR ct_run", self.ct_run
    print "+++++++++ LRVR ",vr
    self.lr_vr[vr] = calculate_valid_runs(self, vr, vr)
    
  # find if lrr (long range runs) in lrl (longrangelist)are worth points
  for k,lrl in self.lr_vr.items():
    for lrr in lrl:
      if lrr not in self.clicked_runs and lrr not in self.lr_vp:
        self.lr_vp.append(lrr)
  
  
  print "LR RUNS", self.lr_vr
  print "LR POINTS", self.lr_vp
  
  sys.exit(1)
  return (self.lr_vr, self.lr_vp)
  
  
  


################################# 
def find_theoretical_runs(self, fromthistile):
  whereami(sys._getframe().f_code.co_name)
  ''' check self.runnerpower and build list of options based on that'''
  
  #print "fromthistile = ", fromthistile
  #print "self.runnerpower = ", self.runnerpower
  theory_runs = []

  # do duck power things to build a list
  # later do cheetah, roo, bee, mouse, chicken, frog

  if self.runnerpower == "duck":
    # arranged for readabilty of upper left to lower right
    vert_up = vert_tile(self, "up", fromthistile)
    theory_runs.append(vert_up - 2)
    theory_runs.append(vert_up)
    theory_runs.append(vert_up + 2)
    theory_runs.append(fromthistile - 2)
    theory_runs.append(fromthistile + 2)
    vert_dn = vert_tile(self, "dn", fromthistile)
    theory_runs.append(vert_dn - 2)
    theory_runs.append(vert_dn)
    theory_runs.append(vert_dn + 2)
    
  return theory_runs
  


#################################
def run_is_unblocked(self, runtile, basetile=False):
  whereami(sys._getframe().f_code.co_name)
  
  ''' IMPORTANT FUNCTION (based on runnerpower)
      from self.clicked_blocks and self.ct_run (or basetile if passed) calculate blocked and UNblocked run options 
  '''
  
  # set up vars
  if basetile == False: basetile = self.ct_run
  thisrunrow = run_row_from_tilenum(self, basetile)
  vert_tile_coeff = (basetile - run_row_starter(self, thisrunrow)) / 2
  
  ct_leftedge = basetile - 1
  ct_rightedge = basetile + 1
  ct_top = basetile - (self.w + vert_tile_coeff) - 1
  ct_bottom = basetile + ( (2 * self.w - vert_tile_coeff))
  # up and down edge vertical neighbors
  ct_leftedge_up = ct_leftedge - self.vert_tile_distance
  ct_leftedge_down = ct_leftedge + self.vert_tile_distance
  ct_rightedge_up = ct_rightedge - self.vert_tile_distance
  ct_rightedge_down = ct_rightedge + self.vert_tile_distance
  # top and bottom edge horizontal neighbors
  ct_top_left = ct_top - 1
  ct_top_right = ct_top + 1
  ct_btm_left = ct_bottom - 1
  ct_btm_right = ct_bottom + 1

  #### run thru conditionals for DUCK (others later)
  ## orthagonals and diagonals (include leftedge+leftegdedown, etc)
  if self.runnerpower  == "duck":
    
    is_unblocked = True
    
    # orthagonals
    if runtile == basetile - 2: # LEFT
      if ct_leftedge in self.clicked_blocks: is_unblocked = False

    if runtile == basetile + 2: # RIGHT
      if ct_rightedge in self.clicked_blocks: is_unblocked = False

    if runtile == basetile - self.vert_tile_distance: # UP
      if ct_top in self.clicked_blocks: is_unblocked = False

    if runtile == basetile + self.vert_tile_distance: # DN
      if ct_bottom in self.clicked_blocks: is_unblocked = False

    # diagonals
    if runtile == basetile + self.vert_tile_distance - 2: # DN LEFT
      if ct_bottom in self.clicked_blocks and ct_leftedge in self.clicked_blocks:
        is_unblocked = False
      if ct_bottom in self.clicked_blocks and ct_btm_left in self.clicked_blocks:
        is_unblocked = False
      if ct_leftedge in self.clicked_blocks and ct_leftedge_down in self.clicked_blocks:
        is_unblocked = False
      
    if runtile == basetile + self.vert_tile_distance + 2: # DN RIGHT
      if ct_bottom in self.clicked_blocks and ct_rightedge in self.clicked_blocks: 
        is_unblocked = False
      if ct_bottom in self.clicked_blocks and ct_btm_right in self.clicked_blocks:
        is_unblocked = False
      if ct_rightedge in self.clicked_blocks and ct_rightedge_down in self.clicked_blocks:
        is_unblocked = False  

    if runtile == basetile - self.vert_tile_distance - 2: # UP LEFT
      if ct_top in self.clicked_blocks and ct_leftedge in self.clicked_blocks: 
        is_unblocked = False
      if ct_top in self.clicked_blocks and ct_top_left in self.clicked_blocks: 
        is_unblocked = False
      if ct_leftedge in self.clicked_blocks and ct_leftedge_up in self.clicked_blocks:
        is_unblocked = False
      
    if runtile == basetile - self.vert_tile_distance + 2: # UP RIGHT
      if ct_top in self.clicked_blocks and ct_rightedge in self.clicked_blocks: 
        is_unblocked = False
      if ct_top in self.clicked_blocks and ct_top_right in self.clicked_blocks: 
        is_unblocked = False
      if ct_rightedge in self.clicked_blocks and ct_rightedge_up in self.clicked_blocks:
        is_unblocked = False 
        


  # print "RUB self.clicked_blocks", self.clicked_blocks
  if is_unblocked == True: print "RUB UNblocked run", basetile,"to", runtile
  if is_unblocked == False: print "RUB Blocked run", basetile, "to", runtile
  
  return is_unblocked



#################################
def round_is_over(self):
  whereami(sys._getframe().f_code.co_name)

  ''' hmm, lotsa things. if round 1, move to 2, if 2, move to game_over. '''
  ### TODO -- keep logs, scores, etc

  print "1 RND OVER self.round_num", self.round_num
  print "\n ############## ROUND OVER! ###############\n"
  
  self.round_num += 1
  print "2 RND OVER self.round_num", self.round_num
  
  #lots more things, probably, but for now
  return True



#################################
def is_game_over(self):
  whereami(sys._getframe().f_code.co_name)

  ''' check round_num > round_num_max '''
  
  if self.round_num > self.round_num_max:
    print "yes game over", self.round_num, self.round_num_max
    return True
  else:
    print "not game over", self.round_num, self.round_num_max
    return False
  



################################# 
def game_is_over(gb_board, gb_board_r2):
  whereami(sys._getframe().f_code.co_name)

  ''' TODOs:
  	-- upgrade from lo-fi gameover, man screen ; )
    - double-check and store logs, scores, etc.  
    - print some stuff for the humans looking at output, etc
    - setup for new game, player rankings, etc.
  '''

  if gb_board.runnerpoints > gb_board_r2.runnerpoints:
    this_is_winner = "############  PLAYER 1 win! #################"
    this_is_score = str(gb_board.runnerpoints) + " to " + str(gb_board_r2.runnerpoints)
  elif gb_board.runnerpoints < gb_board_r2.runnerpoints:
    this_is_winner = "############  PLAYER 2 win! #################"
    this_is_score = str(gb_board_r2.runnerpoints) + " to " + str(gb_board.runnerpoints)
  else:
    this_is_winner = "############  DOUBLE WIN! #################"
    this_is_score = str(gb_board.runnerpoints) + " = " + str(gb_board_r2.runnerpoints)
  
  
  board_size = "on a "+str(gb_board.w) + " x " + str(gb_board.h)
  # use a real conditional, but which one?
  if gb_board_r2.round_num > gb_board_r2.round_num_max :
    print "\n\n    #################################"
    print "############    GAME OVER   #################"
    print this_is_winner
    print "         ", this_is_score + " "+ board_size
    print "    #################################\n\n"
    
  # lots more things
  ShowBoard(gb_board_r2)
  return
  
#################################   
# pinched and tweaked from https://github.com/impshum/Multi-Quote/blob/master/run.py
class color:
  white, cyan, blue, red, green, yellow, magenta, black, gray, bold = '\033[0m', '\033[96m','\033[94m', '\033[91m','\033[92m','\033[93m','\033[95m', '\033[30m', '\033[30m', "\033[1m"  

# maybe add bks, bolds, etc from https://godoc.org/github.com/whitedevops/colors
class bkcolor:
  resetall = "\033[0m"
  default      = "\033[49m"
  black        = "\033[40m"
  red          = "\033[41m"
  green        = "\033[42m"
  yellow       = "\033[43m"
  blue         = "\033[44m"
  magenta      = "\033[45m"
  cyan         = "\033[46m"
  lightgray    = "\033[47m"
  darkgray     = "\033[100m"
  lightred     = "\033[101m"
  lightgreen   = "\033[102m"
  lightyellow  = "\033[103m"
  lightblue    = "\033[104m"
  lightmagenta = "\033[105m"
  lightcyan    = "\033[106m"
  white        = "\033[107m"
  
