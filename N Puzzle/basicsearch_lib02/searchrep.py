'''
searchrep - Classes and functions for representing search
Created on Feb 8, 2018

Based on Russell, S. J., and Norvig, P. (2010). Artificial intelligence : 
    a modern approach (Prentice Hall, Upper Saddle River), pp. xviii, 1132 p.

Contains contributions from multiple authors

'''

def print_nodes(nodes):
    "print_nodes(nodes) - display a set of search nodes on the same line"
    
    if len(nodes) > 0:
        nodereps = []  # string representation of each node
        linecounts = []  # lines in string representation
        widthstr = []  # format string for each node to align display

        # Split representation into lines and add to list
        for n in nodes:
            # create a string representation of the search node
            lines = str(n).split("\n")
            # Make format string k characters wider than longest node line
            # Produces format for fixed length string field, e.g. %12s
            maxlinelen = max([len(l) for l in lines])
            widthstr.append("%%%ds"%(maxlinelen+2))
            linecounts.append(len(lines))  # track # lines needed for node
            nodereps.append(lines)
        
        for lineidx in range(max(linecounts)):
            for nodeidx in range(len(nodes)):
                # Print out row of node representation and stay on same line
                try:
                    print(widthstr[nodeidx]%(nodereps[nodeidx][lineidx]), end='') 
                except IndexError:
                    # This node has fewer lines than the longest one
                    print(widthstr[nodeidx]%" ", end='') 
            print() # move to next line
            


class Problem(object):
    """The abstract class for a formal problem.  You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goals=None, 
                 g = lambda oldnode, action, newnode : oldnode.depth+1, 
                 h = lambda newnode : 0):
        """The constructor specifies the initial state, and one or
        more goal states if they are countable states (override goal_test to
        provide a suitable goal predicate if this is not the case).
        
        Callers should provide functions to estimate g (cost from initial
        node to current node in search tree) as an argument of the 
        of the new edge of the search tree being added:
            oldnode, action that caused transition, newnode
        and h, the heuristic value for the newnode.
        
        By default, breadth-first search behavior is provided.
        
        Your subclass's constructor can add other arguments.
        """
        
        self.initial = initial  # store initial state
        
        # store goal(s) as a list (make it a list if it is not)
        if goals != None:
            self.goals = goals if isinstance(goals, list) else list(goals)
        else:
            self.goals = []
        
        # store function handles
        self.g = g
        self.h = h 

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        
        return state.get_actions()

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method checks if
        state is one of the constructor specified goals. Override this
        method if checking against a list of goals is not sufficient."""
        return state in self.goals

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError
    
    
# -----------------------------------------------------------------------------

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Uses the problem's
    implementation of the cost and heuristic functions to estimate the cost f of
    arriving at the node f and the estimate to the goal node h.
    
    You will not need to subclass this class.
    """

    def __init__(self, problem, state, parent=None, action=None):
        "Create a search tree Node, derived from a parent by an action."
        self.problem = problem # Save problem representation
        self.state = state
        self.parent = parent
        self.action = action
        # find new node's depth and parent and cost from start
        if parent:
            self.depth = parent.depth + 1
            if not action:
                raise ValueError("New search nodes can only be derived " +
                                 "via an action")
            self.g = problem.g(parent, action, self)
        else:
            self.depth = 0  # root of search tree
            self.g = 0  # cost of initial nodes
            
        self.h = problem.h(self.state)
        self.f = self.g + self.h
           
    def expand(self, problem):
        "List the nodes reachable in one step from this node."
        return [self.child_node(action)
                for action in problem.actions(self.state)]

    def child_node(self, action):
        """"child_node - Derive child node by applying an action to problem 
        problem contains the current state representation
        action indicates how the new state will be derived from the current
        Similar to Fig. 3.10 of your text."""

        # derive new state
        nstate = self.problem.result(self.state, action)
        # Create child
        return Node(self.problem, nstate, parent=self, action=action)

    def solution(self):
        "Return the sequence of actions to go from the root to this node."
        return [node.action for node in self.path()[1:]]

    def path(self):
        "Return a list of nodes forming the path from the root to this node."
        node, path = self, []
        # Chase parent pointers, appending each node as it is found
        while node:
            path.append(node)
            node = node.parent
        # List is from goal to initial state,
        # reverse to provide initial state to goal
        path.reverse()
        return path
    
    def get_f(self):
        "get_f estimate of cost from initial node to goal node"
        return self.f
    
    def get_g(self):
        "get_g estimate of cost form initial node to this node"
        return self.g
    
    def get_h(self):
        "get_h estimate of cost from this node to closest goal"
        return self.h    
    # We want for a queue of nodes in breadth_first_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __lt__(self, node):
        return self.f < node.f

    def __hash__(self):
        return hash(self.state)
    
    def __repr__(self):
        return "f=%.1f (g=%.1f + h=%.1f)\n%s"%(
                self.f, self.g, self.h, self.state)

# -----------------------------------------------------------------------------





