import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Preprocess the image by converting it to grayscale and applying thresholding.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (800, 800))
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    processed_image_path = "processed_image.png"
    cv2.imwrite(processed_image_path, binary_image)
    
    return processed_image_path
