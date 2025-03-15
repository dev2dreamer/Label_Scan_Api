import streamlit as st
import os
from ocr.document_ai import DocumentOCR
from ocr.preprocess import preprocess_image
from ocr.extract import extract_nutritional_info

PROJECT_ID = "your-google-cloud-project-id"
PROCESSOR_ID = "your-document-ai-processor-id"

st.title("🥗 Food Label OCR Scanner")

uploaded_file = st.file_uploader("Upload a food label image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image_path = "uploaded_image.png"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Preprocess image
    processed_image_path = preprocess_image(image_path)

    # Perform OCR
    ocr = DocumentOCR(PROJECT_ID, PROCESSOR_ID)
    extracted_text = ocr.process_document(processed_image_path)

    # Extract nutritional information
    nutrition_info = extract_nutritional_info(extracted_text)

    # Display extracted information
    st.subheader("Extracted Nutritional Information")
    for key, value in nutrition_info.items():
        st.write(f"**{key}:** {value if value else 'Not Found'}")
