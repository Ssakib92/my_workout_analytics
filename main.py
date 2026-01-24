# main.py
"""
Main entry point for the Workout Analytics system.

Flow:
1. Log a workout session
2. Save it to CSV
3. Compute fine-grained muscle contribution
4. Collapse to Tier-1 muscle groups
5. Visualize muscle balance
6. (Optional) Inspect sub-muscle coverage
"""

# --------- IMPORTS ----------
from logger import (
    log_workout_session,
    save_session
)

from engine.core import (
    compute_muscle_contribution,
    collapse_to_tier1,
    muscle_coverage_report
)

from visuals import radar_plot


# ==============================
# MAIN EXECUTION
# ==============================

def main():

    # ---- 1. LOG WORKOUT SESSION ----
    session_df = log_workout_session()

    if session_df.empty:
        print("⚠ No exercises logged. Exiting.")
        return

    # ---- 2. SAVE SESSION ----
    save_session(session_df)
    print("\n💾 Session saved successfully.")

    # ---- 3. COMPUTE MUSCLE CONTRIBUTION (FINE) ----
    fine_scores = compute_muscle_contribution(session_df)

    # ---- 4. COLLAPSE TO TIER-1 MUSCLE GROUPS ----
    tier1_df = collapse_to_tier1(fine_scores)

    print("\n=== TIER-1 MUSCLE CONTRIBUTION ===")
    print(tier1_df)

    # ---- 5. VISUALIZE MUSCLE BALANCE ----
    radar_plot(tier1_df, title="Session Muscle Balance")

    # ---- 6. OPTIONAL: SUB-MUSCLE COVERAGE CHECK ----
    VALID_GROUPS = [
        "Chest",
        "Back",
        "Shoulders",
        "Arms",
        "Legs",
        "Core"
    ]

    while True:
        inspect = input(
            f"\nInspect sub-muscle coverage? "
            f"({', '.join(VALID_GROUPS)} / no): "
        ).strip()

        if inspect.lower() == "no":
            break

        if inspect not in VALID_GROUPS:
            print("⚠ Invalid muscle group.")
            continue

        coverage_df = muscle_coverage_report(fine_scores, inspect)

        if coverage_df.empty:
            print(f"⚠ No data for muscle group: {inspect}")
        else:
            print(f"\n=== SUB-MUSCLE COVERAGE: {inspect.upper()} ===")
            print(coverage_df)


# ==============================
# SCRIPT ENTRY POINT
# ==============================

if __name__ == "__main__":
    main()
