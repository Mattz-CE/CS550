import random
import copy
import math

from basicsearch_lib02.board import Board


class TileBoard(Board):
    def __init__(self, n, multiple_solutions=False, force_state=None,
                 verbose=False):
        """"TileBoard(n, multiple_solutions, force_state)
        Create a tile board for an n puzzle.
        
        If multipleSolutions is true, the solution need not
        be in the bottom right.  This defaults to False but
        is automatically set to True when there is no middle square 
        
        force_state can be used to initialize an n puzzle to a desired
        configuration.  No error checking is done.  It is specified as
        a list with n+1 elements in it, 1:n and None in the desired order.
        """
        
        self.verbose = verbose
        

        self.boardsize = int(math.sqrt(n+1))  
        if math.sqrt(n+1) != self.boardsize:
            raise ValueError("Bad board size\n" +
                "Must be one less than an odd perfect square 8, 24, ...")

        # initialize parent
        super().__init__(self.boardsize, self.boardsize)


        # Compute solution states
        if multiple_solutions:
            # Create list of goals [(None, 1, 2, 3, ..), (1, None, 2, 3, ...),
            #                        (1, 2, None, 3, ...), ...]
            self.goals = []
            for hole_position in range(n+1):
                solution = []
                # Add numbers 1 to n, placing a None at current hole_position
                for idx in range(n+1):
                    if idx < hole_position:
                        solution.append(idx+1)
                    elif idx == hole_position:
                        solution.append(None)
                    else:
                        solution.append(idx)
                self.goals.append(tuple(solution))

        else:
            # Single goal, hole in last position [(1, 2, 3, ..., None)]
            self.goals = [tuple([None if idx == n else idx+1
                                     for idx in range(n+1)])]

        if force_state:
            tiles = force_state
            if not self.solvable(tiles):
                raise ValueError("Puzzle is not solvable")
        else:
            # Build initial state - all in order
            tiles = [val+1 for val in range(n)]
            tiles.append(None)
            # Verify problem is solvable
            done = False
            while not done:
                random.shuffle(tiles)  # mix up tiles
                done = self.solvable(tiles)

        # populate the board with our tile order
        for r in range(self.boardsize):
            for c in range(self.boardsize):
                tile = tiles[r*self.boardsize + c]  # next tile
                if tile:                    
                    self.place(r, c, tile)
                else:
                    # keep track of empty tile
                    self.empty = (r, c)
    
    def solvable(self, tiles, verbose=False):
        """solvable - Determines if a puzzle is solvable

            Given a list of tiles, determine if the N-puzzle is solvable.
            You do not need to know how to do this, but the calculation
            is based on the inversion order.

            for each number in the list of tiles,
               How many following numbers are less than that one
               e.g. [13, 10, 11, 6, 5, 7, 4, 8, 1, 12, 14, 9, 3, 15, 2, None]
               Example:  Files following 9:  [3, 15, 2, None]
               Two of these are smaller than 9, so the inversion order
                   for 9 is 2

            A puzzle's inversion order is the sum of the tile inversion
            orders.  For puzzles with even numbers of rows and columns,
            the row number on which the blank resides must be added.
            Note that we need not worry about 1 as there are
            no tiles smaller than one.

            See Wolfram Mathworld for further explanation:
                http://mathworld.wolfram.com/15Puzzle.html
            and http://www.cut-the-knot.org/pythagoras/fifteen.shtml

            This lets us know if a problem can be solved.  The inversion
            order modulo 2 is invariant across moves.  This means that
            when we make a legal move, the inversion order will always
            be even or odd.  The solution state always has an even
            inversion order, so any puzzle with an odd inversion
            number cannot be solved.
        """

        inversionorder = 0
        # Make life easy, remove None
        reduced = [t for t in tiles if t is not None]
        # Loop over all but last (no tile after it)
        for idx in range(len(reduced)-1):
            value = reduced[idx]
            after = reduced[idx+1:]  # Remaining tiles
            smaller = [x for x in after if x < value]
            numtiles = len(smaller)
            inversionorder = inversionorder + numtiles
            if verbose:
                print("idx {} value {} tail {} #smaller {} sum: {}".format(
                    idx, value, after, numtiles, inversionorder))

        # Account for blank when there are an even number of rows
        if self.get_rows() % 2 == 0:
            if verbose:
                print("Even # rows, adding for position of blank")
            inversionorder = inversionorder + \
                math.floor(tiles.index(None) / self.boardsize)+1

        solvable = inversionorder % 2 == 0  # Solvable if even
        return solvable
                                
    def __hash__(self):
        "__hash__ - Hash the board state"
        
        # Convert state to a tuple and hash
        return hash(self.state_tuple())
    
    def __eq__(self, other):
        "__eq__ - Check if objects equal:  a == b"

        # Are states identical?
        return self.state_tuple() == other.state_tuple()

        # Set pairs to be equal to another
        # equal = True  # until we found out otherwise
        # # pair up board items in tuples and compare them
        # for (mystate, otherstate) in zip(self.state_tuple(), other.state_tuple()):
        #     equal = mystate == otherstate
        #     if not equal:
        #         break
        # return equal
    
    def state_tuple(self):
        "state_tuple - Return board state as a single tuple"
        
        # Iterate over the items in each list, merging them
        flattened = [item for sublist in self.board
                            for item in sublist]
        # convert to tuple (hashable) and return 
        return(tuple(flattened))
    
    def get_actions(self):
        "Return row column offsets of where the empty tile can be moved"
        
        actions = []
        # check row and column, no diagonal moves allowed
        boarddims = [self.get_rows(), self.get_cols()]
        for dim in [0, 1]:  # rows, then columns
            # Append offsets to the actions list, 
            # e.g. move left --> (-1,0)
            #      move down --> (0, 1)
            # Note that when we append to the list of actions,
            # we use list( ) to make a copy of the list, otherwise
            # we just get a pointer to it and modification of offset
            # will change copies in the list.
            offset = [0, 0]
            # add if we don't go off the top or left
            if self.empty[dim] - 1 >= 0:
                offset[dim] = -1
                actions.append(list(offset))
            # append if we don't go off the bottom or right
            if self.empty[dim] + 1 < boarddims[dim]:
                offset[dim] = 1
                actions.append(list(offset))
                
        return actions
          
    def move(self, offset):
        """move - Move the empty space by [delta_row, delta_col] and 
        return new TileBoard
        """
        
        # Current row and column of empty space
        (r, c) = self.empty
        
        [delta_r, delta_c] = offset
        
        # validate
        rprime = r + delta_r
        cprime = c + delta_c
        if rprime < 0 or cprime < 0 or \
            rprime >= self.get_rows() or cprime >= self.get_cols():
            raise ValueError("Illegal move (%d,%d) from (%d,%d)"%(
                    delta_r, delta_c, r, c))

        # Make a copy of the board so that mutating it does not 
        # modify other copies of the board.  Not the most efficient
        # way to do this, but it will get the job done.
        newboard = copy.deepcopy(self)
        # Slide a tile into the empty slot position
        newboard.place(r, c, self.get(rprime, cprime))
        # update empty position
        newboard.place(rprime, cprime, None)
        newboard.empty = (rprime, cprime)
        
        return newboard
        
    #def __repr__(self):
    #    """Alternate board representation - as state tuple
    #       Useful for verifying that solutions do not have duplicate
    #       states in path."""
    #    return str(self.state_tuple())
    
    def solved(self):
        "solved - Is the puzzle solved?"

        # Check if state is in goals
        solved = self.state_tuple() in self.goals
        return solved