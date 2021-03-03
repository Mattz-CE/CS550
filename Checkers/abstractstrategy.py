"""
    Nam Tran
    A04
    
    abstractstrategy.py contains the user-written strategy for checkers, implementing
    an alpha beta search with a custom built utility function which weighs several
    different factors respective to the current board state.

"""

import checkerboard
import math
import random

class Strategy:
    """"Abstract strategy for playing a two player game.
    Abstract class from which specific strategies should be derived
    """
        
    def __init__(self, player, game, maxplies):
        """"Initialize a strategy
        player is the player represented by this strategy
        game is a class or instance that supports the class or instance method
            game.other_player(player) which finds the name 
                of the other player
        maxplies is the maximum number of plies before a cutoff is applied
        """
        
        # Useful for initializing any constant values or structures
        # used to evaluate the utility of a board
        self.maxplayer = player
        self.minplayer = game.other_player(player)
        self.maxplies = maxplies
        self.depth = 0
        self.prevBoardPieces = 0
        self.currBoardPieces = 0
        self.baseCasePieceCount = True
    
    def utility(self, board):
        "Return the utility of the specified board"
        # Initialization of necessary variables and players
        val = 0
        player = board.playeridx(self.maxplayer)
        opponent = board.playeridx(self.minplayer)
        
        # Evaluation of player's pieces with variable weights
        pawnWeight = 1
        kingWeight = 2
        
        pawnCount = board.get_pawnsN()[player] - board.get_pawnsN()[opponent]
        kingCount = board.get_kingsN()[player] - board.get_kingsN()[opponent]
        
        val += (pawnWeight *pawnCount) + (kingWeight * kingCount)
        
        # Evaluation of distances from each piece to each player's castle
        for row, column, piece in board:
            (playerType, isKing) = board.identifypiece(piece)
            if isKing == False:
                if playerType == player:
                    val += board.disttoking(piece,row)
                else:
                    val -= board.disttoking(piece,row)
            if ((row == 0) or (row == board.edgesize-1) or (column == 0) or (column == board.edgesize-1)):
                if playerType == player:
                    val += board.edgesize
                else:
                    val -= board.edgesize
        
        # Evaluation of total number of hops and pieces differential
        if (self.baseCasePieceCount == True):
            self.prevBoardPieces = self.currBoardPieces = [(board.get_pawnsN()[player] + board.get_kingsN()[player]), board.get_pawnsN()[opponent] + board.get_kingsN()[opponent]]
            self.baseCasePieceCount == False
        else:
            self.prevBoardPieces = self.currBoardPieces
            self.currBoardPieces = [(board.get_pawnsN()[player] + board.get_kingsN()[player]), board.get_pawnsN()[opponent] + board.get_kingsN()[opponent]]
        
        diffPlayer = self.prevBoardPieces[0] - self.currBoardPieces[0]
        diffOpponent = self.prevBoardPieces[1] - self.prevBoardPieces[1]
        
        if (diffPlayer < diffOpponent):
            val += (diffOpponent)
        else:
            val += (diffOpponent - diffPlayer)
        return val
    
    def play(self, board, moveCount):
        """"play - Make a move
        Given a board, return (newboard, action) where newboard is
        the result of having applied action to board and action is
        determined via a game tree search (e.g. minimax with alpha-beta
        pruning).
        """
        self.depth = 0
        if (moveCount == 1):
            possibleActions = board.get_actions(self.maxplayer)
            move = possibleActions[random.randint(0,len(possibleActions)-1)]
            return (board.move(move), move)
        else:

            return (board.move(self.alphaBeta(board)), self.alphaBeta(board))
    
    def alphaBeta(self, board):
        "Performs an alpha beta search on the board"
        optimalVal = self.maxVal(state = board, alpha = -math.inf, beta = math.inf)
        
        # Comparing utility with optimalVal to determine best move
        possibleActions = board.get_actions(self.maxplayer)
        for move in possibleActions:
            val = self.utility(board.move(move))
            if abs(optimalVal - val) < 1:
                return move
        
    def maxVal(self, state, alpha, beta):
        "Returns max value for alpha beta"
        utility = 0
        # Checking for base case (terminal)
        if (state.is_terminal()[0] == True):
            utility = self.utility(state)
        # Search for values from possible actions stemming from board
        else:
            val = -math.inf
            possibleActions = state.get_actions(self.maxplayer)
            
            # Return val if we have reached the designated maxplies
            if self.depth > self.maxplies:
                return val
            self.depth += 2
            
            for action in possibleActions:
                # Comparison between previous val and minVal
                val = max(val, self.minVal(state = state.move(action), alpha = alpha, beta = beta))
                utility = self.utility(state.move(action))
                
                if (utility >= beta):
                    break
                else:
                    alpha = max(alpha, utility)
        return utility
    
    def minVal(self, state, alpha, beta):
        "Returns min value for alpha beta"
        utility = 0
        # Checking for base case (terminal)
        if (state.is_terminal()[0] == True):
            utility = self.utility(state)
        # Search for values from possible actions stemming from board
        else:
            val = math.inf
            possibleActions = state.get_actions(self.minplayer)
            
            # Return val if we have reached the designated maxplies
            if self.depth > self.maxplies:
                return val
            self.depth += 2
            
            for action in possibleActions:
                # Comparison between previous val and maxVal
                val = min(val, self.maxVal(state = state.move(action), alpha = alpha, beta = beta))
                utility = self.utility(state.move(action))
                
                if (utility <= alpha):
                    break
                else:
                    beta = min(beta, utility)
        return utility
