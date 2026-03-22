from typing import Dict, List


def generate_insights(patterns: Dict) -> List[str]:

    insights = []

    phases = patterns.get("phases", {})
    totals = patterns.get("totals", {})

    total_errors = sum(totals.values())

    if total_errors == 0:
        return ["Excellent! No significant mistakes detected in your moves."]

    phase_error_counts = {
        phase: sum(data.values())
        for phase, data in phases.items()
    }

    # Filter only phases with data
    valid_phases = {
        k: v for k, v in phase_error_counts.items() if v > 0
    }

    if valid_phases:
        worst_phase = max(valid_phases, key=valid_phases.get)
        best_phase = min(valid_phases, key=valid_phases.get)

        insights.append(
            f"Most of your mistakes occur in the {worst_phase}."
        )

        if worst_phase != best_phase:
            insights.append(
                f"You perform relatively better in the {best_phase}."
            )

    # Blunder focus
    blunders_by_phase = {
        phase: data.get("blunder", 0)
        for phase, data in phases.items()
    }

    if any(blunders_by_phase.values()):
        worst_blunder_phase = max(blunders_by_phase, key=blunders_by_phase.get)

        insights.append(
            f"Blunders are most frequent in the {worst_blunder_phase}."
        )

    blunders = totals.get("blunder", 0)
    mistakes = totals.get("mistake", 0)

    if blunders > mistakes:
        insights.append(
            "You tend to make high-impact mistakes more often than smaller ones."
        )
    elif mistakes > blunders:
        insights.append(
            "Most of your errors are moderate mistakes rather than blunders."
        )

    return insights