#!/usr/bin/env python
''' 
GRIDBLOC support functions.
'''


## GLOBAL vars (mostly for use in this file?)
show_whereami = True


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
  print "END GBB self.clicked_tiles_walls_list = ", self.clicked_tiles_walls_list
  print "END GBB self.clicked_runs = ", self.clicked_runs
  print "END GBB self.valid_runs = ", self.valid_runs
  print "END GBB self.unclicked_runs =", self.unclicked_runs
  print
  print "END GBB self.ct_block = ", self.ct_block
  print "END GBB self.clicked_blocks = ", self.clicked_blocks
  print "END GBB self.unclicked_blocks =", self.unclicked_blocks
  print "-------- end summary ----------\n\n"     
  
  
#################################    
def block_row_hor_list(self, this_b_row):
  gbutil.whereami(sys._getframe().f_code.co_name)
  
  ''' create list of horizontal blocker tiles on THIS B ROW '''
  
  if this_b_row == False: return False # nothing to do
  if self.b_tile_type == 2: return False
  
  if self.b_tile_type == 1:
    #print "tiletype HORIZONTAL = ", this_b_row
    b_row_h_list = self.b_hortiles_dict[this_b_row]
        
  print "this_b_row", this_b_row, "for b_row_h_list", b_row_h_list

  return b_row_h_list  



#################################    
def block_row_vert_list(self, this_b_col):
  gbutil.whereami(sys._getframe().f_code.co_name)
  
  ''' create list of VERTICAL blocker tiles in this run row '''
    
  if this_b_col == False: return False # nothing to do
  if self.b_tile_type == 1: return False # mistaken call -- do nothing
    
  if self.b_tile_type == 2: 
    #print "tiletype VERTICAL col =", this_b_col
    b_row_v_list = self.b_vertiles_dict[this_b_col]  
  
  print "end: this_b_col",this_b_col,"has b_row_v_list", b_row_v_list
  
  return b_row_v_list


    