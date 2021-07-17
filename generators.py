import numpy as np
from grid import Grid
from solvers import BackTrackSolver
import random


class GridGen(Grid):

    def __init__(self):
        super().__init__(self._mk_empty_grid())
        self.solver = BackTrackSolver()

    @staticmethod
    def _mk_empty_grid():
        return np.zeros((3, 3, 3, 3), dtype='int64').tolist()

    def unit_generate(self):
        x,y = random.choice(self.solver.empty_boxes(self))
        row = self.rows[x]
        col = self.cols[y]
        squ = self.solver.find_square(self, x, y)
        values = self.solver.possible_values(row, col, squ)
        self.insert(random.choice(values), x, y)

    def generate(self):
        for ix in range(5):
            self.unit_generate()
            # if ix > 9:
                # if self.solver.has_single_solution(self):
                #     return Grid(self.G.tolist())