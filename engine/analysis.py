from engine.config import MUSCLE_COLLAPSE_MAP


def imbalance_flags(tier1_df, threshold=1.8):
    avg = tier1_df["Normalized"].mean()

    tier1_df["Status"] = tier1_df["Normalized"].apply(
        lambda x: "Overused" if x > threshold * avg
        else "Undertrained" if x < 0.6 * avg
        else "Balanced"
    )

    return tier1_df


def coverage_completeness_score(fine_scores, target_group):
    """
    Percentage of fine muscles within a Tier-1 group
    that received non-zero stimulus.
    """

    fine_muscles = [
        m for m, g in MUSCLE_COLLAPSE_MAP.items()
        if g == target_group
    ]

    if not fine_muscles:
        return 0.0

    trained = sum(
        1 for m in fine_muscles
        if fine_scores.get(m, 0) > 0
    )

    return trained / len(fine_muscles) * 100
