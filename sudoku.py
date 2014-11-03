import numpy as np

try:
    __import__('imp').find_module('constraint')
    from constraint import *
except ImportError:
    print('Please Install Python-constraint package')
    raise

class sudoku():

    def __init__(self, problem_string):
        '''given a problem (1xN numerical string), initialize with conversion into a numerical array'''
        #print "in sudoku init"
        self.problem = np.array(map(int,list(problem_string)))

    def solve(self):
        '''solve the given problem with constraint formulation'''
        n = int(np.sqrt(self.problem.shape[0]))
        r = np.arange(0, n, step=1)
        c = np.arange(0,n, step=1)

        #initialize a constraint problem
        sudoku = Problem()

        #create sudoku coordinates, and added as constraint variables
        entries = [(i,j) for i in r for j in c]
        sudoku.addVariables(entries, range(1, n**2+1))

        #constrain: all variables can only take 1-9
        sudoku.addConstraint(InSetConstraint(r+1))

        #constrain: all elements in a row differ
        for row in r:
            row_entry = [(row, col) for col in c]
            sudoku.addConstraint(AllDifferentConstraint(), row_entry)

        #constrain: all elements in a column differ
        for col in c:
            col_entry = [(row, col) for row in r]
            sudoku.addConstraint(AllDifferentConstraint(), col_entry)

        #constrain: non-zero entry is constrained by a corresponding given value
        values = self.problem.reshape(-1)
        for ind, entry in enumerate(entries):
            if values[ind] > 0:
                sudoku.addConstraint(lambda var, val=values[ind]: var == val, (entry,))
            else:
                pass

        #constrain: within a block (for 9x9 sudoku, the block is 3x3), all elements differ
        jump = int(np.sqrt(n))
        for i in np.arange(0,n,jump):
            rows = np.arange(i, i+jump)
            for j in np.arange(0,n,jump):
                cols = np.arange(j, j+jump)
                block = [(row, col) for row in rows for col in cols]
                sudoku.addConstraint(AllDifferentConstraint(), block)

        #Solve the constrained problem
        self.solution = sudoku.getSolution()

        #convert self.solution to an appropriate format for Gui.py to use
        if self.solution is not None:
            self.solution = str([self.solution[i] for i in sorted(self.solution)])
            self.solution = self.solution.translate(None,"'[],.:")
            self.solution = ''.join(self.solution.split())
        else:
            self.solution = None

        return self.solution





