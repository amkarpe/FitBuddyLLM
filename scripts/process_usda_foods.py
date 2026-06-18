import json
from pathlib import Path
from src.config import USDA_RAW_PATH, USDA_PROCESSED_PATH


TARGET_NUTRIENTS = {
    "Energy": "calories_kcal",
    "Protein": "protein_g",
    "Carbohydrate, by difference": "carbs_g",
    "Total lipid (fat)": "fat_g",
    "Fiber, total dietary": "fiber_g",
}


def extract_nutrients(food_nutrients):
    values = {
        "calories_kcal": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 0.0,
        "fiber_g": 0.0,
    }

    for nutrient_entry in food_nutrients:
        nutrient = nutrient_entry.get("nutrient", {})
        name = nutrient.get("name", "")
        amount = nutrient_entry.get("amount", None)

        if name in TARGET_NUTRIENTS and amount is not None:
            values[TARGET_NUTRIENTS[name]] = float(amount)

    return values


def extract_serving_grams(food):
    portions = food.get("foodPortions", [])
    if portions:
        first = portions[0]
        gram_weight = first.get("gramWeight")
        if gram_weight:
            return float(gram_weight)
    return 100.0


def clean_food(food):
    description = food.get("description", "").strip()
    category = food.get("foodCategory", {}).get("description", "Unknown")
    fdc_id = food.get("fdcId")

    nutrients = extract_nutrients(food.get("foodNutrients", []))
    serving_grams = extract_serving_grams(food)

    if not description:
        return None

    return {
        "fdcId": fdc_id,
        "description": description,
        "category": category,
        "serving_grams": serving_grams,
        **nutrients,
    }


def is_useful_food(food):
    desc = food["description"].lower()

    blocked_terms = [
        "baby food",
        "formula",
        "alcohol",
        "beverage, carbonated",
        "sweetener",
    ]

    if any(term in desc for term in blocked_terms):
        return False

    if food["calories_kcal"] <= 0:
        return False

    return True


def main():
    input_path = Path(USDA_RAW_PATH)
    output_path = Path(USDA_PROCESSED_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    foundation_foods = raw.get("FoundationFoods", [])
    cleaned = []

    for food in foundation_foods:
        item = clean_food(food)
        if item and is_useful_food(item):
            cleaned.append(item)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"Saved cleaned USDA foods to: {output_path}")
    print(f"Total foods: {len(cleaned)}")


if __name__ == "__main__":
    main()