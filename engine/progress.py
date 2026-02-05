# engine/progress.py
import pandas as pd
from collections import defaultdict
from engine.config import DEFAULT_LOAD
from engine.core import compute_muscle_contribution
from engine.aggregation import (
    aggregate_by_sessions,
    aggregate_routine_by_sessions, 
    last_n_sessions, 
    routine_intensity_contribution
)



BASELINE_ROUTINE = {
    "push": 145,
    "pull": 131,
    "core": 124,
}

BASELINE_MUSCLE = {
    "Arms": 90,
    "Back": 75,
    "Core": 71,
    "Shoulders": 71.5,
    "Chest": 46,
    "Legs": 46.5,
}

FINAL_ROUTINES = {
    "pull": [
        ("Pull-up", 4, 6),
        ("One-arm DB Row", 4, 10),
        ("Bent-over DB Row", 2, 10),
        ("Rear Delt Fly", 2, 10),
        ("DB Shrug", 4, 10),
        ("Dead Hang", 3, 1),
        ("DB Curl", 3, 10),
        ("Hammer Curl", 2, 10),
    ],

    "push": [
        ("Incline DB Press", 4, 10),
        ("Decline Push-up", 4, 10),
        ("DB Shoulder Press", 3, 8),
        ("Lateral Raise", 4, 10),
        ("DB Triceps Extension", 3, 10),
        ("Diamond Push-up", 2, 10),
    ],

    "core": [
        ("Goblet Squat", 4, 10),
        ("Lunge", 3, 8),
        ("Glute Bridge", 3, 12),
        ("Hanging Knee Raise", 4, 8),
        ("Crunch", 2, 12),
        ("Leg Raise", 2, 10),
        ("Plank", 3, 1),
        ("Russian Twist", 2, 12),
        ("Burpee", 3, 5),
        ("Mountain Climber", 2, 10),
    ],
}

def compute_final_target():
    """
    Simulates final target routines as log entries
    and reuses existing aggregation logic.
    """

    rows = []

    for routine, exercises in FINAL_ROUTINES.items():
        for ex, sets, reps in exercises:
            rows.append({
                "date": "2099-01-01",  # dummy date (single session)
                "routine": routine,
                "exercise": ex,
                "sets": sets,
                "reps": reps,
            })

    final_df = pd.DataFrame(rows)

    # Reuse canonical aggregation
    muscle_df = aggregate_by_sessions(final_df, window_name="weekly")
    routine_df = aggregate_routine_by_sessions(final_df, window_name="weekly")

    muscle_scores = dict(
        zip(muscle_df["Muscle Group"], muscle_df["Intensity Score"])
    )

    routine_scores = dict(
        zip(routine_df["Routine"], routine_df["Intensity Score"])
    )

    return muscle_scores, routine_scores

def compute_current_from_logs(log_df):
    """
    Uses last 3 sessions (weekly window)
    """
    muscle_df = aggregate_by_sessions(log_df, window_name="weekly")
    routine_df = aggregate_routine_by_sessions(log_df, window_name="weekly")

    # Convert to dicts for easier comparison
    muscle_scores = dict(
        zip(muscle_df["Muscle Group"], muscle_df["Intensity Score"])
    )

    routine_scores = dict(
        zip(routine_df["Routine"], routine_df["Intensity Score"])
    )

    return muscle_scores, routine_scores


def progress_ratio(current, baseline, final):
    if final <= baseline:
        progress = 1.0 if current >= final else 0.0
    else:
        progress = (current - baseline) / (final - baseline)

    return {
        "delta_from_baseline": current - baseline,
        "progress_to_final": max(0.0, min(progress, 1.0))
    }

def routine_progress_series(log_df, baseline_routine, window=3):
    """
    Returns a DataFrame with:
    date | push | pull | core
    where values = (current - baseline)
    """

    log_df = log_df.copy()
    log_df["date"] = pd.to_datetime(log_df["date"])

    dates = sorted(log_df["date"].unique())

    rows = []

    for i in range(window - 1, len(dates)):
        window_dates = dates[i - window + 1 : i + 1]
        window_df = log_df[log_df["date"].isin(window_dates)]

        routine_df = routine_intensity_contribution(window_df)

        lookup = dict(
            zip(routine_df["Routine"], routine_df["Intensity Score"])
        )

        rows.append({
            "date": dates[i],
            "push": lookup.get("push", 0.0) - baseline_routine["push"],
            "pull": lookup.get("pull", 0.0) - baseline_routine["pull"],
            "core": lookup.get("core", 0.0) - baseline_routine["core"],
        })

    return pd.DataFrame(rows)
