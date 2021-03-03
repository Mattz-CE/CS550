'''
    Nam Tran
    CS550 A03
    
    npuzzle.py contains the NPuzzle class, which creates an nPuzzle of specified
    size to solve.
'''

from basicsearch_lib02.tileboard import TileBoard
from basicsearch_lib02.searchrep import Problem


class NPuzzle(Problem):
    """"__init__(n, force_state, **kwargs)
        
        NPuzzle constructor.  Creates an initial TileBoard of size n.
        If force_state is not None, the puzzle is initialized to the
        specified state instead of being generated randomly.
        
        The parent's class constructor is then called with the TileBoard
        instance any any remaining arguments captured in **kwargs.
        """
    def __init__(self, n, force_state=None, **kwargs):
        self.nPuzzleBoard = TileBoard(n, force_state = force_state, multiple_solutions = False)
        super(NPuzzle, self).__init__(self.nPuzzleBoard, goals=self.nPuzzleBoard.goals, **kwargs)
    
    """actions(self,state)
    
        Returns a list of possible actions of a certain board state
    """
    def actions(self, state):
        return state.get_actions()
    
    """result(sefl, state, action)
    
        Applies the move action to a certain board state and returns
        the new board state
    """
    def result(self, state, action):
        if (action not in state.get_actions()):
            raise ValueError (str(action) + """ is an illegal action\n These
                              are the only actions: """ + state.getactions())
            
        return state.move(action)
    
    """goal_test(self, state)
    
        Test is the certain board state is a solved state for the nPuzzle.
        Returns true if solved, false if not
    """
    def goal_test(self, state):
        return state.solved()

    
        



