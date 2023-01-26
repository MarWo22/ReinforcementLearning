import chess
import random


# A wrapper class for the chess class with added functionalities.
class Board:
    # Creates a new board with the given position. If the position is left empty, a random endgame board is generated
    def __init__(self, position) -> None:
        if position == None:
            self.board = self._generateRandomBoard(3)
        else:
            self.board = chess.Board(position)


    # Generates a random valid board of size n_pieces. n_pieces needs to be atleast 2 for a valid board (kings for both sides). 
    # All remaining pieces are randomly chosen and placed
    # This solution is not the most efficient, and will not work well for large boards, since it brute-forces a valid board
    # However, for endgame solutions, this is sufficient
    # Note that this is not very realistic, since most of these random boards will never occur on real chess games
    def _generateRandomBoard(self, n_pieces) -> chess.Board:
        # All squares on the board
        positions = list(range(0, 64))
        # All possible pieces for each color (excluding the king)
        pieces_white = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
        pieces_black = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5]

        # Create an empty board
        board = chess.Board(None)
        #Pick a random position from the list
        position = random.choice(positions)
        positions.remove(position)
        #Place the black king on that position
        board.set_piece_at(position, chess.Piece(chess.PieceType(6), chess.BLACK))
        
        #Repeat for white king
        position = random.choice(positions)
        positions.remove(position)
        board.set_piece_at(position, chess.Piece(chess.PieceType(6), chess.WHITE))
        # Check if the game is not in a stalemate or checkmate
        if board.is_stalemate() or board.is_checkmate():
            return self._generateRandomBoard(n_pieces)

        # Place the remaining pieces on the board
        for _ in range(2, n_pieces):
            position = random.choice(positions)
            positions.remove(position)

            # Grab a color for the piece to place
            if len(pieces_white) == 0 and len(pieces_white) > 0:
                color = False
            elif len(pieces_white) > 0 and len(pieces_black) == 0:
                color = True
            else:
                color = random.choice([True, False])

            # Pick the piece from the list of the respective color
            if color:
                piece = random.choice(pieces_white)
                pieces_white.remove(piece)
            else:
                piece = random.choice(pieces_black)
                pieces_black.remove(piece)

            # Place the piece on the board
            board.set_piece_at(position, chess.Piece(piece, color))

            # Makes sure the board is not in a game-over state
            if board.is_game_over():
                return self._generateRandomBoard(n_pieces)
        return board

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

    def kings_distance(self):
        white_king_pos = self.board.pieces(6, True).pop()
        black_king_pos = self.board.pieces(6, False).pop()
        return chess.square_distance(white_king_pos, black_king_pos)

    def black_king_border_distance(self):
        black_king_pos = self.board.pieces(6, False).pop()
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

    