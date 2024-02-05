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

import itertools
from cspbase import *

def binary_ne_grid(cagey_grid):
    n, _ = cagey_grid  # Ignore the cages for this model, just use the grid size
    csp = CSP("binary_ne_grid")  # Initialize the CSP
     # Initialize variables with domains from 1 to n and add them to CSP
    var_array = []  # This will store Variable objects
    for row in range(n):
        for col in range(n):
            var_name = f"cell{row}{col}"
            var = Variable(var_name, list(range(1, n + 1)))
            csp.add_var(var)  # Correct method to add variables to CSP
            var_array.append(var)  # Store Variable objects, not names

    # Add binary not-equal constraints between all pairs of cells in the same row and column
    for i in range(n):
        for j in range(n):
            # Row constraints
            for k in range(n):
                if k != j:  # Ensure we're not comparing a cell with itself
                    var1 = var_array[i * n + j]
                    var2 = var_array[i * n + k]
                    con = Constraint(f"Row{i}_{j}ne{i}{k}", [var1, var2])
                    tuples = [(x, y) for x in range(1, n + 1) for y in range(1, n + 1) if x != y]
                    con.add_satisfying_tuples(tuples)
                    csp.add_constraint(con)
            # Column constraints
            for k in range(n):
                if k != i:  # Ensure we're not comparing a cell with itself
                    var1 = var_array[i * n + j]
                    var2 = var_array[k * n + j]
                    con = Constraint(f"Col{j}_{i}ne{j}_{k}", [var1, var2])
                    tuples = [(x, y) for x in range(1, n + 1) for y in range(1, n + 1) if x != y]
                    con.add_satisfying_tuples(tuples)
                    csp.add_constraint(con)
    return csp, var_array

def nary_ad_grid(cagey_grid):
    n, _ = cagey_grid  # Ignore the cages for this model, just use the grid size
    csp = CSP("nary_ne_grid")  # Initialize the CSP
     # Initialize variables with domains from 1 to n and add them to CSP
    var_array = []  # This will store Variable objects
    domains = [x for (x) in itertools.product(range(1,n+1), repeat=n)]
    mod_dom = []
    for dom in domains:
        if len(set(dom)) == len(dom):
            mod_dom.append(dom)

    rowList = []
    for row in range(n):
        cur_row = []
        for col in range(n):
            var_name = f"cell{row}{col}"
            var = Variable(var_name, list(range(1, n + 1)))
            csp.add_var(var)  # Correct method to add variables to CSP
            cur_row.append(var)  # Store Variable objects, not names
            var_array.append(var)
        rowList.append(cur_row)

    for row in rowList:
        con = Constraint("Row", row)
        con.add_satisfying_tuples(mod_dom)
        csp.add_constraint(con)
    
    colLists = []
    for i in range(n):
        col = []
        for j in range(n):
            col.append(rowList[j][i])
        colLists.append(col)
    
    for col in colLists:
        con = Constraint("Col", col)
        con.add_satisfying_tuples(mod_dom)
        csp.add_constraint(con)

    return csp, var_array


def cagey_csp_model(cagey_grid):
    csp, variables = binary_ne_grid(cagey_grid)
    
    pass
