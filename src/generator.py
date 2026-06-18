import json
from openai import OpenAI
from src.config import MODEL_NAME, BASE_URL, API_KEY
from src.prompts import PLAN_JSON_TEMPLATE

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)


def generate_response(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def _extract_json_block(raw: str) -> str:
    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    start = raw.find("{")
    end = raw.rfind("}")

    if start != -1 and end != -1 and end > start:
        raw = raw[start:end + 1]

    return raw


def _repair_json_with_model(bad_json: str) -> str:
    repair_prompt = f"""
The following text is intended to be valid JSON but is malformed.

Fix it so that it becomes valid JSON.
Do not change the meaning.
Return ONLY valid JSON.
Do not add markdown fences.

Malformed JSON:
{bad_json}
""".strip()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You fix malformed JSON. Return only valid JSON."
            },
            {
                "role": "user",
                "content": repair_prompt
            },
        ],
        temperature=0.0,
    )

    repaired = response.choices[0].message.content
    return _extract_json_block(repaired)


def _safe_plan_fallback() -> dict:
    fallback = json.loads(json.dumps(PLAN_JSON_TEMPLATE))
    fallback["goal_summary"] = "Your starter plan could not be fully formatted this run, but the app generated a fallback structure so you can keep testing."
    fallback["daily_calorie_guidance"] = "Use the estimated calorie target shown in the app as your starting point."
    fallback["protein_guidance"] = "Aim to spread your protein intake across the day using lean, practical food choices."
    fallback["weekly_workout_plan"] = []
    fallback["simple_meal_structure"] = {
        "breakfast": "Choose a high-protein breakfast such as eggs or Greek yogurt with fruit.",
        "lunch": "Build lunch around a lean protein, vegetables, and a carb source if needed.",
        "dinner": "Build dinner around a protein source, vegetables, and a simple carb.",
        "snacks": "Use practical high-protein snacks like yogurt, milk, fruit, or cottage cheese."
    }
    fallback["tips_for_adherence"] = [
        "Keep meals simple and repeatable.",
        "Prioritize consistency over perfection.",
        "Train with good form and recover well."
    ]
    fallback["safety_disclaimer"] = "This is general fitness and nutrition guidance, not medical advice."
    return fallback


def generate_json_response(system_prompt: str, user_prompt: str) -> dict:
    raw = generate_response(system_prompt, user_prompt)
    raw = _extract_json_block(raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    try:
        repaired = _repair_json_with_model(raw)
        return json.loads(repaired)
    except Exception:
        return _safe_plan_fallback()