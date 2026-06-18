from src.generator import generate_response
from src.prompts import SYSTEM_PROMPT


# -------- CALCULATIONS --------

def estimate_calories(weight_kg, activity_level):
    multiplier = {
        "sedentary": 28,
        "lightly active": 31,
        "moderately active": 34,
        "very active": 37,
    }.get(activity_level, 31)

    maintenance = weight_kg * multiplier
    target = maintenance - 300

    return f"{int(target-100)}–{int(target+100)} kcal/day"


def estimate_protein(weight_kg):
    return f"{round(weight_kg*1.6)}–{round(weight_kg*2.0)} g/day"


# -------- PLAN SUMMARY --------

def build_plan_summary(height, weight, activity_level, training_days, diet_preference):
    calories = estimate_calories(weight, activity_level)
    protein = estimate_protein(weight)

    summary_prompt = f"""
Create a beginner-friendly fitness plan summary.

User:
- Height: {height} cm
- Weight: {weight} kg
- Activity level: {activity_level}
- Training days per week: {training_days}
- Diet preference: {diet_preference}

Include:
1. Goal Summary
2. Calorie guidance (EXPLAIN reasoning)
3. Protein guidance (EXPLAIN reasoning)

Adapt advice based on diet preference when relevant.

Tone: coach-like, practical
"""

    summary = generate_response(SYSTEM_PROMPT, summary_prompt)

    return {
        "summary": summary,
        "calories": calories,
        "protein": protein
    }


# -------- WORKOUT GENERATION --------

def generate_workout_plan(height, weight, training_days, diet_preference):
    workout_prompt = f"""
Create a beginner-friendly weekly workout plan.

User:
- Height: {height} cm
- Weight: {weight} kg
- Training days per week: {training_days}
- Diet preference: {diet_preference}

Requirements:
- full weekly structure
- exercises + sets/reps
- rest days
- beginner-friendly

Also:
- slightly adapt recommendations based on diet preference
  (e.g. vegetarian → emphasize recovery + protein planning)

Tone:
- coach-like
- practical
"""

    return generate_response(SYSTEM_PROMPT, workout_prompt)


def generate_diet_plan(clean_foods, diet_preference, calories, protein):

    prompt = f"""
Create a simple daily diet plan.

User:
- Diet preference: {diet_preference}
- Target calories: {calories}
- Target protein: {protein}

Available foods:
{clean_foods}

Requirements:
- 1 breakfast
- 1 lunch
- 1 dinner
- 1 snack
- high protein
- realistic and easy to follow

Keep it:
- simple
- practical
- not too long
- beginner friendly

Tone:
- coach-like
"""

    return generate_response(SYSTEM_PROMPT, prompt)