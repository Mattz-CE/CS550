"""
    Nam Tran
    CS550 A03

Contains g and h functions for:
BreadFirst - breadth first search
DepthFirst - depth first search
Manhattan - city block heuristic search
"""

import math

class BreadthFirst:
    @classmethod
    def g (cls, parentnode, action, childnode):
        return childnode.depth
    
    @classmethod
    def h(cls, state):
        return 0

class DepthFirst:
    @classmethod
    def g (cls, parentnode, action, childnode):
        return (-childnode.depth)
    
    @classmethod
    def h(cls, state):
        return 0
        
class Manhattan:
    @classmethod
    def g (cls, parentnode, action, childnode):
        return parentnode.depth + 2
    
    @classmethod
    def h (cls, state):
        distanceSum = 0
        tileGoal = [0,0]
        goals = list()
        
        # Getting tile locations for solved board state
        for rows in range(state.get_rows()):
            for columns in range(state.get_cols()):
                goals.append([rows,columns])
        
        currentState = state.board
        
        # Iterating over every tile to find Manhattan Distance Sum
        for rows in range(state.boardsize):
            for columns in range(state.boardsize):
                tileValue = currentState[rows][columns]
                if (tileValue == None):
                    tileGoal = goals[len(goals)-1]
                    distanceSum += abs(rows - tileGoal[0]) + abs(columns - tileGoal[1])
                else:
                    tileGoal = goals[tileValue-1]
                    distanceSum += abs(rows - tileGoal[0]) + abs(columns - tileGoal[1])
        
        return distanceSum
        
                    
        
                

       
