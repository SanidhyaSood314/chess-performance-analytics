import chess
import chess.pgn
import io


OPENING_BOOK = {
    ("e4", "c5"): ("Sicilian Defense", ""),
    ("e4", "e5", "Nf3", "Nc6", "Bb5"): ("Ruy Lopez", ""),
    ("e4", "e5", "Nf3", "Nc6", "Bc4"): ("Italian Game", ""),
    ("d4", "d5", "c4"): ("Queen's Gambit", ""),
    ("d4", "Nf6", "c4", "g6"): ("King's Indian Defense", ""),
}


def detect_opening(pgn_string):

    game = chess.pgn.read_game(io.StringIO(pgn_string))
    board = game.board()

    moves = []

    for move in game.mainline_moves():

        san = board.san(move)
        moves.append(san)
        board.push(move)

        if len(moves) >= 6:
            break

    for sequence, opening in OPENING_BOOK.items():

        if tuple(moves[:len(sequence)]) == sequence:

            # Ensure exactly two values returned
            opening_name = opening[0]
            variation = opening[1] if len(opening) > 1 else ""

            return opening_name, variation

    return "Unknown Opening", ""