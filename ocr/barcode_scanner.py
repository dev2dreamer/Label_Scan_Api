import cv2
from pyzbar.pyzbar import decode
import requests
import os
from typing import Optional, Dict, Any

class BarcodeScanner:
    def __init__(self):
        """
        Initialize the barcode scanner.
        """
        self.api_base_url = "https://world.openfoodfacts.org/api/v2/product/"

    def scan_barcode_from_image(self, image_path: str) -> Optional[str]:
        """
        Scans an image for barcodes and returns the first barcode detected.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            The barcode value as a string, or None if no barcode is detected
        """
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert to grayscale for better barcode detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Decode barcodes
        barcodes = decode(gray)
        
        # Return the first barcode found
        if barcodes:
            barcode_data = barcodes[0].data.decode('utf-8')
            return barcode_data
        
        return None
    
    def get_product_info(self, barcode: str) -> Dict[str, Any]:
        """
        Fetch product information from Open Food Facts database using the barcode.
        
        Args:
            barcode: The barcode of the product
            
        Returns:
            Dictionary containing product information
        """
        url = f"{self.api_base_url}{barcode}.json"
        
        response = requests.get(url)
        if response.status_code != 200:
            return {"success": False, "error": f"API returned status code {response.status_code}"}
        
        data = response.json()
        
        if data.get('status') != 1:
            return {"success": False, "error": "Product not found in database"}
        
        # Extract relevant nutritional information
        product = data.get('product', {})
        nutriments = product.get('nutriments', {})
        
        nutrition_data = {
            "Protein": f"{nutriments.get('proteins_100g', 'Not Found')}g",
            "Carbohydrate": f"{nutriments.get('carbohydrates_100g', 'Not Found')}g",
            "Total Sugar": f"{nutriments.get('sugars_100g', 'Not Found')}g",
            "Added Sugar": f"{nutriments.get('added_sugars_100g', 'Not Found')}g",
            "Sodium": f"{nutriments.get('sodium_100g', 'Not Found')}g",
            "Product Name": product.get('product_name', 'Unknown'),
            "Brand": product.get('brands', 'Unknown'),
            "Image URL": product.get('image_url')
        }
        
        return {"success": True, "data": nutrition_data}
