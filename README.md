# sudoku

python script that solves and generates sudoku.

=========================

```py
from solvers import BackTrackSolver
from grid import generate, sample_grids, Grid

puzzle = generate()
# or to test: puzzle = Grid(sample_grids[0])
solver = BackTrackSolver()
solver.solve(puzzle)


# +-------+-------+-------+
# | 4 1   | 3     | 7 6   |
# |   9 3 |   7   | 4   1 |
# | 2     | 1 4   |   8 3 |
# +-------+-------+-------+
# | 9 5 8 |       |     7 |
# | 3 4   |     7 |   1   |
# |   7 2 | 8 9 3 | 5 4   |
# +-------+-------+-------+
# |   8   | 2     | 3 7 4 |
# |     4 |       | 1 9 5 |
# |       |   5   | 6     |
# +-------+-------+-------+

```

