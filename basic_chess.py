# Author: Derek Woodard
# GitHub: https://github.com/cascad1an
# Description: Very basic chess game. Takes input from user to determine move for both sides.
# The game ends when one player's king is captured; some other standard chess rules may not apply.

from piece_classes import *


class InvalidStateError(Exception):
    """Exception class for InvalidStateError"""
    pass


class ChessGame:
    """Manages the general game logic for us, including the game state, player turn, move validation."""
    def __init__(self):
        """init method with items we initialize from the beginning, including the game state, player turn, the board,
        an empty piece dictionary, and a board layout which will be defined immediately after this method."""
        self._game_state = 'UNFINISHED'
        self._player_turn = 'WHITE'
        self._pieces = {}
        self._init_pos = {}    # represents both the initial layout and the current state of the board
        self._board_start()

    def _board_start(self):
        """Initializes all pieces and their starting positions on the board.
        The _init_pos dictionary functions as both a container for all pieces and the live board state."""
        self._pieces = {
            'r': '\u265C', 'kn': '\u265E', 'b': '\u265D', 'q': '\u265B', 'k': '\u265A', 'p': '\u265F',
            'R': '\u2656', 'KN': '\u2658', 'B': '\u2657', 'Q': '\u2655', 'K': '\u2654', 'P': '\u2659', 'sp': ' '
        }

        self._init_pos = {
            'a8': Rook('BLACK', 'a8', self), 'b8': Knight('BLACK', 'b8', self),
            'c8': Bishop('BLACK', 'c8', self), 'd8': King('BLACK', 'd8', self),
            'e8': Queen('BLACK', 'e8', self), 'f8': Bishop('BLACK', 'f8', self),
            'g8': Knight('BLACK', 'g8', self), 'h8': Rook('BLACK', 'h8', self),
            'a7': Pawn('BLACK', 'a7', self), 'b7': Pawn('BLACK', 'b7', self),
            'c7': Pawn('BLACK', 'c7', self), 'd7': Pawn('BLACK', 'd7', self),
            'e7': Pawn('BLACK', 'e7', self), 'f7': Pawn('BLACK', 'f7', self),
            'g7': Pawn('BLACK', 'g7', self), 'h7': Pawn('BLACK', 'h7', self),

            # !! ----------------------------------- BOARD SPLIT ----------------------------------- !!

            'a2': Pawn('WHITE', 'a2', self), 'b2': Pawn('WHITE', 'b2', self),
            'c2': Pawn('WHITE', 'c2', self), 'd2': Pawn('WHITE', 'd2', self),
            'e2': Pawn('WHITE', 'e2', self), 'f2': Pawn('WHITE', 'f2', self),
            'g2': Pawn('WHITE', 'g2', self), 'h2': Pawn('WHITE', 'h2', self),
            'a1': Rook('WHITE', 'a1', self), 'b1': Knight('WHITE', 'b1', self),
            'c1': Bishop('WHITE', 'c1', self), 'd1': Queen('WHITE', 'd1', self),
            'e1': King('WHITE', 'e1', self), 'f1': Bishop('WHITE', 'f1', self),
            'g1': Knight('WHITE', 'g1', self), 'h1': Rook('WHITE', 'h1', self)
        }

    def display_board(self):
        """Displays a visual representation of the board and each piece's position using Unicode symbols."""
        display_board = [[' ' for _ in range(8)] for _ in range(8)]

        # build visual board from current piece positions in _init_pos
        for position, piece in self._init_pos.items():
            col, row = ChessGame.coord_to_index(position)
            # print(f"[{position}] {piece.__class__.__name__} ({piece.get_color()}) → {piece.unicode()}")
            display_board[row][col] = piece.unicode()

        print("   A B C D E F G H")
        row_num = 8
        for row in display_board:
            if row_num == 8:
                row_label = 'Black Home Rank'
            elif row_num in [7, 6, 5]:
                row_label = '-'
            elif row_num in [4, 3, 2]:
                row_label = '+'
            elif row_num == 1:
                row_label = 'White Home Rank'
            else:
                row_label = ''
            print(f"{row_num}| {' '.join(row)} | {row_label}")
            row_num -= 1
        print("   A B C D E F G H")

        if self._game_state == 'WHITE_WON':
            print("WHITE wins by capturing the BLACK king!")
        elif self._game_state == 'BLACK_WON':
            print("BLACK wins by capturing the WHITE king!")
        else:
            print(f"Player Move: {self._player_turn}")
        print(f"Game State: {self._game_state}\n")

    def get_game_state(self):
        """Returns the current game state: 'UNFINISHED,' 'WHITE_WON,' or 'BLACK_WON.'"""
        return self._game_state

    def set_game_state(self, game_state):
        """An extra method for setting game state when it needs to be updated based on player moves."""
        all_states = ['UNFINISHED', 'WHITE_WON', 'BLACK_WON']
        if game_state in all_states:
            self._game_state = game_state
        else:
            raise InvalidStateError

    def get_player_turn(self):
        return self._player_turn

    @staticmethod
    def coord_to_index(coord_str):
        """Converts chess notation (e.g., 'e2') into zero-indexed (col, row) coordinates for internal list access."""
        col = ord(coord_str[0].lower()) - 97
        row = 8 - int(coord_str[1:])
        return col, row

    @staticmethod
    def index_to_coord(col, row):
        """Converts indices back into coordinates again to complete a move."""
        letter_a_ascii = 97
        col_ascii = col + letter_a_ascii
        col_letter = chr(col_ascii)
        row = 7 - row
        row_num = str(row + 1)
        position = col_letter + row_num
        return position

    def make_move(self, move_from, move_to):
        if self._game_state != 'UNFINISHED':
            return False

        piece = self.get_piece(move_from)
        target_piece = self.get_piece(move_to)

        if not piece or piece.get_color() != self._player_turn:
            return False

        if not self.is_valid_move(move_from, move_to):
            print('That is not a valid move, please try again.')
            return False

        from_square = self.index_to_coord(*move_from)
        to_square = self.index_to_coord(*move_to)

        if isinstance(target_piece, King):
            self.set_game_state('WHITE_WON' if piece.get_color() == 'WHITE' else 'BLACK_WON')

        self._init_pos.pop(from_square)
        self._init_pos[to_square] = piece
        piece._position = to_square
        piece._init_move = False

        self.display_board()

        # only toggle turn if game is not over
        if self._game_state == 'UNFINISHED':
            self.toggle_turn()

        return True

    @staticmethod
    def parse_position(from_pos, to_pos):
        """Parses two coordinate strings like 'A2' and 'B3' into board indices (col, row)."""
        try:
            fcol, frow = ChessGame.coord_to_index(from_pos)
            tcol, trow = ChessGame.coord_to_index(to_pos)
            return (fcol, frow), (tcol, trow)
        except (ValueError, IndexError):
            print("Invalid move format. Please use something like A2 B3.")
            return None, None

    def is_valid_move(self, move_from, move_to):
        """This method will check whether a move is valid based on rules defined for a given piece. Also implements
        error-handling if the attempted "move from" square does not contain a piece, or a certain move is unavailable
        for a certain type of piece."""
        piece = self.get_piece(move_from)

        if piece is None:
            print("There is no piece at the starting square, please try again.")
            return False

        valid_moves = piece.valid_moves()
        target_square = self.index_to_coord(*move_to)

        if target_square not in valid_moves:
            print('That move is unavailable for the given piece, please try again.')
            return False

        return True

    def toggle_turn(self):
        """This method toggles the player turn. The game always starts with WHITE going first, and then switches
        after each move until the game has concluded."""
        if self._player_turn == 'WHITE':
            self._player_turn = 'BLACK'
        else:
            self._player_turn = 'WHITE'

    def get_piece(self, pos):
        """Returns the piece object at a given position. Accepts either (col, row) tuples or chess notation strings
        like 'e2'. Returns None if the square is empty."""

        if isinstance(pos, tuple):
            pos = self.index_to_coord(*pos)
        return self._init_pos.get(pos.lower())

    def is_square_open(self, position):
        """Basic check to see if a square is open or not"""
        position = position.lower()
        return position not in self._init_pos or self._init_pos[position] is None

    def is_opponent(self, position, color):
        """Checks if destination square is occupied by an opponent piece for potential capture"""
        piece = self.get_piece(position)
        if piece is None:
            return False
        return piece.get_color() != color  # return the one that isn't the current one == opponent


def main():
    """Main function starts game and allows for user to play through moves until a king is captured"""
    game = ChessGame()
    game.display_board()

    while game.get_game_state() == 'UNFINISHED':
        print(f'\n{game.get_player_turn()}\'s turn')
        curr_move = input('(Using the format a2 a4, as an example)\nPlease choose your next move: ').strip().split()
        move_from, move_to = game.parse_position(curr_move[0], curr_move[1])

        if move_from is None or move_to is None:
            continue

        is_valid = game.is_valid_move(move_from, move_to)

        if is_valid:
            game.make_move(move_from, move_to)


if __name__ == '__main__':
    main()
