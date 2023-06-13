'''
8 puzzle problem, a smaller version of the fifteen puzzle:
http://en.wikipedia.org/wiki/Fifteen_puzzle
States are defined as string representations of the pieces on the puzzle.
Actions denote what piece will be moved to the empty space.

States must allways be inmutable. We will use strings, but internally most of
the time we will convert those strings to lists, which are easier to handle.
For example, the state (string):

'1-2-3
 4-5-6
 7-8-*'

will become (in lists):

[['1', '2', '3'],
 ['4', '5', '6'],
 ['7', '8', '*']]

'''

from __future__ import print_function

from simpleai.search import SearchProblem
from simpleai.search.traditional import astar, uniform_cost
from simpleai.search.local import beam, beam_best_first
from simpleai.search.viewers import WebViewer
import time
import re

# Error classes


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidFormatException(Error):
    """Exception raised for errors in the 8-puzzle input format"""
    pass


GOAL = '''1-2-3
4-5-6
7-8-*'''


# turn list into a string and append dashes between tiles
def list_to_string(list_):
    return '\n'.join(['-'.join(row) for row in list_])

# turn string into list and split the tiles on dashes


def string_to_list(string_):
    return [row.split('-') for row in string_.split('\n')]


def find_location(rows, element_to_find):
    '''Find the location of a piece in the puzzle.
       Returns a tuple: row, column'''
    for ir, row in enumerate(rows):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic


# we create a cache for the goal position of each piece, so we don't have to
# recalculate them every time
goal_positions = {}
rows_goal = string_to_list(GOAL)
for number in '12345678*':
    goal_positions[number] = find_location(rows_goal, number)


class EightPuzzleProblem(SearchProblem):
    def actions(self, state):
        '''Returns a list of the pieces we can move to the empty space.'''
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, '*')

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
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, '*')
        row_n, col_n = find_location(rows, action)

        rows[row_e][col_e], rows[row_n][col_n] = rows[row_n][col_n], rows[row_e][col_e]

        return list_to_string(rows)

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
        rows = string_to_list(state)

        distance = 0

        for number in '12345678*':
            row_n, col_n = find_location(rows, number)
            row_n_goal, col_n_goal = goal_positions[number]

            distance += abs(row_n - row_n_goal) + abs(col_n - col_n_goal)

        return distance


# A utility function to count
# inversions in given array 'arr[]'
def getInvCount(tiles):

    inv_count = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if tiles[j] and tiles[i] and tiles[i] > tiles[j]:
                inv_count += 1

    return inv_count


# This function returns true
# if given 8 puzzle is solvable.
def isSolvable(puzzle):

    # Count inversions in given 8 puzzle
    invCount = getInvCount(puzzle)

    # return true if inversion count is even.
    return (invCount % 2 == 0)


while True:

    # .split(): split the input string into a list using a space as the separator
    row1 = row2 = row3 = ""
    try:
        print("******************************************************************************************************")
        print("*                                                                                                    *")
        print("*               AI PROGRAM TO SOLVE AN 8-PUZZLE GIVEN AN INITIAL STATE USING A* SEARCH               *")
        print("*                                                                                                    *")
        print("******************************************************************************************************")
        print("*                                                                                                    *")
        print("*      Instructions:                                                                                 *")
        print("*      -------------                                                                                 *")
        print("*                                                                                                    *")
        print("*           Enter the initial state of the 8-puzzle using the following format: ### #*# ###.         *")
        print("*                                                                                                    *")
        print("*           '#' represents a digit 1 - 8 and '*' represents the empty space.                         *")
        print("*                                                                                                    *")
        print("*           Digits cannot be repeated and the location of the '*' can be exchanged with the          *")
        print("*           location of any other '#'.                                                               *")
        print("*                                                                                                    *")
        print("*           For instance, if the 8-puzzle's initial state appears as follows:                        *")
        print("*                                                                                                    *")
        print("*             [ 7-3-2 ]                                                                              *")
        print("*             [ 5-*-1 ]                                                                              *")
        print("*             [ 8-6-4 ],                                                                             *")
        print("*                                                                                                    *")
        print("*           users should enter '732 5*1 864' at the prompt below so that each row is separated       *")
        print("*           by a space.                                                                              *")
        print("*                                                                                                    *")
        print("*           Next, press enter when done.                                                             *")
        print("*                                                                                                    *")
        print("******************************************************************************************************")
        print("*                                                                                                    *")
        print("*      Methods:                                                                                      *")
        print("*      --------                                                                                      *")
        print("*                                                                                                    *")
        print("*           The AI program uses the A* search to find the cost-optimal solution from the initial     *")
        print("*           state to the goal state if one exists.                                                   *")
        print("*                                                                                                    *")
        print("*           The following is the goal state of the 8-puzzle:                                         *")
        print("*                                                                                                    *")
        print("*             [ 1-2-3 ]                                                                              *")
        print("*             [ 4-5-6 ]                                                                              *")
        print("*             [ 7-8-* ]                                                                              *")
        print("*                                                                                                    *")
        print("*           If the user makes an error in input or the initial state is unsolvable, the program      *")
        print("*           notifies the user.  Otherwise, the program outputs the steps of the cost-optimal         *")
        print("*           solution.                                                                                *")
        print("*                                                                                                    *")
        print("******************************************************************************************************")
        print()
        row1, row2, row3 = input(
            "Please input the initial state of the 8-puzzle (e.g., ### #*# ###): ").split()
        concat = row1 + row2 + row3
        digitList = []
        if not re.match(r"(?!.*([1-8\*]).*\1)^[1-8\*]{9}$", concat):
            raise InvalidFormatException
        concatRepE = concat.replace("*", "0")
        for c in concatRepE:
            digitList.append(int(c))

        if (isSolvable(digitList)):
            list_2d = [digitList[i:i+3] for i in range(0, len(digitList), 3)]
            strConv = ''
            for row in list_2d:
                for n in range(len(row)):
                    strConv += str(row[n])
                    if n < 2:
                        strConv += '-'

                strConv += '\n'
            strConv = strConv.replace("0", "*")
            strConv = strConv[:-1]
            print()
            print('Thinking...')
            print()
            print('Solving puzzle...')
            print()
            start_time = time.perf_counter()
            result = astar(EightPuzzleProblem(strConv))
            # result = astar(EightPuzzleProblem(strConv), viewer=WebViewer())

            elapsed_time_sec = time.perf_counter() - start_time
            elapsed_time_min = elapsed_time_sec / 60
            count = 0

            for action, state in result.path():
                if count == 0:
                    print(f"Initial State:")
                    print()
                    print(state)
                    print()
                    count += 1
                else:
                    print(f'#{count}. Move tile {action}:')
                    print()
                    print(state)
                    print()
                    count += 1

            print("*****************************************************************************************")
            print()
            print(
                f"\tSolution found in {elapsed_time_sec:0.4f} seconds and {elapsed_time_min:0.4f} minutes!")
            print()
            print(f"\tPuzzle solved in {count - 1} total moves!")
            print()
            print("*****************************************************************************************")
            print()

        else:
            print()
            print("Not Solvable.")
            print()

    except ValueError:
        print()
        print("Input must be in the format ### #*# ###.")
        print()
    except InvalidFormatException:
        print()
        print("Input must be in the format ### #*# ###.")
        print("The value '*' can exchange places with any other number (e.g. #*# ### ###).")
        print("No two digits can be repeated.")
        print("The input only accepts values in the range 1-8.")
        print()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
