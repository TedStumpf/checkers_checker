#   board.py
#   Theodore Stumpf
#   A game board representing a game of checkers
from random import random as rand
from random import choice
from lin_analyzer import LinearAnalyzer

#   Constants for data management
_PIECE_INVALID = 0
_PIECE_EMPTY = 1
_PIECE_RED_MAN = 2
_PIECE_RED_KING = 3
_PIECE_BLACK_MAN = 4
_PIECE_BLACK_KING = 5

_PLAYER_NONE = 0
_PLAYER_RED = 1
_PLAYER_BLACK = 2

#   The GameBoard class
class GameBoard():

    #   __init__():  Initialize the GameBoard
    #   starting_player: The starting player for the game
    #       if set to none, the player will be chosen at random
    def __init__(self, starting_player = _PLAYER_NONE):
        #   Create the empty board
        self.board = [[_PIECE_EMPTY for col in range(8)] for row in range(8)]

        for row in range(8):
            for col in range(8):
                if ((row + col) % 2 == 0):  #   Mark off squares as invalid
                    self.set_position_raw(row, col, _PIECE_INVALID)
                elif (row < 3): #   Add staring squares for red
                    self.set_position_raw(row, col, _PIECE_RED_MAN)
                elif (row > 4): #   Add staring squares for black
                    self.set_position_raw(row, col, _PIECE_BLACK_MAN)

        #   Pick or set the starting player
        if (starting_player == _PLAYER_NONE):
            self.player = choice((_PLAYER_RED, _PLAYER_BLACK))
        else:
            self.player = starting_player

        #   Initialize other vars
        self.forced_move = None
        self.base_analyzer = LinearAnalyzer()


    #   get_position_raw(): Returns the value of a square on the board
    #   row, col: The positon on the board
    def get_position_raw(self, row, col):
        return self.board[row][col]

    #   set_position_raw(): Sets the value of a square on the board to the given value
    #   row, col: The positon on the board
    #   value: The value to set the 
    def set_position_raw(self, row, col, value):
        self.board[row][col] = value

    #   get_position(): Returns the value of a square on the board
    #   row, col: The positon on the board
    def get_position(self, row, col):
        if not self.is_valid(row, col):
            return _PIECE_INVALID
        return self.get_position_raw(row, col)

    #   is_valid(): Returns if the position on the board is valid
    #   row, col: The positon on the board
    def is_valid(self, row, col):
        if ((row < 0) or (row >= 8) or (col < 0) or (col >= 8) or (self.get_position_raw(row, col) == _PIECE_INVALID)):
            return False
        return True

    #   is_red(): Returns if the position on the board is red
    #   row, col: The positon on the board
    def is_red(self, row, col):
        return ((self.get_position(row, col) == _PIECE_RED_MAN) or (self.get_position(row, col) == _PIECE_RED_KING))

    #   is_black(): Returns if the position on the board is black
    #   row, col: The positon on the board
    def is_black(self, row, col):
        return ((self.get_position(row, col) == _PIECE_BLACK_MAN) or (self.get_position(row, col) == _PIECE_BLACK_KING))

    #   is_empty(): Returns if the given board position is empty
    #   row, col: The positon on the board
    def is_empty(self, row, col):
        return (self.get_position(row, col) == _PIECE_EMPTY)

    #   is_ally(): Returns if the piece is allied to the current player
    #   row, col: The positon on the board
    def is_ally(self, row, col):
        if (self.player == _PLAYER_RED):
            return self.is_red(row, col)
        else:
            return self.is_black(row, col)

    #   is_opponent(): Returns if the piece is opposing to the current player
    #   row, col: The positon on the board
    def is_opponent(self, row, col):
        if (self.player == _PLAYER_BLACK):
            return self.is_red(row, col)
        else:
            return self.is_black(row, col)

    #   is_owned(): Returns if the piece belongs to the given player
    #   row, col: The positon on the board
    #   player:   The player to compare to
    def is_owned(self, row, col, player):
        if ((player == _PLAYER_BLACK) and ((self.get_position(row, col) == _PIECE_BLACK_MAN) or (self.get_position(row, col) == _PIECE_BLACK_KING))):
            return True
        if ((player == _PLAYER_RED) and ((self.get_position(row, col) == _PIECE_RED_MAN) or (self.get_position(row, col) == _PIECE_RED_KING))):
            return True
        return False

    #   is_not_owned(): Returns if the piece does not belong to the given player
    #   row, col: The positon on the board
    #   player:   The player to compare to
    def is_not_owned(self, row, col, player):
        if ((player == _PLAYER_RED) and ((self.get_position(row, col) == _PIECE_BLACK_MAN) or (self.get_position(row, col) == _PIECE_BLACK_KING))):
            return True
        if ((player == _PLAYER_BLACK) and ((self.get_position(row, col) == _PIECE_RED_MAN) or (self.get_position(row, col) == _PIECE_RED_KING))):
            return True
        return False

    #   is_king(): Returns if the piece is a king
    #   row, col: The positon on the board
    def is_king(self, row, col):
        return ((self.get_position(row, col) == _PIECE_RED_KING) or (self.get_position(row, col) == _PIECE_BLACK_KING))

    #   get_winner(): returns if a current player has won
    def get_winner(self):
        if (len(self.get_vaild_moves()) == 0):
            if (self.player == _PLAYER_RED):
                return _PLAYER_BLACK
            else:
                return _PLAYER_RED
        return _PLAYER_NONE


    #   get_vaild_moves(): Returns all the valid moves
    #   row, col: The positon on the board
    def get_vaild_moves(self):
        out = []
        for row in range(8):
            for col in range(8):
                out += self.get_valid_moves_for_pos(row, col)

        # Filter for jumps
        only_jumps = [ent for ent in out if ent[4]]
        if (len(only_jumps) > 0):
            return only_jumps

        return out

    #   get_valid_moves_for_pos(): Returns the valid moves for the given position
    #   row, col: The positon on the board
    def get_valid_moves_for_pos(self, row, col, with_jumps = False):
        out = []
        if (self.is_ally(row, col) and ((self.forced_move == None) or (self.forced_move == (row, col)))):
            if (self.is_red(row, col) or (self.get_position(row, col) == _PIECE_BLACK_KING)):
                #   Moving down the board
                #   To the left
                if self.is_empty(row + 1, col - 1):
                    out.append((row, col, row + 1, col - 1, False))
                elif (self.is_opponent(row + 1, col - 1) and self.is_empty(row + 2, col - 2)):
                    out.append((row, col, row + 2, col - 2, True))

                #   To the right
                if self.is_empty(row + 1, col + 1):
                    out.append((row, col, row + 1, col + 1, False))
                elif (self.is_opponent(row + 1, col + 1) and self.is_empty(row + 2, col + 2)):
                    out.append((row, col, row + 2, col + 2, True))
            if (self.is_black(row, col) or (self.get_position(row, col) == _PIECE_RED_KING)):
                #   Moving up the board
                #   To the left
                if self.is_empty(row - 1, col - 1):
                    out.append((row, col, row - 1, col - 1, False))
                elif (self.is_opponent(row - 1, col - 1) and self.is_empty(row - 2, col - 2)):
                    out.append((row, col, row - 2, col - 2, True))

                #   To the right
                if self.is_empty(row - 1, col + 1):
                    out.append((row, col, row - 1, col + 1, False))
                elif (self.is_opponent(row - 1, col + 1) and self.is_empty(row - 2, col + 2)):
                    out.append((row, col, row - 2, col + 2, True))
        
        #   Remove non jumps
        if with_jumps:
            out = [ent for ent in out if ent[4]]

        #   Return the list of moves
        return out

    #   make_move():
    #   from_row, from_col: The position of the the piece to move
    #   to_row, to_col: The position to move the piece to
    #   is_jumping: If the piece is jumping
    def make_move(self, from_row, from_col, to_row, to_col, is_jumping):
        #   Return False if either position is invalid
        if (not (self.is_valid(from_row, from_col) or self.is_valid(to_row, to_col))):
            return False

        #   Return False if the to position is not empty
        if (not self.is_empty(to_row, to_col)):
            return False

        #   Return False if the position does not belong to the current player
        if (not self.is_ally(from_row, from_col)):
            return False

        #   Jump
        if (is_jumping):
            jump_row = from_row + (to_row - from_row) // 2
            jump_col = from_col + (to_col - from_col) // 2
            if ((jump_row == from_row) or (jump_col == from_col) or (not self.is_opponent(jump_row, jump_col))):
                return False

            self.set_position_raw(jump_row, jump_col, _PIECE_EMPTY)

        #   Move the piece
        self.set_position_raw(to_row, to_col, self.get_position_raw(from_row, from_col))
        self.set_position_raw(from_row, from_col, _PIECE_EMPTY)

        #   King piece if it is at the end
        if ((to_row == 7) and (self.get_position_raw(to_row, to_col) == _PIECE_RED_MAN)):
            self.set_position_raw(to_row, to_col, _PIECE_RED_KING)
        if ((to_row == 0) and (self.get_position_raw(to_row, to_col) == _PIECE_BLACK_MAN)):
            self.set_position_raw(to_row, to_col, _PIECE_BLACK_KING)

        #   Update the player turn
        self.forced_move = None
        if (is_jumping and (len(self.get_valid_moves_for_pos(to_row, to_col, True)) > 0)):
            self.forced_move = (to_row, to_col)
        else:
            if (self.player == _PLAYER_RED):
                self.player = _PLAYER_BLACK
            else:
                self.player = _PLAYER_RED

        #   Return True if successful
        return True

    #   score_board(): Scores the board from the perspective of a given player
    #   player: The player to get the perspective of
    #   lin_anl:       The linear analyzer to use
    def score_board(self, player, lin_anl = None):
        winner = self.get_winner()
        if (winner == player):
            return 1000000
        elif (winner != _PLAYER_NONE):
            return -1000000
        else:
            if (lin_anl == None):
                lin_anl = self.base_analyzer
            score = 0
            for row in range(8):
                for col in range(8):
                    if (self.is_owned(row, col, player)):
                        score += lin_anl.get_piece(True, self.is_king(row, col)) * lin_anl.get_square_value(row, col)
                    elif (self.is_not_owned(row, col, player)):
                        score -= lin_anl.get_piece(False, self.is_king(row, col)) * lin_anl.get_square_value(row, col)
            return score

    #   console_print(): Print the console to current state of the board
    def console_print(self):
        print("Current Player: " + ("None", "Red", "Black")[self.player])
        print("Current Score:", round(self.score_board(self.player) * 100) / 100)
        for row in range(8):
            for col in range(8):
                print(" .rRbB"[self.get_position(row, col)], end = "")
            print()
        print()

#   Testing function
def test():
    board = GameBoard()
    print("#" * 30)
    while (board.get_winner() == _PLAYER_NONE):
        board.console_print()
        all_moves = board.get_vaild_moves()
        print(all_moves)
        move = choice(all_moves)
        print("Making move: ", move)
        board.make_move(move[0], move[1], move[2], move[3], move[4])
        input()
    board.console_print()

if __name__ == '__main__':
    test()