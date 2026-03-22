# core/engine/game_analyzer.py

import chess
import chess.pgn
import chess.engine
import io
from typing import List

from core.engine.engine_manager import get_engine
from core.models.move_analysis_model import MoveAnalysis


class GameAnalyzer:
    """
    Encapsulates all engine analysis logic for a chess game.
    """

    def __init__(self, depth: int = 12):
        self.engine = get_engine()
        self.depth = depth

    # -------------------------------------------------
    # Move Classification
    # -------------------------------------------------

    def classify_move(
        self,
        eval_before,
        best_eval,
        player_eval,
        played_move,
        best_move,
        is_white_move
    ):

        if not is_white_move:
            eval_before = -eval_before
            best_eval = -best_eval
            player_eval = -player_eval

        loss = best_eval - player_eval
        improvement = player_eval - eval_before

        if played_move == best_move:
            if improvement > 150:
                return "brilliant"
            return "best"

        if loss <= 30:
            return "great"
        elif loss <= 120:
            return "normal"
        elif loss <= 250:
            return "inaccurate"
        elif loss <= 450:
            return "mistake"
        else:
            return "blunder"

    # -------------------------------------------------
    # Safe Evaluation Extraction
    # -------------------------------------------------

    def _get_eval(self, info):

        score = info.get("score")

        if score is None:
            return 0

        score = score.white()

        if score.is_mate():
            return 10000 if score.mate() > 0 else -10000

        value = score.score()

        return value if value is not None else 0

    # -------------------------------------------------
    # Game Analysis
    # -------------------------------------------------

    def analyze_game(self, pgn_string: str) -> List[MoveAnalysis]:

        game = chess.pgn.read_game(io.StringIO(pgn_string))
        moves = list(game.mainline_moves())

        board = chess.Board()

        analysis: List[MoveAnalysis] = []

        # Initial evaluation
        info = self.engine.analyse(
            board,
            chess.engine.Limit(depth=self.depth)
        )

        eval_before = self._get_eval(info)

        for move in moves:

            is_white_move = board.turn

            multipv_info = self.engine.analyse(
                board,
                chess.engine.Limit(depth=self.depth),
                multipv=2
            )

            best_line = multipv_info[0]

            best_move = best_line["pv"][0]

            best_eval = self._get_eval(best_line)

            board.push(move)

            info_after = self.engine.analyse(
                board,
                chess.engine.Limit(depth=self.depth)
            )

            player_eval = self._get_eval(info_after)

            classification = self.classify_move(
                eval_before,
                best_eval,
                player_eval,
                move,
                best_move,
                is_white_move
            )

            analysis.append(
                MoveAnalysis(
                    move=move,
                    move_number=(len(analysis) // 2) + 1,
                    is_white_move=is_white_move,
                    eval_before=eval_before,
                    eval_after=player_eval,
                    best_move=best_move,
                    best_eval=best_eval,
                    classification=classification
                )
            )

            eval_before = player_eval

        return analysis