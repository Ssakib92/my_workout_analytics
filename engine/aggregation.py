import pandas as pd
from collections import defaultdict
from .config import DEFAULT_LOAD, SESSION_WINDOWS, EXERCISE_INTENT
from .core import compute_muscle_contribution, collapse_to_tier1


def last_n_sessions(log_df, n):
    log_df = log_df.copy()
    log_df["date"] = pd.to_datetime(log_df["date"])

    dates = sorted(log_df["date"].unique())[-n:]
    return log_df[log_df["date"].isin(dates)]


def aggregate_by_sessions(log_df, window_name="weekly"):
    n = SESSION_WINDOWS[window_name]
    window_df = last_n_sessions(log_df, n)

    fine = compute_muscle_contribution(window_df)
    return collapse_to_tier1(fine)


def routine_intensity_contribution(log_df):
    scores = defaultdict(float)

    for _, row in log_df.iterrows():
        scores[row["routine"]] += (
            row["sets"] * row["reps"] * DEFAULT_LOAD.get(row["exercise"], 1.0)
        )

    return pd.DataFrame(
        scores.items(),
        columns=["Routine", "Intensity Score"]
    )


def aggregate_routine_by_sessions(log_df, window_name="weekly"):
    n = SESSION_WINDOWS[window_name]
    return routine_intensity_contribution(last_n_sessions(log_df, n))


def exercise_wise_push_pull(log_df):
    push = pull = 0.0

    for _, row in log_df.iterrows():
        load = row["sets"] * row["reps"] * DEFAULT_LOAD.get(row["exercise"], 1.0)
        intent = EXERCISE_INTENT.get(row["exercise"], "neutral")

        if intent == "push":
            push += load
        elif intent == "pull":
            pull += load

    return push, pull
