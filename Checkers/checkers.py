"""
    Nam Tran
    A04
    
    checkers.py is the driver for A04. It instantiates a game of checkers between
    the user AI (alpha beta) and the professor's Tonto AI. The game runs until
    there is a draw or one side wins.

"""

# Game representation and mechanics
import checkerboard

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.  Big sister is watching you :-)

# Python cand load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
import imp
import sys
major = sys.version_info[0]
minor = sys.version_info[1]
modpath = "__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
tonto = imp.load_compiled("tonto", modpath)


# human - human player, prompts for input    
import human

import abstractstrategy

import boardlibrary # might be useful for debugging

from timer import Timer
        

def Game(red=abstractstrategy.Strategy, black=tonto.Strategy, 
         maxplies=4, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 
    """

    # Don't forget to create instances of your strategy,
    # e.g. black('b', checkerboard.CheckerBoard, maxplies)
    board = checkerboard.CheckerBoard()
    redChecker = red('r', board, maxplies)
    blackChecker = black('b', board, maxplies)
    
    # Initialization of necessary variables/lists
    players = [redChecker,blackChecker]
    moveCount = 1
    t = Timer()
    
    # Looping plays until board is in terminal state
    while board.is_terminal()[0] == False:
        print("\n\n-------------------------------------------------")
        print("Turn #: " + str(moveCount))
        print("Current board:\n:", board)
        
        #Red player's moves
        board = players[0].play(board, moveCount)[0]
        print ("(RED) LONE RANGER'S MOVE: \n", board)
        
        #Black player's moves
        board = players[1].play(board)[0]
        print("(BLACK) TONTO'S MOVE: \n", board)
        
        moveCount += 1
    
    # Stalemate condition
    if (board.is_terminal()[1] == None):
        print("The winner is: NOBODY in " + str(moveCount) + " moves!\n")
    # Win condition
    else:
        print("The winner is: " + str(board.is_terminal()[1] + " in " + str(moveCount) + " moves!\n"))
    
    print("Elapsed time in seconds: " + str(t.elapsed_s()))
        
        
        
        
    
            
if __name__ == "__main__":
    Game()
        
        
        


        
                    
            
        

    
    
