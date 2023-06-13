class PuzzleRepresentation:
    """
    A class that represents the 8-puzzle game.

    ...

    Methods
    -------
    list_to_string(list_)
        Converts a list representation of the puzzle to a string.
    string_to_list(string_)
        Converts a string representation of the puzzle to a list.
    find_location(rows, element_to_find)
        Finds the location of a piece in the puzzle.
    """

    @staticmethod
    def list_to_string(list_):
        """
        Converts a list representation of the puzzle to a string.
        """
        return '\n'.join(['-'.join(row) for row in list_])

    @staticmethod
    def string_to_list(string_):
        """
        Converts a string representation of the puzzle to a list.
        """
        return [row.split('-') for row in string_.split('\n')]

    @staticmethod
    def find_location(rows, element_to_find):
        """
        Finds the location of a piece in the puzzle.
        """
        for ir, row in enumerate(rows):
            for ic, element in enumerate(row):
                if element == element_to_find:
                    return ir, ic
