# Author: Hassan Rachid
# Date: 3/4/20
# Description: Portfolio project where a working version of XiangQi (chinese chess) is made


class Pieces:
    """A parent class for all of the pieces in the game."""

    def __init__(self, color, position):
        self._color = color
        self._position = position
        self._piece_type = None
        self._possible_moves = []

    def get_color(self):
        """A get method for piece color"""
        return self._color

    def get_position(self):
        """A get method for the position of the piece"""
        return self._position

    def get_piece_type(self):
        """A get method for the piece type"""
        return self._piece_type

    def get_possible_moves(self):
        """A get method to get a piece's possible moves"""
        return self._possible_moves

    def set_possible_moves(self, lst):
        """A set method that sets a piece's possible moves to lst"""
        self._possible_moves = lst

    def update_position(self, col, row):
        """Updates the position of the piece"""
        possible_col = 'abcdefghi'
        if col not in possible_col:
            self._position = 'DEAD'
        else:
            new_pos = col + str(row+1)
            self._position = new_pos


class Rook(Pieces):
    """A subclass of Pieces for the Rook in the Chinese Checkers board game"""

    def __init__(self, color, position):
        """Initializes the Rook. Updates the attribute piece_type, which is just the name of the class."""
        super().__init__(color, position)
        self._piece_type = 'rook'

    def move(self, start, end, board):
        """This function moves the rook if possible. Takes as parameters the start position, the end position, and
        the current board."""
        start_col = start[0]
        start_row = int(start[1:]) - 1
        end_col = end[0]
        end_row = int(end[1:]) - 1

        # Check if the piece staying in the same column
        if start_col == end_col:

            # If the row also does not change, return False
            if start_row == end_row:
                return False

            # If moving forward (for red) or backward (for black)
            elif start_row < end_row:

                # Checking if piece is blocked on the way to desired location
                for index in range(start_row+1, end_row):
                    if board[end_col][index] != ' ':
                        return False

                # If the new position is empty, return True
                if board[end_col][end_row] == ' ':
                    return True

                # Otherwise, check whose piece is there
                else:

                    # If same team, can't move, return False
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Otherwise, return True
                    else:
                        return True

            # If moving backwards (for red) or forwards (for black)
            elif start_row > end_row:

                # Checking if piece is blocked on the way to desired location
                for index in range(start_row-1, end_row, -1):
                    if board[end_col][index] != ' ':
                        return False

                # If the new position is empty, return True
                if board[end_col][end_row] == ' ':
                    return True

                else:
                    # Otherwise, check which color the piece is. If same, can't move
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Otherwise, return True
                    else:
                        return True

        # If the piece is moving by staying in the same row (left to right)
        else:

            # Ensures that rows are different
            if start_row != end_row:
                return False

            # If moving to the right
            elif start_col < end_col:
                for index in board:

                    # Ignore columns to the left of the starting column since we are moving to the right
                    if index <= start_col:
                        continue

                    # Ensure that the columns leading up to the desired position are empty
                    elif index < end_col:
                        if board[index][end_row] != ' ':
                            return False

                    # Ignore columns beyond the ending column
                    elif index > end_col:
                        break

                # If the position is empty, return True
                if board[end_col][start_row] == ' ':
                    return True

                else:

                    # Otherwise, if the occupying piece is a friendly piece, Rook is blocked and returns False
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # If it is enemy piece, return True
                    else:
                        return True

            # If moving to the left
            elif start_col > end_col:
                for index in board:

                    # Ignore columns "greater than" the start column
                    if index >= start_col:
                        break

                    # Ignore columns beyond the ending column
                    elif index <= end_col:
                        continue

                    # Ensure that path is not blocked by any piece
                    elif end_col < index < start_col:
                        if board[index][end_row] != ' ':
                            return False

                # If space is empty, return True
                if board[end_col][end_row] == ' ':
                    return True

                else:

                    # If not, check if it is a friend piece. If so, rook is blocked. return False
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Otherwise, return True
                    else:
                        return True

    def __repr__(self):
        if self._color == 'red':
            return str('\u001b[41m R \u001b[0m')
        elif self._color == 'black':
            return str('\u001b[42m R \u001b[0m')


class Knight(Pieces):
    """A subclass of Pieces for the Rook in the Chinese Checkers board game"""

    def __init__(self, color, position):
        """Initializes the Knight piece. Updates the attribute piece_type, which is set to the name of the class."""
        super().__init__(color, position)
        self._piece_type = 'knight'

    def move(self, start, end, board):
        """A move function for the knight. Takes as parameters the start position, the end position and the
        board. The knight first moves one space orthogonally and then one space diagonally, in that order. It can be
        blocked if there is a piece blocking its orthogonal move."""
        start_col = start[0]
        start_row = int(start[1:]) - 1
        end_col = end[0]
        end_row = int(end[1:]) - 1
        letter_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9}
        num_to_letter = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}

        column_diff = letter_to_num[start_col] - letter_to_num[end_col]

        # If the column changes by only one value, the orthogonal move is either forward or back
        if abs(column_diff) == 1:

            # Ensures that the move is legal
            if abs(start_row - end_row) != 2:
                return False

            # If moving forward (for red) or backwards (for black)
            elif start_row < end_row:

                # Check if orthogonal move is blocked
                if board[start_col][start_row+1] != ' ':
                    return False

                else:
                    # If not blocked and space empty, return True
                    if board[end_col][end_row] == ' ':
                        return True

                    # If blocked by teammate, return False
                    elif board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Otherwise, return True
                    else:
                        return True

            # Orthogonal move backwards (for red) or forwards (for black)
            elif start_row > end_row:

                # Check if orthogonal move is blocked
                if board[start_col][start_row - 1] != ' ':
                    return False

                else:

                    # If not blocked and end space empty, return True
                    if board[end_col][end_row] == ' ':
                        return True

                    # If end space has teammate, return False
                    elif board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Otherwise, return True
                    else:
                        return True

        # When orthogonal move is left/right
        else:

            # Ensures that the move is legal
            if abs(column_diff) != 2:
                return False

            elif abs(start_row - end_row) != 1:
                return False

            # If the orthogonal move is to the left
            elif column_diff > 0:

                # If that space is not empty, return False
                if board[num_to_letter[letter_to_num[start_col] - 1]][start_row] != ' ':
                    return False

                # If not blocked
                else:

                    # And final space is empty, return True
                    if board[end_col][end_row] == ' ':
                        return True

                    # If blocked by teammate, return False
                    elif board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Otherwise, return True
                    else:
                        return True

            else:
                # If that space is not empty, return False
                if board[num_to_letter[letter_to_num[start_col] + 1]][start_row] != ' ':
                    return False

                # If not blocked
                else:

                    # And final space is empty, return True
                    if board[end_col][end_row] == ' ':
                        return True

                    # If blocked by teammate, return False
                    elif board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Otherwise, return True
                    else:
                        return True

    def __repr__(self):
        if self._color == 'red':
            return str('\u001b[41m K \u001b[0m')
        elif self._color == 'black':
            return str('\u001b[42m K \u001b[0m')


class Elephant(Pieces):
    """A subclass of Pieces for the Rook in the Chinese Checkers board game"""

    def __init__(self, color, position):
        """Initializes the elephant piece. Updates the attribute piece_type, which is set to the name of the
        class."""
        super().__init__(color, position)
        self._piece_type = 'elephant'

    def move(self, start, end, board):
        """The move function for the elephant. Takes in as parameters the start position, the end position, and the
        board. The elephant moves two points diagonally. It cannot jump over other pieces, so it is possible to
        block the elephant from moving. The elephant cannot cross the river."""
        start_col = start[0]
        start_row = int(start[1:]) - 1
        end_col = end[0]
        end_row = int(end[1:]) - 1
        letter_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9}
        num_to_letter = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}

        # Set the list of possible move locations based on color
        if self.get_color() == 'red':
            possible_moves = ['c1', 'a3', 'c5', 'e3', 'g1', 'i3', 'g5']
        else:
            possible_moves = ['c10', 'a8', 'c6', 'e8', 'g10', 'i8', 'g6']

        # These middle variables are used to check if the elephant is blocked. It calculates the middle column
        # By converting the letters to numbers, finding the average, and converting back to letter. It finds the
        # middle row by simply taking the average
        middle_col = num_to_letter[int(abs(letter_to_num[start_col] + letter_to_num[end_col]) / 2)]
        middle_row = int((start_row + end_row) / 2)

        # If the move requested is not possible, return False
        if end not in possible_moves:
            return False

        # If the move is not diagonal and within two spaces, return False
        elif abs(start_row - end_row) != 2 or abs(letter_to_num[start_col] - letter_to_num[end_col]) != 2:
            return False

        # If the first diagonal move is not empty, the elephant is blocked. Return false
        elif board[middle_col][middle_row] != ' ':
            return False

        else:

            # If the desired location is empty, return True
            if board[end_col][end_row] == ' ':
                return True

            # If blocked by teammate, return False
            elif board[end_col][end_row].get_color() == self.get_color():
                return False

            # Otherwise, return True
            else:
                return True

    def __repr__(self):
        if self._color == 'red':
            return str('\u001b[41m E \u001b[0m')
        elif self._color == 'black':
            return str('\u001b[42m E \u001b[0m')


class Advisor(Pieces):
    """A subclass of Pieces for the Rook in the Chinese Checkers board game"""

    def __init__(self, color, position):
        """Initializes the advisor piece. Updates the attribute piece_type, which is set to the name of the class."""
        super().__init__(color, position)
        self._piece_type = 'advisor'

    def move(self, start, end, board):
        """A move method for the advisor. Takes as a parameter the stand position, the end position, and the board.
        The advisor must stay within the castle and can only move one space diagonally."""
        start_col = start[0]
        start_row = int(start[1:]) - 1
        end_col = end[0]
        end_row = int(end[1:]) - 1
        letter_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9}

        # Possible positions by piece color
        if self.get_color() == 'red':
            possible_pos = ['d1', 'd3', 'e2', 'f1', 'f3']
        else:
            possible_pos = ['d10', 'd8', 'e9', 'f10', 'f8']

        # If the requested move is not possible
        if end not in possible_pos:
            return False

        # If the move is not diagonal and within one space
        elif abs(start_row - end_row) != 1 or abs(letter_to_num[start_col] - letter_to_num[end_col]) != 1:
            return False

        # If the space is empty, return True
        elif board[end_col][end_row] == ' ':
            return True

        else:
            # If blocked by a friendly piece, return False
            if board[end_col][end_row].get_color() == self.get_color():
                return False

            # If an enemy is in spot, return True
            else:
                return True

    def __repr__(self):
        if self._color == 'red':
            return str('\u001b[41m A \u001b[0m')
        elif self._color == 'black':
            return str('\u001b[42m A \u001b[0m')


class General(Pieces):
    """A subclass of Pieces for the Rook in the Chinese Checkers board game"""

    def __init__(self, color, position):
        """Initializes the General piece. Updates the piece_type attribute, which is set to the name of the class."""
        super().__init__(color, position)
        self._piece_type = 'general'

    def move(self, start, end, board):
        """A move method for the general. Takes as parameters the starting position, the ending position, and
        the game board. The general must stay in the castle. It also cannot be in the same column as the enemy
        general without another piece in-between. """
        start_col = start[0]
        start_row = int(start[1:]) - 1
        end_col = end[0]
        end_row = int(end[1:]) - 1
        letter_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9}
        blocking_pieces = 0

        # Set possible_moves list based on color
        if self.get_color() == 'red':
            possible_moves = ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
        else:
            possible_moves = ['d10', 'd9', 'd8', 'e10', 'e9', 'e8', 'f10', 'f9', 'f8']

        # Check if the requested move would put the general in the line of sight of the enemy general
        for row in range(len(board[end_col])):

            # Check blocking pieces for red general
            if self.get_color() == 'red':
                if board[end_col][row] != ' ' and board[end_col][row].get_piece_type() != 'general' and row > end_row:
                    blocking_pieces += 1

            # Checking blocking pieces for black general
            else:
                if board[end_col][row] != ' ' and board[end_col][row].get_piece_type() != 'general' and row < end_row:
                    blocking_pieces += 1

            # Check if same column as general and then check if there are blocking pieces between them
            if board[end_col][row] != ' ' and board[end_col][row].get_piece_type() == 'general':
                if board[end_col][row].get_color() != self.get_color():
                    if blocking_pieces == 0:
                        return False

        # Ensure that requested location is in the move list
        if end not in possible_moves:
            return False

        # Ensure that orthogonal move is within one space in any direction
        elif abs(letter_to_num[start_col] - letter_to_num[end_col]) > 1 or abs(start_row - end_row) > 1:
            return False

        # If space is empty, return True
        elif board[end_col][end_row] == ' ':
            return True

        else:

            # check if piece is location is friendly
            if board[end_col][end_row].get_color() == self.get_color():
                return False

            # If enemy piece, return True
            else:
                return True

    def possible_moves(self):
        if self.get_color() == 'red':
            return ['d1', 'd2', 'd3', 'e1', 'e2', 'e3', 'f1', 'f2', 'f3']
        else:
            return ['d1', 'd9', 'd8', 'e10', 'e9', 'e8', 'f10', 'f9', 'f8']

    def __repr__(self):
        if self._color == 'red':
            return str('\u001b[41m G \u001b[0m')
        elif self._color == 'black':
            return str('\u001b[42m G \u001b[0m')


class Canon(Pieces):
    """A subclass of Pieces for the Rook in the Chinese Checkers board game"""

    def __init__(self, color, position):
        """Initializes the Canon piece. Updates the attribute piece_type, which is set to the name of the class."""
        super().__init__(color, position)
        self._piece_type = 'canon'

    def move(self, start, end, board):
        """Attempts to move the canon piece if possible. The canon moves in the same manner as the Rook. However,
        it needs to jump over one other piece to eliminate an enemy. Takes as a parameters the starting position,
        the ending position, and the board."""
        start_col = start[0]
        start_row = int(start[1:]) - 1
        end_col = end[0]
        end_row = int(end[1:]) - 1
        jump = False
        jumped_pieces = 0

        # Check if moving within the same column
        if start_col == end_col:

            # If the row also does not change, return False
            if start_row == end_row:
                return False

            # If moving forward (for red) or backward (for black)
            elif start_row < end_row:

                # If the new position is empty,
                if board[end_col][end_row] == ' ':

                    # Checking if piece is blocked on the way to desired location
                    for index in range(start_row + 1, end_row):
                        if board[end_col][index] != ' ':
                            return False
                    return True

                # Otherwise, check whose piece is there
                else:

                    # If same team, can't move, return False
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Count how many pieces the canon jumps over
                    else:
                        for index in range(start_row + 1, end_row):
                            if board[end_col][index] != ' ':
                                jump = True
                                jumped_pieces += 1

                        # If only one, return True
                        if jump is True and jumped_pieces == 1:
                            return True

                        # Otherwise, return False
                        else:
                            return False

            # If moving backwards (for red) or forwards (for black)
            elif start_row > end_row:

                # If the new position is empty,
                if board[end_col][end_row] == ' ':

                    # Checking if piece is blocked on the way to desired location
                    for index in range(start_row - 1, end_row, -1):
                        if board[end_col][index] != ' ':
                            return False
                    return True

                else:
                    # Otherwise, check which color the piece is. If same, can't move
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False
                    else:

                        # Count number of pieces jumped over
                        for index in range(start_row - 1, end_row, -1):
                            if board[end_col][index] != ' ':
                                jump = True
                                jumped_pieces += 1

                        # If only one, return True
                        if jump is True and jumped_pieces == 1:
                            return True

                        # Otherwise, return False
                        else:
                            return False

        # If the piece is moving by staying in the same row (left to right)
        else:

            # Ensures that rows are different
            if start_row != end_row:
                return False

            # If moving to the right
            elif start_col < end_col:

                # If the position is empty, check if canon is blocked
                if board[end_col][start_row] == ' ':
                    for index in board:

                        # Ignore columns to the left of the starting column since we are moving to the right
                        if index <= start_col:
                            continue

                        # Ensure that the columns leading up to the desired position are empty
                        elif index < end_col:
                            if board[index][end_row] != ' ':
                                return False

                        # Ignore columns beyond the ending column
                        elif index > end_col:
                            break

                    # If not blocked on the way to empty space, return True
                    return True

                else:

                    # Otherwise, if the occupying piece is a friendly piece, Rook is blocked and returns False
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # If it is enemy piece, check if it jumps one piece
                    else:
                        for index in board:

                            # Ignore columns to the left of the starting column since we are moving to the right
                            if index <= start_col:
                                continue

                            # Count how many pieces the canon jumps over
                            elif index < end_col:
                                if board[index][end_row] != ' ':
                                    jump = True
                                    jumped_pieces += 1
                            elif index > end_col:
                                break

                        # Ensure that canon jumps over one piece
                        if jump is True and jumped_pieces == 1:
                            return True

                        # If not, return False
                        else:
                            return False

            # If moving to the left
            elif start_col > end_col:

                # If space is empty
                if board[end_col][end_row] == ' ':
                    for index in board:

                        # Ignore columns "greater than" the start column
                        if index >= start_col:
                            break

                        # Ignore columns beyond the ending column
                        elif index <= end_col:
                            continue

                        # Ensure that path is not blocked by any piece
                        elif end_col < index < start_col:
                            if board[index][end_row] != ' ':
                                return False

                    # If not blocked on the way to empty space, return True
                    return True

                else:

                    # If not, check if it is a friend piece. If so, rook is blocked. return False
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # When space occupied by enemy piece
                    else:

                        # Need to check if canon jumps over a piece
                        for index in board:

                            # Ignore columns "greater than" the start column
                            if index >= start_col:
                                break

                            # Ignore columns beyond the ending column
                            elif index <= end_col:
                                continue

                            # Count number of pieces that the canon jumps over
                            elif end_col < index < start_col:
                                if board[index][end_row] != ' ':
                                    jump = True
                                    jumped_pieces += 1

                        # If canon jumps only one piece, return True
                        if jump is True and jumped_pieces == 1:
                            return True

                        # Otherwise return False
                        else:
                            return False

    def __repr__(self):
        if self._color == 'red':
            return str("\u001b[41m C \u001b[0m")
        elif self._color == 'black':
            return str('\u001b[42m C \u001b[0m')


class Soldier(Pieces):
    """A subclass of Pieces for the Rook in the Chinese Checkers board game"""

    def __init__(self, color, position):
        """Initializes the Soldier piece. Adds two new attributes: crossed_river and piece_type. Crossed river
        indicates if the soldier has crossed the river and will allow it to move sideways. Piece_type is the name
        of the class."""
        super().__init__(color, position)
        self._crossed_river = False
        self._piece_type = 'soldier'

    def get_crossed_river(self):
        """A get method for crossed_river attribute"""
        return self._crossed_river

    def move(self, start, end, board):
        """A move method for the soldier piece on the board. It moves the soldier piece if possible. Takes as a
        parameter the start position, end position, and the board state. The soldier moves one point forward. never
        backward. Once it crosses the river, it can also move one point sideways"""
        start_col = start[0]
        start_row = int(start[1:]) - 1
        end_col = end[0]
        end_row = int(end[1:]) - 1
        letter_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f':  6, 'g': 7, 'h': 8, 'i': 9}

        # Checks to see if the soldier can move sideways yet
        if start_col != end_col and self.get_crossed_river() is False:
            return False

        # Checks that the requested move is within one space
        elif abs(start_row - end_row) > 1 or abs(letter_to_num[start_col] - letter_to_num[end_col]) > 1:
            return False

        else:

            # Makes sure soldier is not moving backwards
            if self.get_color() == 'red' and start_row > end_row:
                return False
            elif self.get_color() == 'black' and start_row < end_row:
                return False

            # If moving forward
            if start_col == end_col and start_row != end_row:

                # And position is empty, return True
                if board[end_col][end_row] == ' ':

                    # If river is crossed, update attribute
                    if self.get_color() == 'red' and end_row >= 5:
                        self._crossed_river = True
                    elif self.get_color() == 'black' and end_row <= 4:
                        self._crossed_river = True
                    return True

                else:

                    # If blocked by teammate, return False
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # If its an enemy, return True
                    else:

                        # If river is crossed, update attribute
                        if self.get_color() == 'red' and end_row >= 5:
                            self._crossed_river = True
                        elif self.get_color() == 'black' and end_row <= 4:
                            self._crossed_river = True
                        return True

            # if moving sideways
            elif start_col != end_col and start_row == end_row:

                # And position is empty, return True
                if board[end_col][start_row] == ' ':
                    return True

                else:

                    # If blocked by a teammate, return False
                    if board[end_col][end_row].get_color() == self.get_color():
                        return False

                    # Otherwise, return True
                    else:
                        return True

            # Not moving forwards or sideways
            else:
                return False

    def __repr__(self):
        if self._color == 'red':
            return str('\u001b[41m S \u001b[0m')
        elif self._color == 'black':
            return str('\u001b[42m S \u001b[0m')


class XiangqiGame:
    """This initializes the Xiangqi board game by setting up the board. Red pieces are uppercase. Black pieces are
    lowercase. Red goes first."""

    def __init__(self):
        """Initializes the game. The board is stored in a dictionary by column. Each index in the dictionary is
        the letter a-i. The game state is initialized to UNFINISHED. And the first player's turn is set to red.
        Uppercase letters are red pieces. Lowercase letters are black pieces"""
        R1 = Rook('red', 'a1')
        R2 = Rook('red', 'i1')
        K1 = Knight('red', 'b1')
        K2 = Knight('red', 'h1')
        E1 = Elephant('red', 'c1')
        E2 = Elephant('red', 'g1')
        A1 = Advisor('red', 'd1')
        A2 = Advisor('red', 'f1')
        G = General('red', 'e1')
        C1 = Canon('red', 'b3')
        C2 = Canon('red', 'h3')
        S1 = Soldier('red', 'a4')
        S2 = Soldier('red', 'c4')
        S3 = Soldier('red', 'e4')
        S4 = Soldier('red', 'g4')
        S5 = Soldier('red', 'i4')
        r1 = Rook('black', 'a10')
        r2 = Rook('black', 'i10')
        k1 = Knight('black', 'b10')
        k2 = Knight('black', 'h10')
        e1 = Elephant('black', 'c10')
        e2 = Elephant('black', 'g10')
        a1 = Advisor('black', 'd10')
        a2 = Advisor('black', 'f10')
        g = General('black', 'e10')
        c1 = Canon('black', 'b8')
        c2 = Canon('black', 'h8')
        s1 = Soldier('black', 'a7')
        s2 = Soldier('black', 'c7')
        s3 = Soldier('black', 'e7')
        s4 = Soldier('black', 'g7')
        s5 = Soldier('black', 'i7')

        self._board = {
            'a': [R1, ' ', ' ', S1, ' ', ' ', s1, ' ', ' ', r1],
            'b': [K1, ' ', C1, ' ', ' ', ' ', ' ', c1, ' ', k1],
            'c': [E1, ' ', ' ', S2, ' ', ' ', s2, ' ', ' ', e1],
            'd': [A1, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', a1],
            'e': [G, ' ', ' ', S3, ' ', ' ', s3, ' ', ' ', g],
            'f': [A2, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', a2],
            'g': [E2, ' ', ' ', S4, ' ', ' ', s4, ' ', ' ', e2],
            'h': [K2, ' ', C2, ' ', ' ', ' ', ' ', c2, ' ', k2],
            'i': [R2, ' ', ' ', S5, ' ', ' ', s5, ' ', ' ', r2]
        }
        self._game_state = 'UNFINISHED'
        self._turn = 'red'
        self._red_pieces_left = [R1, R2, K1, K2, E1, E2, A1, A2, G, C1, C2, S1, S2, S3, S4, S5]
        self._black_pieces_left = [r1, r2, k1, k2, e1, e2, a1, a2, g, c1, c2, s1, s2, s3, s4, s5]
        self._red_general = G
        self._black_general = g

    def get_game_state(self):
        """A get method that returns the current game state."""
        return self._game_state

    def get_turn(self):
        """A get method to get whose turn it is"""
        return self._turn

    def get_board(self):
        """A get method for game board"""
        return self._board

    def get_red_pieces_left(self):
        """A get method for the pieces left of the specified color"""
        return self._red_pieces_left

    def get_black_pieces_left(self):
        """A get method for the pieces left of the specified color"""
        return self._black_pieces_left

    def get_red_gen(self):
        """A get method for the red general"""
        return self._red_general

    def get_black_gen(self):
        """A get method for the black general"""
        return self._black_general

    def set_turn(self, color):
        """A set method to set the proper player's turn"""
        self._turn = color

    def make_move(self, start, end):
        """A method that moves a piece from a starting position to the ending position. It first checks to make sure
        the proper player is moving. Then, it moves the piece if possible."""
        start_column = start[0]
        start_row = int(start[1:]) - 1
        end_column = end[0]
        end_row = int(end[1:]) - 1
        board = self.get_board()
        piece = board[start_column][start_row]
        enemy = board[end_column][end_row]

        # Check if game is still going
        if self.get_game_state() != 'UNFINISHED':
            return False

        # Check that a piece was selected
        elif piece == ' ':
            return False

        # Check that it is that piece's turn
        elif self.get_turn() != piece.get_color():
            return False

        else:
            # Try to make a move with the selected piece
            move = piece.move(start, end, board)

            # If the .move method returns False, move is invalid, return False
            if move is False:
                return False

            # Otherwise, empty the starting position, move to new position, update positions, and update the game state
            else:
                if enemy != ' ':
                    enemy.update_position('z', 0)
                board[start_column][start_row] = ' '
                board[end_column][end_row] = piece
                piece.update_position(end_column, end_row)

                # Check if move puts general in line of sight of other general or if move puts general in check
                if self.general_los() or self.is_in_check(piece.get_color()):

                    # Move is then not legal, must go back and return False
                    if enemy != ' ':
                        enemy.update_position(end_column, end_row)
                    board[end_column][end_row] = enemy
                    board[start_column][start_row] = piece
                    piece.update_position(start_column, start_row)
                    return False

                # Otherwise, update game state and return True
                else:
                    self.update_game_state()
                    return True

    def is_in_check(self, color):
        """A method that checks whether the indicated color's general is in check"""
        red_general = self.get_red_gen()
        black_general = self.get_black_gen()

        # Check color
        if color.lower() == 'red':

            # Check if any black piece has a legal move to eliminate the red general
            for piece in self.get_black_pieces_left():
                if piece.get_position() == 'DEAD':
                    continue
                result = piece.move(piece.get_position(), red_general.get_position(), self.get_board())

                # If a piece has a legal move to the general, then it is in check
                if result is True:
                    return True

            # Otherwise, return False
            return False

        else:

            # Check if any red piece has a legal move to the black general
            for piece in self.get_red_pieces_left():
                if piece.get_position() == 'DEAD':
                    continue
                result = piece.move(piece.get_position(), black_general.get_position(), self.get_board())

                # If a piece has a legal move to the general, it is in check
                if result is True:
                    return True

            # Otherwise, return False
            return False

    def update_game_state(self):
        """A method that updates the game state based on the board"""

        # Remove any pieces that were eliminate from the game from piece lists
        for el in self.get_red_pieces_left():
            if el.get_position() == 'DEAD':
                self._red_pieces_left.remove(el)
        for el in self.get_black_pieces_left():
            if el.get_position() == 'DEAD':
                self._black_pieces_left.remove(el)

        # Update all possible moves
        self.all_poss_moves()

        # If red just went, check if black has any legal moves
        if self.get_turn() == 'red':

            # Change whose turn it is
            self.set_turn('black')
            possible_moves = 0
            for piece in self.get_black_pieces_left():

                # Check if any black piece has any legal moves (whether in check or not)
                move_list = piece.get_possible_moves()

                # If there is, increase possible_moves by 1
                if len(move_list) > 0:
                    possible_moves += 1
                    break

            # If no legal moves available, Red wins
            if possible_moves == 0:
                self._game_state = 'RED_WON'

        # If black just went, check if red has any legal moves
        elif self.get_turn() == 'black':

            # Change whose turn it is
            self.set_turn('red')
            possible_moves = 0
            for piece in self.get_red_pieces_left():

                # Check if any black piece has any legal moves (whether in check or not)
                move_list = piece.get_possible_moves()

                # If there is, increase possible_moves by 1
                if len(move_list) > 0:
                    possible_moves += 1
                    break

            # If no legal moves available, black wins
            if possible_moves == 0:
                self._game_state = 'BLACK_WON'

    def general_los(self):
        """A method that checks if the generals have line of sight of each other."""
        red_general = self.get_red_gen()
        black_general = self.get_black_gen()

        red_gen_pos = red_general.get_position()
        black_gen_pos = black_general.get_position()

        # If in same column
        if red_gen_pos[0] == black_gen_pos[0]:
            board = self.get_board()
            piece_in_middle = False
            # Check if other pieces block line of sight
            for row in range(len(board[red_gen_pos[0]])):
                if int(red_gen_pos[1:])-1 < row < int(black_gen_pos[1:])-1 and board[red_gen_pos[0]][row] != ' ':
                    piece_in_middle = True
                    break
            return not piece_in_middle

        # If not in same column, no line of sight
        else:
            return False

    def stalemate(self, color):
        """Checks to see if the color was put in stalemate by checking if they have any legal moves. This should
        only be used when not in check."""
        if color == 'red':
            piece_list = self.get_red_pieces_left()
        else:
            piece_list = self.get_black_pieces_left()

        # For every piece left, get their possible move list and check their lengths
        for piece in piece_list:
            moves = piece.get_possible_moves()

            # If any move list has one entry, then there is no stalemate, return False
            if len(moves) > 0:
                return False

        # Otherwise, return True
        return True

    def legal_move(self, start, end):
        """A method that is almost identical to the make_move method. However, every move made is undone and it does
        not update the game state. This checks if a move made is legal and returns True if it is and False if it
        isn't. Either way, it resets the board"""
        start_column = start[0]
        start_row = int(start[1:]) - 1
        end_column = end[0]
        end_row = int(end[1:]) - 1
        board = self.get_board()
        piece = board[start_column][start_row]
        enemy = board[end_column][end_row]

        # Check if game is still going
        if self.get_game_state() != 'UNFINISHED':
            return False

        # Check that a piece was selected
        elif piece == ' ':
            return False

        else:
            # Try to make a move with the selected piece
            move = piece.move(start, end, board)

            # If the .move method returns False, move is invalid, return False
            if move is False:
                return False

            # Otherwise, empty the starting position, move to new position, update positions, and update the game state
            else:
                board[start_column][start_row] = ' '
                board[end_column][end_row] = piece
                piece.update_position(end_column, end_row)

                # Check if move puts general in line of sight of other general or if move puts general in check
                if self.general_los() or self.is_in_check(piece.get_color()):

                    # Still in check, undo move and return False
                    board[end_column][end_row] = enemy
                    board[start_column][start_row] = piece
                    piece.update_position(start_column, start_row)
                    return False

                # Otherwise, move is legal. Undo move and return True
                else:
                    board[end_column][end_row] = enemy
                    board[start_column][start_row] = piece
                    piece.update_position(start_column, start_row)
                    return True

    def all_poss_moves(self):
        """A method that updates all possible moves for all of the pieces left in the game"""
        possible_col = 'abcdefghi'
        check_pos = ''

        # For every piece left, check if they have a legal move to anywhere on the board
        # Save every possible move to a list, then update the piece's attribute. Then reset and do the next piece
        for piece in self.get_black_pieces_left():
            moves = []
            for letter in possible_col:
                for index in range(1, 11):
                    check_pos += letter + str(index)
                    result = self.legal_move(piece.get_position(), check_pos)

                    if result:
                        moves += [check_pos]
                    check_pos = ''
            piece.set_possible_moves(moves)

        for piece in self.get_red_pieces_left():
            moves = []
            for letter in possible_col:
                for index in range(1, 11):
                    check_pos += letter + str(index)
                    result = self.legal_move(piece.get_position(), check_pos)

                    if result:
                        moves += [check_pos]
                    check_pos = ''
            piece.set_possible_moves(moves)

    def __repr__(self):
        """When the board is printed. Red squares are red pieces. Green squares are black piecs. Blue line is
        the river."""
        board = '--|---1   2   3   4   5   r   6   7   8   9  10--|--'
        board += '\n'
        board += "--|---|---|---|---|---|-------|---|---|---|---|--|--"
        board += '\n'
        for column in self._board:
            board += column + '-|-'
            for index in range(len(self._board[column])):
                if isinstance(self._board[column][index], str):
                    if index == 4:
                        board += '-[ ]-'
                        board += '\u001b[44m   \u001b[0m'
                    elif index == 5:
                        board += '-[ ]'
                    else:
                        board += '-[ ]'
                    board += ''
                else:
                    board += '-' + str(self._board[column][index])
                    if index == 4:
                        board += '-' + '\u001b[44m   \u001b[0m'
                    board += ''
            board += '-|-' + column
            board += "\n"
        board += "--|---|---|---|---|---|-------|---|---|---|---|--|--"
        board += '\n'
        board += '--|---1   2   3   4   5   r   6   7   8   9  10--|--'
        return board



def main():
    game = XiangqiGame()
    print('Hello! Welcome to XiangQi (Chinese Chess)! Red player goes first.')
    print('Please input a starting position and an ending position to make a move.')
    print('\n')
    print(game)
    while True:
        if game.get_turn() == 'red':
            print('Your move, red.')
        else:
            print('Your move, black.')
        start = input('Starting Position: ')
        end = input('Ending Position: ')
        game.make_move(start, end)
        print('\n')
        print(game)

        if game.get_game_state() != 'UNFINISHED':
            break

    if game.get_game_state() == 'RED_WON':
        print('Red wins!', end=' ')
    else:
        print('Black wins!', end=' ')
    print('Hope you enjoyed playing!')


main()