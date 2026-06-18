import json
from src.config import EXERCISE_DB_PATH


def load_exercises():
    with open(EXERCISE_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# 🔥 smarter sets/reps
def get_sets_reps(exercise):
    ex = exercise.lower()

    if "squat" in ex or "deadlift" in ex:
        return "3–4 sets × 5–8 reps"
    elif "curl" in ex or "raise" in ex:
        return "2–3 sets × 10–15 reps"
    elif "bike" in ex or "sit" in ex:
        return "2–3 sets × 12–20 reps"
    else:
        return "3 sets × 8–12 reps"


def format_exercise(ex):
    return f"{ex} — {get_sets_reps(ex)}"


def build_weekly_exercise_plan(training_days):

    if training_days >= 5:
        return [
            {
                "day": "Day 1",
                "focus": "Upper Body Strength",
                "details": "Focus on controlled pushing and pulling movements.",
                "exercises": [
                    format_exercise("Barbell Bench Press"),
                    format_exercise("Barbell Shoulder Press"),
                    format_exercise("Band Pull Apart"),
                    format_exercise("Dumbbell Curl"),
                ]
            },
            {
                "day": "Day 2",
                "focus": "Lower Body Strength",
                "details": "Train legs with compound movements.",
                "exercises": [
                    format_exercise("Squats"),
                    format_exercise("Lunges"),
                    format_exercise("Leg Curl"),
                    format_exercise("Calf Raises"),
                ]
            },
            {
                "day": "Day 3",
                "focus": "Cardio & Core",
                "details": "Keep this session light and consistent.",
                "exercises": [
                    format_exercise("Air Bike"),
                    format_exercise("Sit-ups"),
                    format_exercise("Heel Touches"),
                ]
            },
            {
                "day": "Day 4",
                "focus": "Upper Body Strength",
                "details": "Repeat upper body with slight variation.",
                "exercises": [
                    format_exercise("Overhead Press"),
                    format_exercise("Pull-ups"),
                    format_exercise("Rear Delt Raises"),
                    format_exercise("Dumbbell Raises"),
                ]
            },
            {
                "day": "Day 5",
                "focus": "Full Body",
                "details": "Balanced strength and conditioning.",
                "exercises": [
                    format_exercise("Deadlift"),
                    format_exercise("Bench Press"),
                    format_exercise("Lunges"),
                    format_exercise("Air Bike"),
                ]
            }
        ]
    else:
        return [
            {
                "day": "Day 1",
                "focus": "Full Body",
                "details": "Train all major muscle groups.",
                "exercises": [
                    format_exercise("Squats"),
                    format_exercise("Bench Press"),
                    format_exercise("Pull-ups"),
                    format_exercise("Core Work"),
                ]
            }
        ]