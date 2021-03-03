"""
    Nam Tran
    CS550 A05
    
    constraint_prop.py contains the functions required to use the AC3
      Constraint Propogation algorithm.
"""

def AC3(csp, queue=None, removals=None):
    """AC3 constraint propagation
    
    """
    csp.support_pruning()
    
    # Creating queue and populating with binary arcs tuples
    queue = list()
    for X_i in csp.variables:
        for X_k in csp.neighbors[X_i]:
            queue.append((X_i,X_k))
   
    # Iterating through the queue and running revision algorithm
    while queue:
        (X_i, X_j) = queue.pop()
        domainSize = len(csp.curr_domains[X_i])
        if revise(csp, X_i, X_j):
            # Base case of 0 domain
            if domainSize == 0:
                return False
            else:
                for X_k in csp.neighbors[X_i]:
                    queue.append((X_k, X_i))
    return True
    
def revise(csp, X_i, X_j):
    revised = False
    
    removals = list()
    for x in csp.curr_domains[X_i]:
        if all(not csp.constraints(X_i, x, X_j, y) for y in csp.curr_domains[X_j]):
            csp.prune(X_i, x, removals)
            revised = True
    
    return revised
    