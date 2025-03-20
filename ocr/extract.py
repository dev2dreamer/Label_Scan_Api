def extract_nutritional_info(ocr_data):
    """
    Processes structured OCR data to return extracted nutritional information.
    """
    nutrition_info = {
        "Protein": ocr_data.get("Protein", "Not Found"),
        "Carbohydrate": ocr_data.get("Carbohydrate", "Not Found"),
        "Total Sugar": ocr_data.get("Total Sugar", "Not Found"),
        "Added Sugar": ocr_data.get("Added Sugar", "Not Found"),
        "Sodium": ocr_data.get("Sodium", "Not Found"),
    }
    return nutrition_info
