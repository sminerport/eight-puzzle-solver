import re
import time
from src.eight_puzzle_problem import EightPuzzleProblem
from src.puzzle_solver import PuzzleSolver
from simpleai.search.traditional import astar

class InvalidFormatException(Exception):
    pass

def main():
    while True:
        try:
            print_instructions()
            user_input = input("Please input the initial state of the 8-puzzle, with each row separated by a space (e.g., '732 5*1 864'): ")
            digitList = process_input(user_input)
            if (PuzzleSolver.isSolvable(digitList)):
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
                print("\nProcessing input and initiating A* search...")

                start_time = time.perf_counter()
                result = astar(EightPuzzleProblem(strConv))
                elapsed_time_sec = time.perf_counter() - start_time

                if elapsed_time_sec < 60:
                    print_solution(result, elapsed_time_sec)
                else:
                    elapsed_time_min = elapsed_time_sec / 60
                    print_solution(result, elapsed_time_min, format_in_minutes=True)
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

# Helper functions
def print_instructions():
    # Print the instructions for the user
    print("*************************************************************************************")
    print("AI PROGRAM TO SOLVE AN 8-PUZZLE GIVEN AN INITIAL STATE USING A* SEARCH")
    print("*************************************************************************************")

    print("Instructions:")
    print("-------------")
    print("1. Enter the initial state of the 8-puzzle in the following format: ### #*# ###")
    print("   Each '#' represents a digit from 1 to 8, and '*' represents the empty space.")
    print("   Digits cannot be repeated, and the location of the '*' can be exchanged with any '#'.")
    print()
    print("2. For example, if the 8-puzzle's initial state is:")
    print("   [ 7-3-2 ]")
    print("   [ 5-*-1 ]")
    print("   [ 8-6-4 ]")
    print("   Then, enter '732 5*1 864', with each row separated by a space.")
    print()
    print("3. Press enter when done.")
    print()

    print("Method:")
    print("-------")
    print("The AI program uses the A* search to find the cost-optimal solution from the initial state to the goal state.")
    print("The goal state of the 8-puzzle is:")
    print("   [ 1-2-3 ]")
    print("   [ 4-5-6 ]")
    print("   [ 7-8-* ]")
    print()
    print("If the initial state is unsolvable or if there is an error in the input, the program will notify you.")
    print("Otherwise, the program will output the steps of the cost-optimal solution.")
    print("*************************************************************************************")
    print()


def process_input(user_input):
    row1, row2, row3 = user_input.split()
    concat = row1 + row2 + row3
    digitList = []
    if not re.match(r"(?!.*([1-8\*]).*\1)^[1-8\*]{9}$", concat):
        raise InvalidFormatException
    concatRepE = concat.replace("*", "0")
    for c in concatRepE:
        digitList.append(int(c))
    return digitList

def print_solution(solution, elapsed_time, format_in_minutes=False):
    step_number = 0
    for action, state in solution.path():
        print("--------------------------------------------------------------------------------")
        if step_number == 0:
            print("Initial State:\n")
            print(state)
        else:
            print(f"Step {step_number}: Move tile {action}\n")
            print(state)
        step_number += 1
        print("--------------------------------------------------------------------------------")

    if format_in_minutes:
        print(f"\nSolution found in {elapsed_time:0.2f} minutes!")
    else:
        print(f"\nSolution found in {elapsed_time:0.2f} seconds!")

    print(f"Puzzle solved in {step_number - 1} steps!\n")


# Run the main function
if __name__ == "__main__":
    main()
