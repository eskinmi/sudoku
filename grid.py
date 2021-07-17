import numpy as np


class Grid:

    def __init__(self, original_grid):
        self.original_grid = original_grid
        self.G = np.array(self.original_grid)

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

    def reset_grid(self, grid):
        self.__init__(grid)


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
    ]
]
