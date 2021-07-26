# sudoku

python script that solves and generates sudoku.

=========================

```py
from sudoku.solvers import BackTrackSolver
from sudoku.grid import generate, sample_grids, Grid

puzzle = generate()
# or to test: puzzle = Grid(sample_grids[0])
solver = BackTrackSolver()
solver.solve(puzzle)


array([[6, 7, 5, 9, 1, 2, 8, 4, 3],
       [1, 9, 3, 8, 4, 5, 6, 2, 7],
       [2, 4, 8, 7, 3, 6, 5, 1, 9],
       [8, 2, 4, 1, 6, 9, 3, 7, 5],
       [3, 6, 9, 2, 5, 7, 1, 8, 4],
       [5, 1, 7, 3, 8, 4, 9, 6, 2],
       [4, 8, 2, 6, 9, 3, 7, 5, 1],
       [7, 3, 1, 5, 2, 8, 4, 9, 6],
       [9, 5, 6, 4, 7, 1, 2, 3, 8]])

```

