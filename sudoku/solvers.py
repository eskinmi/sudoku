import numpy as np
import itertools
import uuid
import pulp as lp


class BackTrackSolver:

    def __init__(self, puzzle, max_depth=0):
        self.puzzle = puzzle
        self.true_serie = np.arange(1, 10, 1)
        self.inserted = dict()
        self.inserted[puzzle] = dict()
        self.n_depth = 0
        self.max_depth = max_depth
        self.change_selection_order = False

    def test(self):
        for ele in [self.puzzle.rows, self.puzzle.cols, self.puzzle.squares]:
            for x in ele:
                vals = [i for i in x.flatten() if i != 0]
                if not len(set(vals)) == len(list(vals)):
                    return False
        return True

    def empty_boxes(self):
        # sort this to make the solver faster.
        # sorting is based on the least amount of possibilities.
        return sorted([[x, y] for x, y in itertools.product(range(9), range(9))
                       if self.puzzle.rows[x][y] == 0])

    def possible_values(self, x, y):
        if self.change_selection_order:
            inserted_to_index = [val for indices, val in self.inserted[self.puzzle].items()
                                 if f'{x}-{y}' in indices]
            val_rank = inserted_to_index[0] if inserted_to_index else 0
            true_serie = np.roll(self.true_serie, 9-val_rank)
        else:
            true_serie = self.true_serie
        values = [i for i in true_serie
                  if i not in self.puzzle.cols[y]
                  if i not in self.puzzle.rows[x]
                  if i not in self.puzzle.find_square(x, y)
                  if i != 0]
        return values

    def run(self):
        self.n_depth += 1
        if self.max_depth and self.n_depth > self.max_depth:
            print('max recursion depth is reached!')
            return self.puzzle
        boxes = self.empty_boxes()
        if not boxes:
            return self.puzzle
        else:
            box = boxes[0]
            x, y = box[0], box[1]
            possible_vals = self.possible_values(x, y)
            # print(possible_vals)
            for val in possible_vals:
                self.puzzle.insert(val, x, y)
                if self.test():
                    self.inserted[self.puzzle][f'{x}-{y}'] = val
                    solved_puzzle = self.run()
                    if solved_puzzle:
                        return solved_puzzle
                    else:
                        self.puzzle.delete(x, y)
                else:
                    self.puzzle.insert(0, x, y)
            return False

    def find_all_solutions(self, max_solutions=5):
        self.change_selection_order = True
        solutions = []
        # add already tried solutions to the possible solutions
        run = True
        while run:
            sol = self.run()
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
        self.change_selection_order = False
        return solutions


class LPSolver:

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.values = range(1, 10)
        self.indices = range(0, 9)
        self.problem_id = uuid.uuid4().hex
        self.pr = lp.LpProblem(self.problem_id)
        self._set_pseudo_objective()
        self.vars = self._define_vars()
        self._set_constraints()

    def _set_pseudo_objective(self):
        return self.pr.setObjective(lp.lpSum(0))

    def _define_vars(self):
        return lp.LpVariable.dicts("x_cell", (self.indices, self.indices, self.values), cat='Binary')

    def _set_constraints(self):
        for row in self.indices:
            for col in self.indices:
                self.pr.addConstraint(lp.LpConstraint(
                    e=lp.lpSum([self.vars[row][col][value] for value in self.values]),
                    sense=lp.LpConstraintEQ,
                    rhs=1,
                    name=f"constraint_sum_{row}_{col}"))

        # CONSTRAINT 2: Constraint to ensure that values from 1 to 9 is filled only once in a row
        for row in self.indices:
            for value in self.values:
                self.pr.addConstraint(lp.LpConstraint(
                    e=lp.lpSum([self.vars[row][col][value] * value for col in self.indices]),
                    sense=lp.LpConstraintEQ,
                    rhs=value,
                    name=f"constraint_unique_row_{row}_{value}"))

        # CONSTRAINT 3: Constraint to ensure that values from 1 to 9 is filled only once in a column
        for col in self.indices:
            for value in self.values:
                self.pr.addConstraint(lp.LpConstraint(
                    e=lp.lpSum([self.vars[row][col][value] * value for row in self.indices]),
                    sense=lp.LpConstraintEQ, rhs=value,
                    name=f"constraint_unique_col_{col}_{value}"))

        # CONSTRAINT 4: Constraint to ensure that values from 1 to 9 is filled only once in the 3x3 grid
        for grid in self.indices:
            grid_row = int(grid / 3)
            grid_col = int(grid % 3)

            for value in self.values:
                self.pr.addConstraint(lp.LpConstraint(
                    e=lp.lpSum([self.vars[grid_row * 3 + row][grid_col * 3 + col][value] * value
                                for col in range(0, 3) for row in range(0, 3)]),
                    sense=lp.LpConstraintEQ, rhs=value,
                    name=f"constraint_unique_grid_{grid}_{value}"))

        # Fill the prefilled values from input sudoku as constraints
        for row in self.indices:
            for col in self.indices:
                if self.puzzle.rows[row][col] != 0:
                    self.pr.addConstraint(
                        lp.LpConstraint(e=lp.lpSum([self.vars[row][col][value] * value for value in self.values]),
                                        sense=lp.LpConstraintEQ,
                                        rhs=self.puzzle.rows[row][col],
                                        name=f"constraint_pre_filled_{row}_{col}"))

    def run(self):
        self.pr.solve()
        for row in self.indices:
            for col in self.indices:
                for value in self.values:
                    if lp.value(self.vars[row][col][value]):
                        self.puzzle.insert(value, row, col)
        return self.puzzle


