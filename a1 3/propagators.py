# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    if newVar == None:
        pass
    else:


        pruned = []  # To keep track of pruned values

        # This is for checking constraints with exactly one variable in their scope
        # that is unassigned
        have_newVar = csp.get_cons_with_var(newVar)
        # Iterate through constraints and check if they only have one unasigned var
        for const in have_newVar:
            if const.get_n_unasgn() == 1:
                scope = const.get_scope()
                #prune = []
                # Scopes seem to be rows and columns, and the same num can't appear
                # twice, so prune any numbers that are in same row / col
                for var in scope:
                    if var.is_assigned():
                        pruned.append(var.get_assigned_value())
                    else: 
                        # Just doing this so I know where in the list the unassigned var is
                        # Shit ass code lol
                        scope.remove(var)
                        scope.append(var)
                for p in pruned:
                    scope[-1].prune_value(p)


'''
def prop_FC(csp, newVar=None):
    pruned = []  # To keep track of pruned values

    if newVar is None:
        # For forward checking, if no variable is newly instantiated, no action is needed
        return True, pruned

    # Get constraints involving the newly instantiated variable
    constraints = csp.get_cons_with_var(newVar)
    for const in constraints:
        # Proceed only if there's exactly one unassigned variable in the constraint
        if const.get_n_unasgn() == 1:
            unasgn_var = const.get_unasgn_vars()[0]  # The unassigned variable in the constraint
            for val in unasgn_var.cur_domain():
                # Temporarily assign the value to check constraint satisfaction
                unasgn_var.assign(val)
                if not const.check():  # Check the constraint with this temporary assignment
                    unasgn_var.prune_value(val)  # Prune if the constraint is not satisfied
                    pruned.append((unasgn_var, val))  # Keep track of pruned values
                unasgn_var.unassign()  # Undo the temporary assignment
            if unasgn_var.cur_domain_size() == 0:
                return False, pruned  # Failure if the domain is empty

    return True, pruned
'''



def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    if newVar == None:
        pass
    else:
        have_newVar = csp.get_cons_with_var(newVar)
        print(have_newVar)

