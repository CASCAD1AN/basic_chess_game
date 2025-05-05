# Author: Derek Woodard
# GitHub: https://github.com/cascad1an
# Description: This file defines all chess piece classes, including their movement rules and Unicode representations.

class Pawn:
    """This class represents a Pawn piece with movement, capture logic, and Unicode rendering."""
    def __init__(self, color, position, board):
        self._init_move = True
        self._color = color
        self._position = position
        self._board = board

    def get_color(self):
        """Getter method for color"""
        return self._color

    def valid_moves(self):
        """
        Movement: Moves forward one square. Can move forward two squares on its first move.
        Capture Style: Captures one square diagonally forward.
        Restrictions: Cannot move backward. Cannot move forward into an occupied square. Cannot capture forward.
        """
        valid_moves = []
        start_col, start_row = self._board.coord_to_index(self._position)
        direction = 1 if self._color == 'WHITE' else -1         # pawns cannot move backwards

        forward_reg = start_row - direction
        if 8 > forward_reg >= 0:
            move_forward = self._board.index_to_coord(start_col, forward_reg)
            if self._board.is_square_open(move_forward):
                valid_moves.append(move_forward)

            if self._init_move:
                forward_move1 = start_row - (2 * direction)
                # initial move for pawn can move forward two squares (i.e. 2 * default dir)
                if 8 > forward_move1 >= 0:
                    forward_move1 = self._board.index_to_coord(start_col, forward_move1)
                    if self._board.is_square_open(forward_move1):
                        valid_moves.append(forward_move1)

        for diagonal in [-1, 1]:
            cap_col = start_col + diagonal
            if 0 <= cap_col < 8:
                cap_pos = self._board.index_to_coord(cap_col, forward_reg)
                if self._board.is_opponent(cap_pos, self._color):
                    valid_moves.append(cap_pos)

        return valid_moves

    def unicode(self):
        """Map unicode to piece"""
        if self._color == 'WHITE':
            return '\u2659'
        else:
            return '\u265F'


class Rook:
    """This class represents a Rook piece with movement, capture logic, and Unicode rendering."""
    def __init__(self, color, position, board):
        self._color = color
        self._position = position
        self._board = board

    def get_color(self):
        """Getter method for color"""
        return self._color

    def unicode(self):
        """Map unicode to piece"""
        if self._color == 'WHITE':
            return '\u2656'
        else:
            return '\u265C'

    def valid_moves(self):
        """
        Movement: Can move any number of vacant squares vertically or horizontally.
        Capture Style: Same as movement; captures by landing on an opponent’s piece along the same rank or file.
        Restrictions: Cannot jump over other pieces; movement is blocked by any intervening pieces.
        """
        valid_moves = []
        start_col, start_row = self._board.coord_to_index(self._position)
        direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for diag_col, diag_row in direction:
            for move in range(1, 8):
                to_col = start_col + (diag_col * move)
                to_row = start_row + (diag_row * move)
                if not (0 <= to_col < 8 and 0 <= to_row < 8):
                    break

                next_pos = self._board.index_to_coord(to_col, to_row)
                if self._board.is_square_open(next_pos):
                    valid_moves.append(next_pos)
                # SOME CAPTURE LOGIC
                elif self._board.is_opponent(next_pos, self._color):
                    valid_moves.append(next_pos)

        return valid_moves


class Knight:
    """This class represents a Knight piece with movement, capture logic, and Unicode rendering."""
    def __init__(self, color, position, board):
        self._color = color
        self._position = position
        self._board = board

    def get_color(self):
        """Getter method for color"""
        return self._color

    def unicode(self):
        """Map unicode to piece"""
        if self._color == 'WHITE':
            return '\u2658'
        else:
            return '\u265E'

    def valid_moves(self):
        """
        Movement: Moves in an L shape (two squares in one direction and then one square perpendicular to that).
        Capture Style: Same as movement; captures by landing on a square occupied by an opponent’s piece.
        Restrictions: Can jump over other pieces; movement is not blocked by intervening pieces.
        """
        valid_moves = []
        start_col, start_row = self._board.coord_to_index(self._position)

        direction = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                  (-2, -1), (-1, -2), (1, -2), (2, -1)]

        for col, row in direction:
            to_col = start_col + col
            to_row = start_row + row

            if 0 <= to_col < 8 and 0 <= to_row < 8:
                pos = self._board.index_to_coord(to_col, to_row)
                if self._board.is_square_open(pos) or self._board.is_opponent(pos, self._color):
                    valid_moves.append(pos)

        return valid_moves


class Bishop:
    """This class represents a Bishop piece with movement, capture logic, and Unicode rendering."""
    def __init__(self, color, position, board):
        self._color = color
        self._position = position
        self._board = board

    def get_color(self):
        """Getter method for color"""
        return self._color

    def unicode(self):
        """Map unicode to piece"""
        if self._color == 'WHITE':
            return '\u2657'
        else:
            return '\u265D'

    def valid_moves(self):
        """
        Movement: Can move any number of vacant squares diagonally.
        Capture Style: Same as movement; captures by moving to diagonally adjacent square occupied by opponent's piece.
        Restrictions: Cannot jump over other pieces; movement is limited to unobstructed diagonal paths.
        """
        valid_moves = []
        start_col, start_row = self._board.coord_to_index(self._position)

        direction = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        for coords in direction:
            to_col, to_row = start_col, start_row
            while True:
                to_col += coords[0]
                to_row += coords[1]
                # more board logic/validation checking bounds
                if not (7 >= to_col >= 0 and 7 >= to_row >= 0):
                    break

                target_pos = self._board.index_to_coord(to_col, to_row)

                if self._board.is_square_open(target_pos):
                    valid_moves.append(target_pos)
                elif self._board.is_opponent(target_pos, self._color):
                    valid_moves.append(target_pos)

        return valid_moves


class Queen:
    """This class represents a Queen piece with movement, capture logic, and Unicode rendering."""
    def __init__(self, color, position, board):
        self._color = color
        self._position = position
        self._board = board

    def get_color(self):
        """Getter method for color"""
        return self._color

    def unicode(self):
        """Map unicode to piece"""
        if self._color == 'WHITE':
            return '\u2655'
        else:
            return '\u265B'

    def valid_moves(self):
        """
        Movement: The queen can move any number of squares in a straight line — vertically, horizontally, or diagonally.
        Capture Style: Same as movement; captures by moving to a square occupied by an opponent's piece.
        Restrictions: Cannot jump over other pieces; movement is blocked by the first piece in its path.
        """
        valid_moves = []
        start_col, start_row = self._board.coord_to_index(self._position)

        direction = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for coords in direction:
            to_col, to_row = start_col, start_row

            while True:
                to_col += coords[0]
                to_row += coords[1]

                if not (7 >= to_col >= 0 and 7 >= to_row >= 0):
                    break

                target_pos = self._board.index_to_coord(to_col, to_row)

                if self._board.is_square_open(target_pos):
                    valid_moves.append(target_pos)
                elif self._board.is_opponent(target_pos, self._color):
                    valid_moves.append(target_pos)

        return valid_moves


class King:
    """This class represents a King piece with movement, capture logic, and Unicode rendering."""
    def __init__(self, color, position, board):
        self._color = color
        self._position = position
        self._board = board

    def get_color(self):
        """Getter method for color"""
        return self._color

    def unicode(self):
        """Map unicode to piece"""
        if self._color == 'WHITE':
            return '\u2654'
        else:
            return '\u265A'

    def valid_moves(self):
        """
        Movement: Can move exactly one square in any direction, vertically, horizontally, or diagonally.
        Capture Style: Same as movement; captures by moving to a square occupied by an opponent's piece.
        Restrictions: Cannot jump over other pieces; limited to one-square movement.
        """

        valid_moves = []
        start_col, start_row = self._board.coord_to_index(self._position)

        direction = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for coords in direction:
            to_col = start_col + coords[0]
            to_row = start_row + coords[1]

            if 0 <= to_col < 8 and 0 <= to_row < 8:
                target_pos = self._board.index_to_coord(to_col, to_row)
                if self._board.is_square_open(target_pos) or self._board.is_opponent(target_pos, self._color):
                    valid_moves.append(target_pos)

        return valid_moves
