"""
    Nam Tran
    CS550 A05
    
    driver.py is the driver for Assignment 5. It creates two Sudoku puzzles
      of varying difficulty and attempts to solve them using AC3 Constraint
      Propogation algorithm. If AC3 fails, it attempts to solve the puzzle
      using a Backtracking Search algorithm.
"""
from csp_lib.sudoku import (Sudoku, easy1, harder1)
from constraint_prop import AC3
from csp_lib.backtrack_util import mrv
from backtrack import backtracking_search


for idx, puzzle in enumerate([easy1, harder1]):
    s  = Sudoku(puzzle)  # construct a Sudoku problem
    
    # Displaying initial informations
    print("\n\n----------------------------------------------------------")
    print ("INITIAL STATE OF SUDOKU:")
    if (idx == 0):
        print("DIFFICULTY: EASY")
    else:
        print("DIFFICULTY: HARD")
        
    s.display(s.infer_assignment())
    
    # Starting AC3 Constraint Propogation Algorithm
    AC3(s)
    print("\nPOST AC3 STATE OF SUDOKU:")
    s.display(s.infer_assignment())
    
    if (s.goal_test(s.curr_domains)):
        print("WINNER WINNER CHICKEN DINNER")
        
    # Starting Backtracking Search Algorithm
    else:
        print("\nAC3 HAS FAILED US, STARTING BACKTRACK:")
        print("*Don't panic! It has not frozen, just takes a while")
        if (backtracking_search(s) != None):
            print ("POST BACKTRACK STATE OF SUDOKU:")
            s.display(s.infer_assignment())
            if(s.goal_test(s.curr_domains)):
                print("WINNER WINNER CHICKEN DINNER")
        else:
            print("BACKTRACKING HAS FAILED, ABANDON ALL HOPE")