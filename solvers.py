import numpy as np
import itertools
from grid import Grid


class BackTrackSolver(Grid):

    def __init__(self, max_depth=0):
        self.true_serie = np.arange(1, 10, 1)
        self.inserted = {}
        self.n_depth = 0
        self.max_depth = max_depth
        self.change_selection_order = False

    @staticmethod
    def test(puzzle):
        for ele in [puzzle.rows, puzzle.cols, puzzle.squares]:
            for x in ele:
                vals = [i for i in x.flatten() if i != 0]
                if not len(set(vals)) == len(list(vals)):
                    return False
        return True

    @staticmethod
    def empty_boxes(puzzle):
        # sort this to make the solver faster.
        # sorting is based on the least amount of possibilities.
        return sorted([[x, y] for x, y in itertools.product(range(9), range(9))
                       if puzzle.rows[x][y] == 0])

    def possible_values(self, puzzle, x, y):
        if self.change_selection_order:
            inserted_to_index = [val for indices,val in self.inserted[puzzle].items()
                                 if f'{x}-{y}' in indices]
            val_rank = inserted_to_index[0] if inserted_to_index else 0
            true_serie = np.roll(self.true_serie, 9-val_rank)
        else:
            true_serie = self.true_serie
        values = [i for i in true_serie
                         if i not in puzzle.cols[y]
                         if i not in puzzle.rows[x]
                         if i not in puzzle.find_square(x, y)
                         if i != 0]
        return values

    def solve(self, puzzle):
        super().__init__(puzzle)
        if puzzle not in self.inserted:
            self.inserted[puzzle] = dict()
        self.n_depth += 1
        if self.max_depth and self.n_depth > self.max_depth:
            print('max recursion depth is reached!')
            return puzzle
        boxes = self.empty_boxes(puzzle)
        if not boxes:
            return puzzle
        else:
            box = boxes[0]
            x, y = box[0], box[1]
            possible_vals = self.possible_values(puzzle, x, y)
            # print(possible_vals)
            for val in possible_vals:
                puzzle.insert(val, x, y)
                if self.test(puzzle):
                    self.inserted[puzzle][f'{x}-{y}'] = val
                    solved_puzzle = self.solve(puzzle)
                    if solved_puzzle:
                        return solved_puzzle
                    else:
                        puzzle.delete(x, y)
                else:
                    puzzle.insert(0, x, y)
            return False

    def find_all_solutions(self, puzzle, max_solutions=5):
        self.change_selection_order = True
        solutions = []
        # add already tried solutions to the possible solutions
        run = True
        while run:
            sol = self.solve(puzzle)
            if sol:
                if solutions and (sol.G == np.array([s.G for s in solutions])).all(axis=1).any():
                    # if solution is already found
                    run = False
                else:
                    solutions.append(sol)
                if len(solutions) >= max_solutions:
                    run = False
            else:
                run = False
        self.inserted = {}
        self.change_selection_order = False
        return solutions
