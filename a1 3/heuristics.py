# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    # IMPLEMENT
    pass

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # Returns the variable with the most constrained legal domain
    # Get all variables
    all_vars = csp.get_all_vars()
    most_constrained = None
    domain_size = 100000
    # Iterate through variables checking current domain size
    # Return variable with smallest domain
    for var in all_vars:
        if var.cur_domain_size() < domain_size:
            most_constrained = var
    return most_constrained

