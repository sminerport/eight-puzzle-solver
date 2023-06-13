class PuzzleSolver:
    """
    A class that provides utility functions for solving the puzzle.

    ...

    Methods
    -------
    getInvCount(tiles)
        Counts the inversions in a given array 'tiles[]'.
    isSolvable(puzzle)
        Returns true if given 8 puzzle is solvable.
    """

    @staticmethod
    def getInvCount(tiles):
        """
        Counts the inversions in a given array 'tiles[]'.
        """

        inv_count = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if tiles[j] and tiles[i] and tiles[i] > tiles[j]:
                    inv_count += 1
        return inv_count

    @staticmethod
    def isSolvable(puzzle):
        """
        Returns true if given 8 puzzle is solvable.
        """

        # Count inversions in given 8 puzzle
        invCount = PuzzleSolver.getInvCount(puzzle)
        # return true if inversion count is even.
        return (invCount % 2 == 0)