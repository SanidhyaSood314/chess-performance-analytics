from typing import Dict, List


def generate_recommendations(
    patterns: Dict,
    phase_analysis: Dict
) -> List[str]:
    """
    Generate actionable chess improvement suggestions.
    """

    recommendations = []

    phase_strength = phase_analysis.get("strength", {})
    phases = patterns.get("phases", {})
    totals = patterns.get("totals", {})

    # ---------------------------------
    # Phase-based recommendations
    # ---------------------------------

    for phase, strength in phase_strength.items():

        if strength == "weak":

            if phase == "opening":
                recommendations.append(
                    "Work on your opening fundamentals and avoid early inaccuracies."
                )

            elif phase == "middlegame":
                recommendations.append(
                    "Focus on middlegame tactics such as forks, pins, and discovered attacks."
                )

            elif phase == "endgame":
                recommendations.append(
                    "Improve your endgame technique, especially in basic king and pawn endings."
                )

    # ---------------------------------
    # Blunder-based recommendations
    # ---------------------------------

    total_blunders = totals.get("blunder", 0)
    total_mistakes = totals.get("mistake", 0)

    if total_blunders > 0:
        recommendations.append(
            "Try to reduce blunders by double-checking moves before playing."
        )

    if total_blunders > total_mistakes:
        recommendations.append(
            "Your mistakes are often severe. Focus on slowing down and evaluating positions carefully."
        )

    # ---------------------------------
    # Middlegame-heavy errors
    # ---------------------------------

    middlegame_errors = sum(phases.get("middlegame", {}).values())
    opening_errors = sum(phases.get("opening", {}).values())

    if middlegame_errors > opening_errors:
        recommendations.append(
            "You tend to struggle more in the middlegame—consider studying typical plans and structures."
        )

    # ---------------------------------
    # Fallback
    # ---------------------------------

    if not recommendations:
        recommendations.append(
            "Your play is quite balanced. Continue practicing to improve consistency."
        )

    return recommendations