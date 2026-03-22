from typing import Dict, List


def generate_game_report(
    player_color: str,
    phase_analysis: Dict,
    insights: List[str],
    recommendations: List[str]
) -> str:
    """
    Generate a clean, human-readable game summary report.
    """

    report_parts = []

    # ---------------------------------
    # Player context
    # ---------------------------------
    report_parts.append(f"You played as {player_color}.")

    # ---------------------------------
    # Phase summary
    # ---------------------------------
    accuracy = phase_analysis.get("accuracy", {})
    strength = phase_analysis.get("strength", {})

    phase_sentences = []

    for phase in ["opening", "middlegame", "endgame"]:

        acc = accuracy.get(phase)
        strg = strength.get(phase)

        if acc is None:
            continue

        phase_sentences.append(
            f"{phase} ({acc}% - {strg})"
        )

    if phase_sentences:
        report_parts.append(
            "Your phase performance: " + ", ".join(phase_sentences) + "."
        )

    # ---------------------------------
    # Key insight (top one)
    # ---------------------------------
    if insights:
        report_parts.append(insights[0])

    # ---------------------------------
    # Recommendations (top 1–2)
    # ---------------------------------
    if recommendations:
        rec_text = " ".join(recommendations[:2])
        report_parts.append("Recommendation: " + rec_text)

    # ---------------------------------
    # Final overall conclusion
    # ---------------------------------

    weak_phases = [
        phase for phase, s in strength.items() if s == "weak"
    ]

    if weak_phases:
        report_parts.append(
            f"Overall, your play is strong in other phases but needs improvement in the {', '.join(weak_phases)}."
        )

    # ---------------------------------
    # Final report
    # ---------------------------------
    return "\n\n".join(report_parts)