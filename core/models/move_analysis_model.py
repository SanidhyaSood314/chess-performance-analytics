import chess
from dataclasses import dataclass


@dataclass
class MoveAnalysis:
    """
    Structured representation of a move analysis result.
    """

    move: chess.Move
    move_number: int
    is_white_move: bool

    eval_before: float
    eval_after: float

    best_move: chess.Move
    best_eval: float

    classification: str

    # ---------------------------------
    # NEW: Helper to check player move
    # ---------------------------------

    def is_player_move(self, player_color: str) -> bool:
        """
        Returns True if this move belongs to the given player.
        player_color: "White" or "Black"
        """
        if player_color == "White":
            return self.is_white_move
        return not self.is_white_move