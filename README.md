# 🏋️ Workout Analytics Tracker

A **session-based workout logging and analytics system** designed to analyze
training balance, muscle load, recovery, and routine-level overload.

This is **not** a generic fitness app.
It focuses on **relative training stimulus**, explainability, and long-term trend reliability.

---

## 🔍 Key Features

- Guided workout logging (push / pull / core routines)
- Fine-grained exercise → muscle modeling
- Tier-1 muscle aggregation (Chest, Back, Shoulders, Arms, Legs, Core)
- Session-based aggregation:
  - Last 3 sessions ≈ weekly
  - Last 12 sessions ≈ monthly
- Muscle balance & overload detection
- Push / Pull ratios:
  - Muscle-wise (fatigue balance)
  - Exercise-wise (programming balance)
- Unified muscle readiness score
- Sub-muscle coverage analysis
- Streamlit dashboard for visualization

---

## 🧠 Design Philosophy

- **Session-based aggregation** instead of calendar time
- No fake precision (no RIR, tempo, wearables)
- Clear separation of concerns:
  - `logger.py` → data collection
  - `engine/` → analytics logic
  - `streamlit_app.py` → visualization only
- Relative load modeling, not absolute biomechanics

---

## 📁 Project Structure

