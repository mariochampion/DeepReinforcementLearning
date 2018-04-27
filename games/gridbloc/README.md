## adding gridbloc game

## PURPOSE
the goal here is to mathematically describe the DUAL + OVERLAPPING grids of gridbloc game, which required both running tiles and blocking tiles, so that arrays of valid choices can be calculated as needed. (the grid could, alternately, be said to have non-equal row-lengths (ie, diff num of columns), if you like.) the grid for running tiles is pretty classic, just cap all 4 edges (in an rectangular grid version) of each running tile with a tile to block and you see the dual/overlapping/interposed grid system of gridbloc.

unlike most other board games, there are TWO rounds, and the winner of the game is whomever has the most points after each player has run (so, 2 rounds in a 2 player game). runners earn points for each NEW tile they occupy during a game, and may return to already scored tiles as a matter of strategy, but wont get an extra point for that move. specifically, a tile can only be scored once per game, and blockers dont earn points, they just try to limit the points the runner earns by blocking them in.

## IMPORTANT CONDITIONS
 * runner moves first, blocker moves next. that is one turn.
 * The end-round condition occurs when no un-scored tiles available for a runner to reach with a valid move.
 * at the end of a round, the players swap roles. new runner makes first move.
 * The end-game condition occurs at the end of round two.
 * The winner has the higher run score AFTER end of round two.
 
 ## NOTE: 
 * blocking tiles (hor and vert, including edge walls etc) will be calculated from w & h 
 * "n" is the row number (n=3 is the 3rd row, etc) --now called "self.run_row_num"
 * "ct_run" is the NUMBER of the current_tile, which is NOT a A7 or F2 chess style notation, but a simple integer calculated from row width, according to the formulas which account for interposing blocking tiles.
 * the upper left RUNNING tile is NEITHER 1 nor 0 (zero). the upper left column horizontal top tile is actually 1, as a blocking tile ATOP each row uses numbers 1 to w. so then, w+1 is the left border wall for the first row, and the first running tile is w+2.

## SOME FORMULAS
### NOTE: need to calculate "ct_run" when starting, from the available runner options. then track as runner moves, using the formulas.
### NOTE: "n" is calculated from ct_run and w, then track as runner moves, using the formulas.

