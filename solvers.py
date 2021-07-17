import numpy as np
import itertools


class BackTrackSolver:

    def __init__(self, max_depth=0):
        self.true_serie = np.arange(1, 10, 1)
        self.inserted = {}
        self.n_depth = 0
        self.max_depth = max_depth
        self.puzzle = None

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
        return sorted([[x, y] for x, y in itertools.product(range(9), range(9))
                       if puzzle.rows[x][y] == 0])

    @staticmethod
    def find_square(puzzle, x, y):
        return puzzle.squares[int(np.floor(x / 3) * 3 + np.floor(y / 3))]

    def possible_values(self, puzzle, x, y):
        return [i for i in self.true_serie
                if i not in puzzle.cols[y]
                if i not in puzzle.rows[x]
                if i not in self.find_square(puzzle, x, y)
                if i != 0]

    def solve(self, puzzle):
        self.n_depth += 1
        if self.max_depth and self.n_depth > self.max_depth:
            print('max recursion depth is reached!')
            return puzzle
        boxes = self.empty_boxes(puzzle)
        if not boxes:
            self.puzzle = puzzle
            return puzzle
        else:
            box = boxes[0]
            x, y = box[0], box[1]
            possible_vals = self.possible_values(puzzle, x, y)
            for val in possible_vals:
                puzzle.insert(val, x, y)
                if self.test(puzzle):
                    self.inserted[f'{x}-{y}'] = val
                    solved_puzzle = self.solve(puzzle)
                    if solved_puzzle:
                        return solved_puzzle
                    else:
                        puzzle.delete(x, y)
                else:
                    puzzle.insert(0, x, y)
            return False

    @staticmethod
    def _grid_in_solutions(grid, grids):
        return (grid == grids).all(axis=1).any()

    def find_all_solutions(self, puzzle, max_solutions=5):
        solutions = []
        # add already tried solutions to the possible solutions
        run = True
        while run:
            sol = self.solve(puzzle)
            if solution:
                if self._grid_in_solutions(sol.G, np.array(solutions)):
                    run = False
                else:
                    solutions.append(sol.G)
                if len(solutions) >= max_solutions:
                    run = False
            else:
                run = False
        return solutions
