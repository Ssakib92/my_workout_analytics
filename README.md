# 🏋️ Workout Analytics — Personal Experiment

This repository is a **personal experiment** I built to log and analyze **my own workouts**.

I wasn’t trying to build a fitness app or a polished product.  
I just wanted a better way to understand **what my training actually looks like** once you step back and look at the data.

Over time, the scripts grew a bit, the ideas got clearer, and the project slowly became more structured.

---

## Why I Built This

I train with a simple push / pull / core split and had a few recurring questions:

- Am I actually balanced, or does it just *feel* balanced?
- Is push work slowly dominating without me noticing?
- Which muscle groups am I consistently neglecting?
- Does looking at “last 3 sessions” tell me more than a calendar week?

Instead of guessing, I decided to log everything and see what falls out.

---

## What This Is (and What It Isn’t)

### This *is*
- A personal logging + analysis tool
- Built specifically around my own routines
- Session-based (not calendar-based)
- Simple, explainable, and hackable
- A place to experiment with analytics ideas

### This *is not*
- A commercial fitness app
- A universal training recommendation system
- A biomechanical or medical model
- Something meant to replace a coach or common sense

All numbers here represent **relative training stimulus**, nothing more.

---

## Ideas I’m Playing With

- Mapping exercises to muscle groups in a simple way
- Collapsing many muscles into a few “big picture” groups
- Looking at training in terms of **sessions**, not weeks
- Comparing push vs pull from two angles:
  - muscle fatigue
  - exercise programming
- Tracking routine-level overload (push / pull / core)
- Very lightweight recovery and readiness heuristics

---

## How the Project Is Organized

engine/
├── config.py # constants, exercise models
├── core.py # muscle contribution logic
├── aggregation.py # session-based summaries
├── recovery.py # simple fatigue & readiness ideas
└── analysis.py # interpretation helpers

logger.py # CLI workout logging
main.py # run a logging session
streamlit_app.py # interactive dashboard
visuals.py # plotting helpers