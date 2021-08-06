# sudoku

This package generates and solves **Sudoku**.

=========================

```py
from sudoku import grid
from sudoku.solvers import BackTrackSolver

pzl = grid.generate(difficulty=0.5)
solver = BackTrackSolver(grid)
solver.run()

# === or ===

from sudoku.solvers import LPSolver
from sudoku import Grid

puzzle = [
[[[0, 0, 0], [6, 9, 1], [0, 2, 0]], [[5, 0, 0], [0, 8, 0], [0, 0, 6]], [[0, 3, 0], [4, 5, 7], [0, 0, 0]]],
[[[0, 0, 6], [0, 3, 0], [7, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 9], [0, 6, 0], [3, 0, 0]]],
[[[0, 0, 0], [4, 1, 7], [0, 8, 0]], [[1, 0, 0], [0, 6, 0], [0, 0, 3]], [[0, 2, 0], [9, 8, 3], [0, 0, 0]]]
       ]      
pzl = Grid(puzzle)
solver = LPSolver(pzl)
solver.run()
  

```



