# ==============================
# EXERCISE → MUSCLE MODEL
# ==============================

EXERCISE_LIBRARY = {
    "Push-up": {"muscles": {"Chest": 0.5, "Triceps": 0.3, "Shoulders": 0.2}},
    "DB Bench Press": {"muscles": {"Chest": 0.55, "Triceps": 0.25, "Shoulders": 0.2}},
    "DB Chest Fly": {"muscles": {"Chest": 0.7, "Shoulders": 0.15, "Biceps": 0.15}},
    "DB Shoulder Press": {"muscles": {"Shoulders": 0.6, "Triceps": 0.25, "Upper Chest": 0.15}},
    "Lateral Raise": {"muscles": {"Side Delts": 0.75, "Upper Traps": 0.15, "Core": 0.1}},
    "DB Triceps Extension": {"muscles": {"Triceps": 0.8, "Shoulders": 0.2}},
    "Incline DB Press": { "muscles": { "Upper Chest": 0.55, "Shoulders": 0.20, "Triceps": 0.20, "Core": 0.05 } },
    "Diamond Push-up": {"muscles": {"Triceps": 0.5,"Chest": 0.3,"Shoulders": 0.2}},
    "Decline Push-up": {"muscles": {"Upper Chest": 0.45, "Shoulders": 0.3, "Triceps": 0.25}},

    "Dead Hang": {"muscles": {"Forearms": 0.45, "Upper Back": 0.2, "Shoulders": 0.25, "Core": 0.1}},
    "Scapular Pull-up": {"muscles": {"Upper Back": 0.6, "Lats": 0.15, "Shoulders": 0.25}},
    "Negative Pull-up": {"muscles": {"Lats": 0.5, "Upper Back": 0.25, "Biceps": 0.15, "Core": 0.1}},
    "One-arm DB Row": {"muscles": {"Lats": 0.5, "Upper Back": 0.2, "Biceps": 0.2, "Forearms": 0.1}},
    "Bent-over DB Row": {"muscles": {"Upper Back": 0.4, "Lats": 0.3, "Biceps": 0.2, "Lower Back": 0.1}},
    "Rear Delt Fly": {"muscles": {"Rear Delts": 0.6, "Upper Back": 0.3, "Traps": 0.1}},
    "DB Curl": {"muscles": {"Biceps": 0.75, "Forearms": 0.25}},
    "Hammer Curl": {"muscles": {"Biceps": 0.6, "Forearms": 0.4}},
    "Pull-up": { "muscles": { "Lats": 0.55, "Biceps": 0.25, "Rear Delts": 0.15, "Core": 0.05 } }, 
    "DB Shrug": {"muscles": {"Upper Traps": 0.7, "Shoulders": 0.2, "Forearms": 0.1}},
    "Superman": {"muscles": {"Lower Back": 0.6, "Glutes": 0.25, "Core": 0.15}}, 

    "Goblet Squat": {"muscles": {"Quads": 0.45, "Glutes": 0.3, "Hamstrings": 0.15, "Core": 0.1}},
    "Lunge": {"muscles": {"Glutes": 0.4, "Quads": 0.35, "Hamstrings": 0.15, "Core": 0.1}},
    "Plank": {"muscles": {"Core": 0.75, "Shoulders": 0.2, "Glutes": 0.05}},
    "Leg Raise": {"muscles": {"Lower Abs": 0.6, "Hip Flexors": 0.25, "Core": 0.15}},
    "Russian Twist": {"muscles": {"Obliques": 0.6, "Core": 0.4}},
    "Glute Bridge": {"muscles": {"Glutes": 0.6, "Hamstrings": 0.25, "Lower Back": 0.15}},
    "High Knees": {"muscles": {"Hip Flexors": 0.4, "Quads": 0.25,"Core": 0.25,"Calves": 0.1}},
    "Crunch": {"muscles": {"Abs": 0.75, "Core": 0.25}},
    "DB Side Bends": {"muscles": {"Obliques": 0.7, "Core": 0.3}},
    "Mountain Climber": {"muscles": {"Core": 0.4, "Hip Flexors": 0.25, "Shoulders": 0.2, "Quads": 0.15}},
    "Flutter Kicks": {"muscles": {"Lower Abs": 0.6, "Hip Flexors": 0.25, "Core": 0.15}},
    "Burpee": {"muscles": {"Quads": 0.25, "Glutes": 0.2, "Chest": 0.15, "Shoulders": 0.15, "Core": 0.15, "Calves": 0.1}},
    "Active Hang": {"muscles": {"Forearms": 0.3,"Upper Back": 0.25,"Shoulders": 0.25,"Core": 0.2}},
    "Hanging Knee Raise": {"muscles": {"Lower Abs": 0.45,"Hip Flexors": 0.2,"Core": 0.2,"Lats": 0.1,"Forearms": 0.05}}
}


# ==============================
# RELATIVE LOAD MODEL
# ==============================

DEFAULT_LOAD = {
    "Push-up": 1.0,
    "DB Bench Press": 1.7,
    "DB Chest Fly": 0.9,
    "DB Shoulder Press": 1.7,
    "Lateral Raise": 1.0,
    "DB Triceps Extension": 1.0,
    "Diamond Push-up": 1.1,     
    "Decline Push-up": 1.1, 
    "Incline DB Press": 1.7,  

    "Pull-up": 1.8,  
    "Dead Hang": 0.6,
    "Scapular Pull-up": 1.0,
    "Negative Pull-up": 1.5,
    "One-arm DB Row": 1.7,
    "Bent-over DB Row": 1.1,
    "Rear Delt Fly": 1.0,
    "DB Curl": 0.9,
    "Hammer Curl": 0.9,
    "DB Shrug": 0.9,
    "Superman": 0.6, 

    "Goblet Squat": 1.7,
    "Lunge": 1.0,
    "Plank": 1.2,
    "Leg Raise": 1.0,
    "Active Hang": 0.8,
    "Hanging Knee Raise": 1.2,
    "Russian Twist": 0.5,
    "Glute Bridge": 0.3,
    "High Knees": 0.4,
    "Crunch": 0.8,
    "DB Side Bends": 0.6,
    "Mountain Climber": 0.5,
    "Flutter Kicks": 0.5,
    "Burpee": 1.1
}


# ==============================
# MUSCLE COLLAPSE (Tier-1)
# ==============================

MUSCLE_COLLAPSE_MAP = {
    "Chest": "Chest", "Upper Chest": "Chest",
    "Lats": "Back", "Upper Back": "Back", "Lower Back": "Back",
    "Traps": "Back", "Upper Traps": "Back",

    "Front Delts": "Shoulders", "Side Delts": "Shoulders",
    "Rear Delts": "Shoulders", "Shoulders": "Shoulders",

    "Biceps": "Arms", "Triceps": "Arms", "Forearms": "Arms",

    "Quads": "Legs", "Hamstrings": "Legs",
    "Calves": "Legs", "Glutes": "Legs",

    "Abs": "Core", "Core": "Core",
    "Lower Abs": "Core", "Obliques": "Core",
    "Hip Flexors": "Core",
}


# ==============================
# EXERCISE INTENT
# ==============================

EXERCISE_INTENT = {
    # PUSH
    "Push-up": "push",
    "DB Bench Press": "push",
    "DB Chest Fly": "push",
    "DB Shoulder Press": "push",
    "Lateral Raise": "push",
    "DB Triceps Extension": "push",
    "Diamond Push-up": "push",
    "Decline Push-up": "push",
    "Incline DB Press": "push",

    # PULL
    "Dead Hang": "pull",
    "Scapular Pull-up": "pull",
    "Negative Pull-up": "pull",
    "One-arm DB Row": "pull",
    "Bent-over DB Row": "pull",
    "Rear Delt Fly": "pull",
    "DB Curl": "pull",
    "Hammer Curl": "pull",
    "DB Shrug": "pull",
    "Pull-up": "pull",

    # NEUTRAL / CORE
    "Goblet Squat": "neutral",
    "Lunge": "neutral",
    "Plank": "neutral",
    "Leg Raise": "neutral",
    "Russian Twist": "neutral",
    "Glute Bridge": "neutral",
    "Superman": "neutral",
    "High Knees": "neutral",
    "Crunch": "neutral",
    "DB Side Bends": "neutral",
    "Mountain Climber": "neutral",
    "Flutter Kicks": "neutral",
    "Burpee": "neutral"
}


# ==============================
# RECOVERY CONSTANTS
# ==============================

AVG_SLEEP_HOURS = 6.5

RECOVERY_TAU = {
    "Chest": 5,
    "Back": 5,
    "Shoulders": 6,
    "Arms": 4,
    "Legs": 7,
    "Core": 3
}


# ==============================
# SESSION WINDOWS
# ==============================

SESSION_WINDOWS = {
    "weekly": 3,
    "monthly": 12
}
