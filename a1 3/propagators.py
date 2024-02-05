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
    prune_list = []
    final_bool = True
    if newVar != None:
        domainVals = newVar.cur_domain() #get the current domain (this domain contains all the previously pruned values for newVar)
        constraints = csp.get_cons_with_var(newVar) #get all constraints for newVar
        for constraint in constraints: #loop through all constraints
            temp_bool = False #set temp_bool to false with every constraint checked, only switch it to true if a domain value satisifies the constraint
            for val in domainVals: #loop through domain on newVar
                check = constraint.check_var_val(newVar, val) #check that the constraint still holds if newVar is equal to val 
                if check == False: #if domain value breaks constraint, add to prune list
                    if (newVar, val) not in prune_list: #check if variable-val pair is already in prune list
                        newVar.prune_value(val)
                        prune_list.append((newVar, val)) #add (variable,val) tuple to prune list
                else:
                    temp_bool = True #at least one domain value satisfies the constraint
            if temp_bool == False:#if no domain satifies any of the constraint, then the variable is at a deadend
                final_bool = False
        return final_bool, prune_list
    else:
        #this section creates a prune list on all unassigned variable in a constraints scope. It does this for each constraint.
        #I return true because im hoping that the profs algorithm only calls propagator functions with newVar=None when the program first starts running lol
        constraints = csp.get_all_cons()
        for constraint in constraints:
            if constraint.get_n_unasgn() > 0:
                unasgn_list = constraint.get_unasgn_vars()
                for var in unasgn_list:
                    domainVals = var.cur_domain()
                    for val in domainVals:
                        check = constraint.check_var_val(var, val)
                        if check == False:
                            if (var, val) not in prune_list:
                                var.prune_value(val)
                                prune_list.append((var, val))
        return True, prune_list
    




def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    if newVar == None:
       constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)

    prune_list = []
    while constraints:
        for constraint in constraints:
            if constraint.get_n_unasgn() > 0:
                unasgn_list = constraint.get_unasgn_vars()
                for var in unasgn_list:
                    domainVals = var.cur_domain()
                    for val in domainVals:
                        check = constraint.check_var_val(var, val)
                        if check == False:
                            if (var, val) not in prune_list:
                                var.prune_value(val)
                                prune_list.append((var, val))
        return True, prune_list


