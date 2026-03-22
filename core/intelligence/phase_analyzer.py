from typing import List, Dict
import math
from core.models.move_analysis_model import MoveAnalysis


def get_game_phase(move_number: int) -> str:
    if move_number <= 10:
        return "opening"
    elif move_number <= 30:
        return "middlegame"
    return "endgame"


def convert_to_accuracy(avg_loss: float) -> float:
    return 100 * math.exp(-avg_loss / 300)

def compute_cp_loss(best_eval, eval_after):

    if abs(best_eval) >= 9000 or abs(eval_after) >= 9000:
        return 1000

    loss = abs(best_eval - eval_after)
    return min(loss, 1000)

def analyze_phase_accuracy(
    analysis_data: List[MoveAnalysis],
    player_color: str
) -> Dict:

    phase_loss = {
        "opening": 0,
        "middlegame": 0,
        "endgame": 0
    }

    phase_moves = {
        "opening": 0,
        "middlegame": 0,
        "endgame": 0
    }

    for move in analysis_data:

        # ✅ FILTER: Only player's moves
        if not move.is_player_move(player_color):
            continue

        cp_loss = compute_cp_loss(move.best_eval, move.eval_after)

        phase = get_game_phase(move.move_number)

        phase_loss[phase] += cp_loss
        phase_moves[phase] += 1

    phase_accuracy = {}

    for phase in phase_loss:

        if phase_moves[phase] == 0:
            phase_accuracy[phase] = None  # ✅ FIX: No data
        else:
            avg_loss = phase_loss[phase] / phase_moves[phase]
            phase_accuracy[phase] = round(convert_to_accuracy(avg_loss), 2)

    def classify_strength(acc):
        if acc is None:
            return "no data"
        if acc >= 80:
            return "strong"
        elif acc >= 65:
            return "average"
        return "weak"

    phase_strength = {
        phase: classify_strength(acc)
        for phase, acc in phase_accuracy.items()
    }

    return {
        "accuracy": phase_accuracy,
        "strength": phase_strength
    }