def extract_nutritional_info_from_barcode(barcode_data):
    """
    Processes structured barcode data to return extracted nutritional information
    in a format consistent with OCR extraction.
    """
    if not barcode_data.get("success", False):
        return {
            "Protein": "Not Found",
            "Carbohydrate": "Not Found",
            "Total Sugar": "Not Found",
            "Added Sugar": "Not Found",
            "Sodium": "Not Found",
        }
    
    data = barcode_data.get("data", {})
    
    nutrition_info = {
        "Protein": data.get("Protein", "Not Found"),
        "Carbohydrate": data.get("Carbohydrate", "Not Found"),
        "Total Sugar": data.get("Total Sugar", "Not Found"),
        "Added Sugar": data.get("Added Sugar", "Not Found"),
        "Sodium": data.get("Sodium", "Not Found"),
    }
    
    # Add additional product information
    additional_info = {
        "Product Name": data.get("Product Name", "Unknown"),
        "Brand": data.get("Brand", "Unknown"),
        "Image URL": data.get("Image URL")
    }
    
    return nutrition_info, additional_info