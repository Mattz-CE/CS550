'''
    Nam Tran
    CS550 A03
'''
class Explored(object):
    "Maintain an explored set.  Assumes that states are hashable"

    def __init__(self):
        "__init__() - Create an empty explored set"
        self.exploredSet = set()
        
    def exists(self, state):
        """exists(state) - Has this state already been explored?
        Returns True or False, state must be hashable
        """
        if state.state_tuple() in self.exploredSet:
            return True
        else:
            return False
    
    def add(self, state):
        """add(state) - add given state to the explored set.  
        state must be hashable and we asssume that it is not already in set
        """
        self.exploredSet.add(state.state_tuple())
    
    def getLength(self):
        """getLength() - gets the number of explored nodes
        """
        numItems = 0
        
        for items in self.exploredSet:
            numItems += 1
        
        return numItems
