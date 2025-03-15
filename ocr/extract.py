import re

def extract_nutritional_info(text):
    nutrition_data = {
        "Calories": None,
        "Added Sugar": None,
        "Natural Sugar": None,
        "Carbohydrates": None
    }

    patterns = {
        "Calories": r"(\d+)\s*calories",
        "Added Sugar": r"(\d+)\s*g\s*added sugar",
        "Natural Sugar": r"(\d+)\s*g\s*natural sugar",
        "Carbohydrates": r"(\d+)\s*g\s*carbohydrates"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            nutrition_data[key] = match.group(1)

    return nutrition_data
