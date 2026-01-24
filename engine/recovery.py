import numpy as np
import pandas as pd
import datetime
from .config import RECOVERY_TAU, AVG_SLEEP_HOURS
from .core import compute_muscle_contribution, collapse_to_tier1


def sleep_modifier(hours):
    if hours < 5:
        return 0.7
    if hours < 6:
        return 0.85
    if hours < 7:
        return 1.0
    if hours < 8:
        return 1.1
    return 1.2


def recovery_weight(days_ago, tau):
    return np.exp(-days_ago / tau)


def muscle_recovery_percentage_today(log_df, reference_date=None):
    if reference_date is None:
        reference_date = pd.to_datetime(datetime.date.today())

    recovery = {}
    tier1_groups = set(RECOVERY_TAU.keys())

    for muscle in tier1_groups:
        relevant = []

        for _, row in log_df.iterrows():
            fine = compute_muscle_contribution(pd.DataFrame([row]))
            tier1 = collapse_to_tier1(fine)

            if muscle in tier1["Muscle Group"].values:
                intensity = tier1.loc[
                    tier1["Muscle Group"] == muscle, "Intensity Score"
                ].values[0]
                relevant.append((row["date"], intensity))

        if not relevant:
            recovery[muscle] = 1.0
            continue

        last_date, _ = max(relevant, key=lambda x: x[0])
        days = (reference_date - last_date).days
        tau = RECOVERY_TAU[muscle] * sleep_modifier(AVG_SLEEP_HOURS)

        recovery[muscle] = 1 - np.exp(-days / tau)

    return pd.DataFrame(
        recovery.items(),
        columns=["Muscle Group", "Recovery"]
    )


def unified_muscle_readiness(log_df, alpha=1.5):
    rec = muscle_recovery_percentage_today(log_df).set_index("Muscle Group")["Recovery"]
    readiness = rec * np.exp(-alpha * (rec - 1) ** 2)

    return pd.DataFrame({
        "Recovery": rec.round(2),
        "Readiness Score": readiness.round(2)
    }).sort_values("Readiness Score")
