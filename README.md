# sudoku

python script that solves and generates sudoku.

=========================

```py
from sudoku import grid

pzl = grid.generate()
pzl.solve()

# === or ===

from sudoku import grid

sample_grid = grid.sample_grids[1]
pzl = grid.Grid(sample_grid)
pzl.solve()

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

