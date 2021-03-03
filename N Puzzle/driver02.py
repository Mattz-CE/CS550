'''
    Nam Tran
    CS550 A03
    
    driver02.py is the main for A03. It creates 31 trials of different search techniques
     to solve an nPuzzle of x size. Prints out the average, and standard deviation of
     number of steps to solution, number of nodes expanded, and time elapsed in seconds
     for each search technique.
'''

from statistics import (mean, stdev)  # Only available in Python 3.4 and newer

from npuzzle import NPuzzle
from basicsearch_lib02.tileboard import TileBoard
from searchstrategies import (BreadthFirst, DepthFirst, Manhattan)
from problemsearch import graph_search
import collections
import time
import searchstrategies
import statistics

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
    
def driver() :
    # Variable initializations
    numTrials = 1
    nPuzzleSize = 8
    t = Timer()
    breadthList = list()
    depthList = list()
    manhattanList = list()
    for i in range(numTrials):
        print("Starting Trial " + str(i+1))
        print("----BreadthFirst----")
        bfPuzzle = NPuzzle(nPuzzleSize, g = BreadthFirst.g, h = BreadthFirst.h)
        breadthList.append(graph_search(bfPuzzle))
        print("Time elapsed in seconds from beginning: " + str(t.elapsed_s()))
        print("\n")
        
        print("----DepthFirst----")
        dfPuzzle = NPuzzle(nPuzzleSize, g = DepthFirst.g, h = DepthFirst.h)
        depthList.append(graph_search(dfPuzzle))
        print("Time elapsed in seconds from beginning: " + str(t.elapsed_s()))
        print("\n")
        
        print("----Manhattan----")
        manhattanPuzzle = NPuzzle(nPuzzleSize, g = Manhattan.g, h = Manhattan.h)
        manhattanList.append(graph_search(manhattanPuzzle))
        print("Time elapsed in seconds from beginning: " + str(t.elapsed_s()))
        
        print("\n\n")
        
    # Creating lists for the table
    solutions = list()
    nodesExplored = list()
    timeElapsed = list()
    
    for i in range(len(breadthList)):
        solutions.append(breadthList[i][0])
        nodesExplored.append(breadthList[i][1])
        timeElapsed.append(breadthList[i][2])
        
    print("----BreadthFirst Table----")     
    print("Category\tMean(Average)\tStandard Deviation")
    print("Steps to solution\t" + str(statistics.mean(solutions)) + "\t" + str(statistics.stdev(solutions)))
    print("Nodes Explored\t" + str(statistics.mean(nodesExplored)) + "\t" + str(statistics.stdev(nodesExplored)))
    print("Time elapsed\t" + str(statistics.mean(timeElapsed)) + "\t" + str(statistics.stdev(timeElapsed)))
    
    solutions = list()
    nodesExplored = list()
    timeElapsed = list()
    
    for i in range(len(depthList)):
        solutions.append(depthList[i][0])
        nodesExplored.append(depthList[i][1])
        timeElapsed.append(depthList[i][2])
        
    print("----DepthFirst Table----")     
    print("Category\tMean(Average)\tStandard Deviation")
    print("Steps to solution\t" + str(statistics.mean(solutions)) + "\t" + str(statistics.stdev(solutions)))
    print("Nodes Explored\t" + str(statistics.mean(nodesExplored)) + "\t" + str(statistics.stdev(nodesExplored)))
    print("Time elapsed\t" + str(statistics.mean(timeElapsed)) + "\t" + str(statistics.stdev(timeElapsed)))
    
    solutions = list()
    nodesExplored = list()
    timeElapsed = list()
    
    for i in range(len(manhattanList)):
        solutions.append(manhattanList[i][0])
        nodesExplored.append(manhattanList[i][1])
        timeElapsed.append(manhattanList[i][2])
        
    print("----Manhattan Table----")     
    print("Category\tMean(Average)\tStandard Deviation")
    print("Steps to solution\t" + str(statistics.mean(solutions)) + "\t" + str(statistics.stdev(solutions)))
    print("Nodes Explored\t" + str(statistics.mean(nodesExplored)) + "\t" + str(statistics.stdev(nodesExplored)))
    print("Time elapsed\t" + str(statistics.mean(timeElapsed)) + "\t" + str(statistics.stdev(timeElapsed)))
    
    
if __name__ == '__main__':
    driver()
