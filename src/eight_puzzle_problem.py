from simpleai.search import SearchProblem
from src.puzzle_representation import PuzzleRepresentation

GOAL = '''1-2-3
4-5-6
7-8-*'''

goal_positions = {'1': (0, 0), '2': (0, 1), '3': (0, 2),
                  '4': (1, 0), '5': (1, 1), '6': (1, 2),
                  '7': (2, 0), '8': (2, 1), '*': (2, 2)}

class EightPuzzleProblem(SearchProblem):
    def actions(self, state):
        '''Returns a list of the pieces we can move to the empty space.'''

        rows = PuzzleRepresentation.string_to_list(state)
        row_e, col_e = PuzzleRepresentation.find_location(rows, '*')

        actions = []
        if row_e > 0:
            actions.append(rows[row_e - 1][col_e])
        if row_e < 2:
            actions.append(rows[row_e + 1][col_e])
        if col_e > 0:
            actions.append(rows[row_e][col_e - 1])
        if col_e < 2:
            actions.append(rows[row_e][col_e + 1])

        return actions

    def result(self, state, action):
        '''Return the resulting state after moving a piece to the empty space.
           (the "action" parameter contains the piece to move)
        '''

        rows = PuzzleRepresentation.string_to_list(state)
        row_e, col_e = PuzzleRepresentation.find_location(rows, '*')
        row_n, col_n = PuzzleRepresentation.find_location(rows, action)

        rows[row_e][col_e], rows[row_n][col_n] = rows[row_n][col_n], rows[row_e][col_e]

        return PuzzleRepresentation.list_to_string(rows)

    def is_goal(self, state):
        '''Returns true if a state is the goal state.'''

        return state == GOAL

    def cost(self, state1, action, state2):
        '''Returns the cost of performing an action. No useful on this problem, i
           but needed.
        '''

        return 1

    def heuristic(self, state):
        '''Returns an *estimation* of the distance from a state to the goal.
           We are using the manhattan distance.
        '''

        rows = PuzzleRepresentation.string_to_list(state)

        distance = 0

        for number in '12345678*':
            row_n, col_n = PuzzleRepresentation.find_location(rows, number)
            row_n_goal, col_n_goal = goal_positions[number]

            distance += abs(row_n - row_n_goal) + abs(col_n - col_n_goal)

        return distance
