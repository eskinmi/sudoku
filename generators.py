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

    def random_unit_generate(self):
        x,y = random.choice(self.solver.empty_boxes(self))
        values = self.solver.possible_values(self, x, y)
        if values:
            self.insert(random.choice(values), x, y)
        else:
            self.revert_step()

    def generate(self):
        i = 0
        n_elem = self.G.size
        for ix in range(n_elem):
            self.random_unit_generate()
            if i > 17: # minimum elements that can make a sudoku
                solutions = self.solver.find_all_solutions(self, max_solutions=2)
                if len(solutions) == 1:
                    return Grid(self.G.tolist())