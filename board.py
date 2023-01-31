import chess
import random

# A wrapper class for the chess class with added functionalities.
class Board:
    # Creates a new board with one of the two starting positions chosen at random
    def __init__(self) -> None:
            self.board = chess.Board(random.choice(["8/8/8/2k5/8/6R1/3K4/8", "8/8/8/2k5/8/2K3Q1/8/8"]))

    # Returns a list with the legal moves the current player can make
    def legal_moves(self) -> list:
        return list(self.board.legal_moves)

    # Makes the given move and returns the outcome
    def make_move(self, move) -> str:
        self.board.push(move)
        return self.board.result()

    # Prints the board to the terminal
    def print_board(self):
        print(self.board)
        print("")

    # Returns the step distance between the two kings
    def kings_distance(self) -> int:
        white_king_pos = self.board.pieces(chess.KING, chess.WHITE).pop()
        black_king_pos = self.board.pieces(chess.KING, chess.BLACK).pop()
        return chess.square_distance(white_king_pos, black_king_pos)

    # Returns the step distance between the black king and the nearest border
    def black_king_border_distance(self) -> int:
        black_king_pos = self.board.pieces(chess.KING, chess.BLACK).pop()
        black_king_file = chess.square_file(black_king_pos)
        black_king_rank = chess.square_rank(black_king_pos)
        return min(7-black_king_file, 7+black_king_file, 7+black_king_rank, 7-black_king_rank)

    # Returns the state of the board, which is represented as a tuple of the FEN string and player at turn
    def state(self) -> tuple:
        return (self.board.board_fen(), self.board.turn)    