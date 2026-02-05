import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from logger import load_history

# ---- CORE ----
from engine.core import (
    compute_muscle_contribution,
    collapse_to_tier1,
    muscle_coverage_report
)

# ---- AGGREGATION ----
from engine.aggregation import (
    aggregate_by_sessions,
    aggregate_routine_by_sessions,
    exercise_wise_push_pull
)

# ---- RECOVERY ----
from engine.recovery import (
    unified_muscle_readiness
)

# ---- ANALYSIS ----
from engine.analysis import (
    imbalance_flags,
    coverage_completeness_score
)

# ---- Progress ----
from engine.progress import (
    BASELINE_ROUTINE,
    BASELINE_MUSCLE,
    compute_final_target,
    compute_current_from_logs,
    progress_ratio,
    routine_progress_series
)

BODYWEIGHT_KG = 63


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Workout Analytics Dashboard",
    layout="wide"
)

st.title("🏋️ Workout Analytics Dashboard")
st.caption("Relative muscle load • balance • readiness • routine overload")


# ==============================
# LOAD DATA
# ==============================

history = load_history()

if history.empty:
    st.warning("No workout data found. Log workouts first.")
    st.stop()

history["date"] = pd.to_datetime(
    history["date"],
    format="mixed",
    errors="coerce"
)


# ==============================
# SIDEBAR FILTERS
# ==============================

st.sidebar.header("Filters")

date_range = st.sidebar.date_input(
    "Select date range",
    [history["date"].min(), history["date"].max()]
)

if len(date_range) != 2:
    st.stop()

filtered = history[
    (history["date"] >= pd.to_datetime(date_range[0])) &
    (history["date"] <= pd.to_datetime(date_range[1]))
]

st.sidebar.markdown(f"**Sessions:** {filtered['date'].nunique()}")


# ==============================
# MUSCLE CONTRIBUTION
# ==============================

fine_scores = compute_muscle_contribution(filtered)
tier1_df = collapse_to_tier1(fine_scores)

tier1_df["Normalized"] = tier1_df["Intensity Score"] / BODYWEIGHT_KG


# ==============================
# MAIN LAYOUT
# ==============================

col1, col2 = st.columns([1.15, 1])

# ---------- TABLE ----------
with col1:
    st.subheader("Tier-1 Muscle Contribution")

    st.dataframe(
        tier1_df,
        use_container_width=True
    )

    imbalance_df = imbalance_flags(tier1_df.copy())

    st.subheader("⚠️ Imbalance Detection")
    st.dataframe(
        imbalance_df[["Muscle Group", "Normalized", "Status"]],
        use_container_width=True
    )

# ---------- RADAR ----------
with col2:
    st.subheader("Muscle Balance Radar")

    labels = tier1_df["Muscle Group"].tolist()
    values = tier1_df["Normalized"].tolist()

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    values += values[:1]
    angles = np.append(angles, angles[0])

    fig = plt.figure(figsize=(5, 5))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("Relative Muscle Balance")

    st.pyplot(fig)


# ==============================
# SUB-MUSCLE COVERAGE
# ==============================

st.divider()
st.subheader("🔍 Sub-Muscle Coverage")

target_group = st.selectbox(
    "Select muscle group",
    tier1_df["Muscle Group"].tolist()
)

coverage_df = muscle_coverage_report(fine_scores, target_group)

if coverage_df.empty:
    st.info("No sub-muscle data.")
else:
    st.dataframe(coverage_df, use_container_width=True)

coverage_pct = coverage_completeness_score(
    fine_scores,
    target_group
)

st.metric(
    f"{target_group} Coverage",
    f"{coverage_pct:.0f}%",
    help="Sub-muscles activated at least once"
)


# ==============================
# BALANCE RATIOS
# ==============================

st.divider()
st.subheader("⚖️ Training Balance Ratios")

def ratio(a, b):
    return a / b if b > 0 else np.nan

lookup = dict(
    zip(
        tier1_df["Muscle Group"],
        tier1_df["Normalized"]
    )
)

# Muscle-wise (fatigue)
push_m = lookup.get("Chest", 0) + lookup.get("Shoulders", 0) + lookup.get("Arms", 0)
pull_m = lookup.get("Back", 0)

upper = push_m + pull_m
lower = lookup.get("Legs", 0) + lookup.get("Core", 0)

# Exercise-wise (programming)
push_e, pull_e = exercise_wise_push_pull(filtered)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Push / Pull (Muscle-wise)",
    f"{ratio(push_m, pull_m):.2f}",
    help="Fatigue & injury balance"
)

c2.metric(
    "Push / Pull (Exercise-wise)",
    f"{ratio(push_e, pull_e):.2f}",
    help="Programming balance"
)

c3.metric(
    "Upper / Lower",
    f"{ratio(upper, lower):.2f}",
    help="Structural balance"
)


# ==============================
# MUSCLE READINESS
# ==============================

st.divider()
st.subheader("🧠 Muscle Readiness")

readiness_df = unified_muscle_readiness(filtered)

st.dataframe(readiness_df, use_container_width=True)

for muscle, row in readiness_df.iterrows():
    score = row["Readiness Score"]

    if score < 0.4:
        st.error(f"{muscle}: Avoid loading")
    elif score < 0.6:
        st.warning(f"{muscle}: Light work")
    elif score < 0.8:
        st.info(f"{muscle}: Moderate volume")
    else:
        st.success(f"{muscle}: Fully ready")


# ==============================
# SESSION-BASED AGGREGATION
# ==============================

st.divider()
aggregation_mode = st.selectbox(
    "Aggregation window",
    ["Last 3 Sessions", "Last 12 Sessions"]
)

mode_map = {
    "Last 3 Sessions": "weekly",
    "Last 12 Sessions": "monthly"
}

st.subheader(f"📊 {aggregation_mode} — Muscle Contribution")

agg_df = aggregate_by_sessions(
    filtered,
    window_name=mode_map[aggregation_mode]
)

agg_df["Normalized"] = agg_df["Intensity Score"] / BODYWEIGHT_KG

st.dataframe(agg_df, use_container_width=True)


# ==============================
# ROUTINE OVERLOAD (NEW)
# ==============================

st.subheader(f"🏗 {aggregation_mode} — Routine Intensity")

routine_df = aggregate_routine_by_sessions(
    filtered,
    window_name=mode_map[aggregation_mode]
)

routine_df["Normalized"] = routine_df["Intensity Score"] / BODYWEIGHT_KG

st.dataframe(routine_df, use_container_width=True)


# ==============================
# FOOTER
# ==============================

st.caption(
    "All scores represent relative training stimulus. "
    "Not absolute force, hypertrophy, or calories."
)

# ==============================
# PROGRESS: BASELINE → CURRENT → FINAL
# ==============================

final_muscle, final_routine = compute_final_target()
current_muscle, current_routine = compute_current_from_logs(filtered)

st.divider()
st.subheader("📊 Muscle Intensity — Baseline vs Current vs Final")

muscle_rows = []

for muscle in final_muscle:
    baseline = BASELINE_MUSCLE.get(muscle, 0.0)
    current = current_muscle.get(muscle, 0.0)
    final = final_muscle[muscle]

    muscle_rows.append({
        "Muscle": muscle,
        "Baseline": round(baseline, 1),
        "Current": round(current, 1),
        "Final": round(final, 1),
        "Δ vs Baseline": round(current - baseline, 1),
        "% Progress": round(
            ((current - baseline) / (final - baseline)) * 100
            if final > baseline else 100.0,1)
    })

muscle_progress_df = pd.DataFrame(muscle_rows).sort_values(
    "% Progress", ascending=False
)

st.dataframe(muscle_progress_df, use_container_width=True)

st.subheader("📊 Routine Intensity — Baseline vs Current vs Final")

routine_rows = []

for routine in final_routine:
    baseline = BASELINE_ROUTINE.get(routine, 0.0)
    current = current_routine.get(routine, 0.0)
    final = final_routine[routine]

    routine_rows.append({
        "Routine": routine.upper(),
        "Baseline": round(baseline, 1),
        "Current": round(current, 1),
        "Final": round(final, 1),
        "Δ vs Baseline": round(current - baseline, 1),
        "% Progress": round(
            ((current - baseline) / (final - baseline)) * 100
            if final > baseline else 100.0,1)
    })

routine_progress_df = pd.DataFrame(routine_rows).sort_values(
    "% Progress", ascending=False
)

st.dataframe(routine_progress_df, use_container_width=True)

st.divider()
st.subheader("📈 Routine Progression (Δ from Baseline)")

progress_df = routine_progress_series(
    filtered,
    BASELINE_ROUTINE,
    window=3
)

if progress_df.empty:
    st.info("Not enough sessions to show progression (need ≥3).")
else:
    # X-axis as session index
    x = list(range(1, len(progress_df) + 1))

    fig, ax = plt.subplots(figsize=(7, 4))

    # Transparent backgrounds (Streamlit dark-mode friendly)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    # Plot lines
    ax.plot(x, progress_df["push"], label="Push", marker="o")
    ax.plot(x, progress_df["pull"], label="Pull", marker="o")
    ax.plot(x, progress_df["core"], label="Core", marker="o")


    # Baseline reference line
    ax.axhline(0, linestyle="--", linewidth=1, alpha=0.6)

    # Axis labels & title (light text)
    ax.set_xlabel("Session Index", color="#DDDDDD")
    ax.set_ylabel("Δ Intensity vs Baseline", color="#DDDDDD")
    ax.set_title("Routine-wise Progression (Last 3-Session Window)", color="#FFFFFF")

    # Ticks styling
    ax.tick_params(axis="x", colors="#CCCCCC")
    ax.tick_params(axis="y", colors="#CCCCCC")

    # Grid styling
    ax.grid(True, alpha=0.2)

    # Legend styling
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_color("#DDDDDD")

    st.pyplot(fig)
