import chess

# A wrapper class for the chess class with added functionalities.
# Initially created to also generate random endgame positions to train on, but due to time limitations we did not manage to finish this
class Board:
    # Creates a new board with the given position. If the position is left empty, a random endgame board is generated
    def __init__(self, position) -> None:
            self.board = chess.Board(position)

    # Returns the legal moves the current color can make
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

    def kings_distance(self) -> int:
        white_king_pos = self.board.pieces(chess.KING, chess.WHITE).pop()
        black_king_pos = self.board.pieces(chess.KING, chess.BLACK).pop()
        return chess.square_distance(white_king_pos, black_king_pos)

    def black_king_border_distance(self) -> int:
        black_king_pos = self.board.pieces(chess.KING, chess.BLACK).pop()
        black_king_file = chess.square_file(black_king_pos)
        black_king_rank = chess.square_rank(black_king_pos)
        return min(7-black_king_file, 7+black_king_file, 7+black_king_rank, 7-black_king_rank)
    
    def get_next_state(self, action) -> tuple:
        self.board.push(action)
        fen = self.state()
        self.board.pop()
        return fen

    def state(self) -> tuple:
        return (self.board.board_fen(), self.board.turn)

    def get_game_ended(self) -> bool:
        return self.board.is_game_over()

    