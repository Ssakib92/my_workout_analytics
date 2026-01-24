from collections import defaultdict
import pandas as pd
from .config import EXERCISE_LIBRARY, DEFAULT_LOAD, MUSCLE_COLLAPSE_MAP


def compute_muscle_contribution(log_df):
    scores = defaultdict(float)

    for _, row in log_df.iterrows():
        exercise = row["exercise"]
        base = row["sets"] * row["reps"] * DEFAULT_LOAD.get(exercise, 1.0)

        for muscle, weight in EXERCISE_LIBRARY[exercise]["muscles"].items():
            scores[muscle] += base * weight

    return scores


def collapse_to_tier1(fine_scores):
    tier1 = defaultdict(float)

    for muscle, score in fine_scores.items():
        tier1[MUSCLE_COLLAPSE_MAP[muscle]] += score

    return pd.DataFrame(
        tier1.items(),
        columns=["Muscle Group", "Intensity Score"]
    ).sort_values("Intensity Score", ascending=False)


def muscle_coverage_report(fine_scores, target_group):
    covered = {
        m: fine_scores.get(m, 0.0)
        for m, g in MUSCLE_COLLAPSE_MAP.items()
        if g == target_group
    }

    return pd.DataFrame(
        covered.items(),
        columns=["Fine Muscle", "Intensity Score"]
    ).sort_values("Intensity Score", ascending=False)
