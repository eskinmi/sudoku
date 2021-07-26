import numpy as np
import random
from sudoku.solvers import BackTrackSolver


class Grid(BackTrackSolver):

    def __init__(self, original_grid):
        self.original_grid = original_grid
        self.G = np.array(self.original_grid)
        super().__init__(self)

    @property
    def rows(self):
        return self.G.swapaxes(1, 2).reshape(9, 9)

    @property
    def cols(self):
        return self.rows.T

    @property
    def squares(self):
        return self.G.reshape((9, 3, 3))

    def insert(self, element, x, y):
        self.G[int(np.floor(x / 3))][int(np.floor(y / 3))][x % 3][y % 3] = element

    def delete(self, x, y):
        self.G[int(np.floor(x / 3))][int(np.floor(y / 3))][x % 3][y % 3] = 0

    def find_square(self, x, y):
        return self.squares[int(np.floor(x / 3) * 3 + np.floor(y / 3))]

    def reset_grid(self, grid=None):
        if not grid:
            grid = self.original_grid
        self.G = np.array(grid)


def make_empty_grid():
    """
    Make empty grid.
        np.zeros
    :return:
        list (3,3,3,3)
    """
    return np.zeros((3, 3, 3, 3), dtype='int64').tolist()


def generate(difficulty:float = None):
    """
    Generate random Sudoku grid.
        :param difficulty: difficulty level (float)
    :return:
        grid.Grid
    """
    if difficulty is None:
        n_rounds = random.choice(range(17, 81))
        _test_start = random.choice(range(17, n_rounds+1))
    elif difficulty == 0:
        n_rounds = random.choice(range(36, 81))
        _test_start = random.choice(range(36, n_rounds+1))
    else:
        n_rounds = random.choice(range(17, 36-int(18*difficulty)))
        _test_start = random.choice(range(17, n_rounds+1))

    empty_grid = make_empty_grid()
    pzl = Grid(empty_grid)
    x_prev, y_prev = None, None
    for ix in range(n_rounds):
        x, y = random.choice(pzl.empty_boxes())
        values = pzl.possible_values(x, y)
        if values:
            pzl.insert(random.choice(values), x, y)
        else:
            pzl.delete(x_prev, y_prev)
            return Grid(pzl.G.tolist())
        x_prev, y_prev = x, y
        grid = pzl.G.tolist()
        if ix >= _test_start:
            # print('searching for solutions...')
            sol = pzl.solve()
            pzl.reset_grid(grid)
            if not sol:
                pzl.delete(x_prev, y_prev)
    return Grid(pzl.G.tolist())


sample_grids = [
    [
        [[[0, 0, 5], [0, 9, 0], [2, 0, 0]], [[0, 1, 0], [8, 0, 0], [0, 0, 6]], [[8, 0, 0], [0, 2, 0], [0, 0, 9]]],
        [[[0, 0, 4], [3, 0, 0], [0, 1, 0]], [[0, 0, 0], [0, 5, 0], [0, 0, 0]], [[0, 7, 0], [0, 0, 4], [9, 0, 0]]],
        [[[4, 0, 0], [0, 3, 0], [0, 0, 6]], [[6, 0, 0], [0, 0, 8], [0, 7, 0]], [[0, 0, 1], [0, 9, 0], [2, 0, 0]]]
    ],
    [
        [[[6, 0, 0], [0, 9, 0], [0, 0, 4]], [[0, 8, 0], [0, 0, 0], [0, 2, 0]], [[0, 0, 3], [0, 1, 0], [5, 0, 0]]],
        [[[0, 0, 0], [7, 0, 5], [0, 0, 0]], [[3, 0, 2], [0, 9, 0], [6, 0, 7]], [[0, 0, 0], [4, 0, 6], [0, 0, 0]]],
        [[[0, 0, 3], [0, 8, 0], [9, 0, 0]], [[0, 7, 0], [0, 0, 0], [0, 3, 0]], [[1, 0, 0], [0, 5, 0], [0, 0, 8]]]
    ],
    [
        [[[2, 9, 5], [4, 3, 1], [8, 7, 6]], [[7, 4, 3], [8, 6, 5], [1, 9, 2]], [[8, 6, 1], [9, 0, 0], [5, 4, 3]]],
        [[[3, 8, 7], [6, 1, 2], [5, 4, 9]], [[4, 5, 9], [3, 8, 7], [2, 1, 6]], [[2, 1, 6], [4, 9, 5], [7, 3, 8]]],
        [[[7, 6, 3], [9, 2, 8], [1, 5, 4]], [[5, 2, 4], [6, 7, 1], [9, 3, 8]], [[1, 8, 9], [3, 5, 4], [6, 0, 0]]]
    ],
    [
        [[[0, 0, 0], [6, 9, 1], [0, 2, 0]], [[5, 0, 0], [0, 8, 0], [0, 0, 6]], [[0, 3, 0], [4, 5, 7], [0, 0, 0]]],
        [[[0, 0, 6], [0, 3, 0], [7, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 9], [0, 6, 0], [3, 0, 0]]],
        [[[0, 0, 0], [4, 1, 7], [0, 8, 0]], [[1, 0, 0], [0, 6, 0], [0, 0, 3]], [[0, 2, 0], [9, 8, 3], [0, 0, 0]]]
    ]
]
