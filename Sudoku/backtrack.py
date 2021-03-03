"""
    Nam Tran
    CS550 A05
    
    constraint_prop.py contains the functions required to use the 
      Backtracking Search algorithm.
"""

from csp_lib.backtrack_util import (first_unassigned_variable, 
                                    unordered_domain_values,
                                    no_inference)

def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """backtracking_search
    Given a constraint satisfaction problem (CSP),
    a function handle for selecting variables, 
    a function handle for selecting elements of a domain,
    and a set of inferences, solve the CSP using backtrack search
    """
    
    # See Figure 6.5] of your book for details

    def backtrack(assignment):
        """Attempt to backtrack search with current assignment
        Returns None if there is no solution.  Otherwise, the
        csp should be in a goal state.
        """
        # Base case all variables assigned
        if (len(assignment) == len(csp.variables)):
            return assignment
        
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            csp.assign(var, value, assignment)
            removals = csp.suppose(var, value)
            
            if (csp.nconflicts(var, value, assignment) == 0):
                inferences = inference(csp, var, value, assignment, removals)
                
                if (inferences == True):
                    result = backtrack(assignment)
                    
                    if (result != None):
                        return result
            csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    # Call with empty assignments, variables accessed
    # through dynamic scoping (variables in outer
    # scope can be accessed in Python)
    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result
