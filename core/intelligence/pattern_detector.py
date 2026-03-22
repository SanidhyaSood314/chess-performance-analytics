from typing import List, Dict
from core.models.move_analysis_model import MoveAnalysis


def get_game_phase(move_number: int) -> str:
    if move_number <= 10:
        return "opening"
    elif move_number <= 30:
        return "middlegame"
    return "endgame"


def detect_error_patterns(
    analysis_data: List[MoveAnalysis],
    player_color: str
) -> Dict:
    """
    Analyze ONLY player's moves and return error distribution.
    """

    phases = {
        "opening": {"inaccurate": 0, "mistake": 0, "blunder": 0},
        "middlegame": {"inaccurate": 0, "mistake": 0, "blunder": 0},
        "endgame": {"inaccurate": 0, "mistake": 0, "blunder": 0},
    }

    totals = {"inaccurate": 0, "mistake": 0, "blunder": 0}

    for move in analysis_data:

        # ✅ FILTER: Only player's moves
        if not move.is_player_move(player_color):
            continue

        classification = move.classification

        if classification not in totals:
            continue

        phase = get_game_phase(move.move_number)

        phases[phase][classification] += 1
        totals[classification] += 1

    return {
        "phases": phases,
        "totals": totals,
    }