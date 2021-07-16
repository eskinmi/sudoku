import numpy as np

class Grid:

    def __init__(self, original_grid):
        self.original_grid = original_grid
        self.G = np.array(self.original_grid)

    def test(self):
        for ele in [self.rows, self.cols, self.squares]:
            for x in ele:
                vals = [i for i in x.flatten() if i != 0]
                if not len(set(vals)) == len(list(vals)):
                    return False
                else:
                    return True

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



