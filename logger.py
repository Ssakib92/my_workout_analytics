# logger.py
import os
import pandas as pd
from datetime import datetime

CSV_PATH = "workout_log.csv"

# ==============================
# ROUTINE DEFINITIONS (ORDERED)
# ==============================

ROUTINES = {
    "push": [
        "Push-up",
        "DB Bench Press",
        "DB Shoulder Press",
        "Lateral Raise",
        "DB Triceps Extension",
        "Diamond Push-up",     
        "Decline Push-up"
    ],

    "pull": [
        "Dead Hang",
        "Scapular Pull-up",
        "Negative Pull-up",
        "One-arm DB Row",
        "Bent-over DB Row",
        "DB Shrug",
        "Rear Delt Fly",
        "DB Curl",
        "Hammer Curl",
        "Superman"
    ],

    "core": [
        "Goblet Squat",
        "Lunge",
        "High Knees",
        "Hanging Knee Raise",
        "Plank",
        "Active Hang",
        "Leg Raise",
        "Russian Twist",
        "DB Side Bends",
        "Glute Bridge", 
        "Mountain Climber",
        "Burpee"
    ]
}


def log_workout_session():
    print("\n=== WORKOUT LOGGER (GUIDED) ===")

    date_input = input("Date (YYYY-MM-DD) [blank = today]: ")
    date = datetime.today().date() if not date_input else pd.to_datetime(date_input).date()

    routine = input("Routine (push / pull / core): ").strip().lower()

    if routine not in ROUTINES:
        raise ValueError("Invalid routine")

    print(f"\nLogging routine: {routine.upper()}")
    print("Enter sets/reps for each exercise.")
    print("Press ENTER to skip an exercise.\n")

    logs = []

    for exercise in ROUTINES[routine]:

        print(f"→ {exercise}")

        sets_input = input("  Sets (blank = skip): ").strip()
        if sets_input == "":
            print("  ⏭ Skipped\n")
            continue

        reps_input = input("  Reps: ").strip()

        try:
            sets = int(sets_input)
            reps = int(reps_input)
        except ValueError:
            print("  ❌ Invalid input, skipping\n")
            continue

        logs.append({
            "date": date,
            "routine": routine,
            "exercise": exercise,
            "sets": sets,
            "reps": reps
        })

        print("  ✔ Logged\n")

    df = pd.DataFrame(logs)

    print("\n=== SESSION COMPLETE ===")
    print(df)

    return df



def save_session(df, path=CSV_PATH):
    df.to_csv(path, mode="a", header=not os.path.exists(path), index=False)


def load_history(path=CSV_PATH):
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path, parse_dates=["date"])
