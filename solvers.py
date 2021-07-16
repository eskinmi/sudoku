import numpy as np
import itertools

class BackTrackSolver:

    def __init__(self, max_depth=0):
        self.true_serie = np.arange(1, 10, 1)
        self.inserted = {}
        self.n_depth = 0
        self.max_depth = max_depth


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

    def possible_values(self, row, col, square):
        return [i for i in self.true_serie if i not in col if i not in row if i not in square and i != 0]

    def solve(self, puzzle):
        self.n_depth += 1
        if self.max_depth and self.n_depth > self.max_depth:
            print('max recursion depth is reached!')
            return puzzle
        empty_boxes = self.empty_boxes(puzzle)
        if not empty_boxes:
            return puzzle
        else:
            box = empty_boxes[0]
            x, y = box[0], box[1]
            squ = self.find_square(puzzle, x, y)
            possible_vals = self.possible_values(puzzle.rows[x], puzzle.cols[y], squ)
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
                    self.insert(0, x, y)
            return False
