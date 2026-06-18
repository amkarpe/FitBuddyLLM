import json
from typing import List, Dict
from src.config import USDA_PROCESSED_PATH

PREFERRED_FOOD_KEYWORDS = [
    "chicken", "egg", "yogurt", "milk", "tuna", "salmon",
    "beef", "turkey", "lentils", "beans", "tofu",
    "rice", "oats", "potato", "broccoli", "spinach",
    "banana", "apple", "berries"
]

def load_foods() -> List[Dict]:
    try:
        with open(USDA_PROCESSED_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def select_foods_for_plan(diet_preference: str, top_k: int = 15):
    foods = load_foods()

    filtered = []
    for food in foods:
        desc = food.get("description", "").lower()

        if any(k in desc for k in PREFERRED_FOOD_KEYWORDS):
            filtered.append(food)

    return filtered[:top_k]


# -------- CLEAN FOOD NAMES --------

def simplify_food_name(name: str) -> str:
    name = name.lower()

    mapping = [
        ("egg", "Eggs"),
        ("yogurt", "Greek Yogurt"),
        ("chicken", "Chicken Breast"),
        ("turkey", "Turkey"),
        ("tuna", "Tuna"),
        ("salmon", "Salmon"),
        ("beef", "Lean Beef"),
        ("milk", "Milk"),
        ("oats", "Oats"),
        ("rice", "Rice"),
        ("potato", "Potatoes"),
        ("broccoli", "Broccoli"),
        ("spinach", "Spinach"),
        ("beans", "Beans"),
        ("lentils", "Lentils"),
        ("banana", "Banana"),
        ("apple", "Apple"),
        ("berries", "Berries"),
        ("cheese", "Cheese"),
    ]

    for key, val in mapping:
        if key in name:
            return val

    return None


def clean_food_list(foods):
    cleaned = []
    seen = set()

    for food in foods:
        simple = simplify_food_name(food["description"])

        if not simple:
            continue

        if simple in seen:
            continue

        seen.add(simple)
        cleaned.append(simple)

    return cleaned


# -------- MEAL GROUPING --------

def choose_meal_foods(foods):
    names = [f["description"] for f in foods]

    meals = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snacks": []
    }

    for name in names:
        lower = name.lower()

        if any(x in lower for x in ["egg", "yogurt", "milk", "oats", "banana"]):
            meals["breakfast"].append(name)

        elif any(x in lower for x in ["chicken", "rice", "beans", "lentils", "turkey"]):
            meals["lunch"].append(name)

        elif any(x in lower for x in ["beef", "salmon", "tuna", "potato"]):
            meals["dinner"].append(name)

        else:
            meals["snacks"].append(name)

    return meals