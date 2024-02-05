# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *

def binary_ne_grid(cagey_grid):
    n, _ = cagey_grid  # Ignore the cages for this model, just use the grid size
    csp = CSP("binary_ne_grid")  # Initialize the CSP
    var_array = []
    # Create a variable for each cell in the grid, with domain 1 to n
    cell_array = [[f'Cell({i},{j})' for j in range(n)] for i in range(n)]
    for cell in cell_array:
        for i in cell:  
            i = Variable(i, [1,2,3,4,5,6,7,8,9])
            var_array.append(i)
    # Constraint creation
    column_constraint = Constraint("Column_constraint", var_array)
    row_constraint = Constraint("Row_constraint", var_array)
    return csp, var_array

def nary_ad_grid(cagey_grid):
    n, cages = cagey_grid
    csp = CSP("nary_ad_grid")
    
    # Create variables for the grid
    var_array = []
    variables = []  # To keep a linear list of variables for easy access

    for i in range(n):
        row = []
        for j in range(n):
            # Create a variable for each cell with a domain from 1 to n
            variable = Variable(domain=list(range(1, n+1)))
            row.append(variable)
            variables.append(variable)  # Add to the linear list of variables
        var_array.append(row)
        
   # Adding n-ary all-different constraints for each row
    for i in range(n):
        row_vars = var_array[i]
        # Assuming add_all_diff_constraint is a method to add an all-different constraint
        # for a list of variables. Replace with your actual method as necessary.
        csp.add_all_diff_constraint(row_vars)
    
    # Adding n-ary all-different constraints for each column
    for j in range(n):
        col_vars = [var_array[i][j] for i in range(n)]
        csp.add_all_diff_constraint(col_vars)
        
    return csp, var_array

def cagey_csp_model(cagey_grid):
    csp, variables = binary_ne_grid(cagey_grid)
    
    pass
