#!/usr/bin/env python
''' 
GRIDBLOC support functions.
'''



show_whereami = True


##################################	
## just a debug placefinder to help trace actions
def whereami(funcname):
  if show_whereami == True:
    print
    print "-------------", funcname, " ------------------" 
    print