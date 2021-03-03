'''
    Nam Tran
    CS550 A03
    
    problemsearch.py conducts different types of searches on a particular problem
'''

from basicsearch_lib02.searchrep import (Node, print_nodes)
from basicsearch_lib02.queues import PriorityQueue 
from explored import Explored
import time

class Timer:
    """Timer class
    Usage:
      t = Timer()
      # figure out how long it takes to do stuff...
      elapsed_s = t.elapsed_s() OR elapsed_min = t.elapsed_min()
    """
    
    def __init__(self):
        "Timer - Start a timer"
        self.s_per_min = 60.0  # Number seconds per minute
        self.start = time.time()

    def elapsed_s(self):
        "elapsed_s - Seconds elapsed since start (wall clock time)"
        return time.time() - self.start

    def elapsed_min(self):
        "elapsed_min - Minutes elapsed since start (wall clock time)"

        # Get elapsed seconds and convert to minutes
        return self.elapsed_s() / self.s_per_min

def graph_search(problem, verbose=True, debug=False):
    """graph_search(problem, verbose, debug) - Given a problem representation
    (instance of basicsearch_lib02.representation.Problem or derived class),
    attempt to solve the problem.
    
    If debug is True, debugging information will be displayed.
    
    if verbose is True, the following information will be displayed:
        
        Number of moves to solution
        List of moves and resulting puzzle states
        Example:
        
            Solution in 25 moves        
            Initial state
                  0        1        2    
            0     4        8        7    
            1     5        .        2    
            2     3        6        1    
            Move 1 -  [0, -1]
                  0        1        2    
            0     4        8        7    
            1     .        5        2    
            2     3        6        1    
            Move 2 -  [1, 0]
                  0        1        2    
            0     4        8        7    
            1     3        5        2    
            2     .        6        1    
            
            ... more moves ...
            
                  0        1        2    
            0     1        3        5    
            1     4        2        .    
            2     6        7        8    
            Move 22 -  [-1, 0]
                  0        1        2    
            0     1        3        .    
            1     4        2        5    
            2     6        7        8    
            Move 23 -  [0, -1]
                  0        1        2    
            0     1        .        3    
            1     4        2        5    
            2     6        7        8    
            Move 24 -  [1, 0]
                  0        1        2    
            0     1        2        3    
            1     4        .        5    
            2     6        7        8    
        
        If no solution were found (not possible with the puzzles we
        are using), we would display:
        
            No solution found
    
    Returns a tuple (path, nodes_explored) where:
    path - list of actions to solve the problem or None if no solution was found
    nodes_explored - Number of nodes explored (dequeued from frontier)
    """
    # Starting the timer
    t = Timer()
    
    # Creating frontier and explored
    frontier = PriorityQueue(f=Node.get_f)
    explored = Explored()
    root = Node(problem = problem, state = problem.initial, parent = None, action = None)
    frontier.append(root)
    explored.add(root.state)
    
    # Initializing the search
    parentNode = frontier.pop()
    
    # While the board is unsolved, search the nodes according to specified search
    while not parentNode.state.solved():
        childrenNodes = parentNode.expand(problem=problem)
        
        for i in range(childrenNodes.__len__()):
            if not explored.exists(childrenNodes[i].state):
                explored.add(childrenNodes[i].state)
                frontier.append(childrenNodes[i])
        
        parentNode = frontier.pop()
    
    solutionPath = parentNode.solution()
    
    #Verbose mode logging
    if (verbose == True):
        print("Solution in " + str(len(solutionPath)) + " moves with path:")
        print(solutionPath)
        print("Initial State")
        newBoard = problem.nPuzzleBoard
        print(newBoard)
        for i in range(len(solutionPath)):
            print("Move " + str(i) + " - " + str(solutionPath[i]))
            newBoard = newBoard.move(solutionPath[i])
            print(newBoard)
            
    nodesExplored = explored.getLength()
    print("Solution in " + str(len(solutionPath)) + " moves.")
    print("Nodes explored: " + str(nodesExplored))       
    print("Done in " + str(t.elapsed_s()) + " seconds")
    return (len(solutionPath), nodesExplored, t.elapsed_s())

    
    