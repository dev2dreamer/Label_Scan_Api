import streamlit as st
import os
from ocr.document_ai import DocumentOCR
from ocr.preprocess import preprocess_image
from ocr.extract import extract_nutritional_info
from ocr.barcode_scanner import BarcodeScanner
from ocr.barcode_extract import extract_nutritional_info_from_barcode

PROJECT_ID = os.getenv("PROJECT_ID")
PROCESSOR_ID = os.getenv("PROCESSOR_ID")

st.title("🥗 Food Label OCR & Barcode Scanner")

# Add a tab interface to switch between OCR and barcode scanning
tab_selection = st.radio("Select Input Method:", ["OCR Label Scanner", "Barcode Scanner"])

if tab_selection == "OCR Label Scanner":
    st.header("OCR Label Scanner")
    uploaded_file = st.file_uploader("Upload a food label image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image_path = "uploaded_image.png"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(image_path, caption="Uploaded Image", use_column_width=True)

        # Process button
        if st.button("Extract Nutrition Information"):
            with st.spinner("Processing image..."):
                # Preprocess image
                processed_image_path = preprocess_image(image_path)

                # Perform OCR
                ocr = DocumentOCR(PROJECT_ID, PROCESSOR_ID)
                extracted_data = ocr.process_document(processed_image_path)

                # Extract nutritional information
                nutrition_info = extract_nutritional_info(extracted_data)

                # Display extracted information
                st.subheader("Extracted Nutritional Information")
                for key, value in nutrition_info.items():
                    st.write(f"**{key}:** {value if value else 'Not Found'}")

else:  # Barcode Scanner
    st.header("Barcode Scanner")
    st.write("Upload an image containing a barcode or enter a barcode manually to fetch nutrition information")
    
    barcode_method = st.radio("Select barcode input method:", ["Upload Image", "Enter Manually"])
    
    barcode_value = None
    barcode_scanner = BarcodeScanner()
    
    if barcode_method == "Upload Image":
        barcode_file = st.file_uploader("Upload barcode image", type=["png", "jpg", "jpeg"])
        
        if barcode_file:
            # Save the uploaded file
            barcode_image_path = "barcode_image.png"
            with open(barcode_image_path, "wb") as f:
                f.write(barcode_file.getbuffer())
            
            st.image(barcode_image_path, caption="Uploaded Barcode Image", width=300)
            
            # Process button for barcode scanning
            if st.button("Scan Barcode"):
                with st.spinner("Scanning barcode..."):
                    try:
                        barcode_value = barcode_scanner.scan_barcode_from_image(barcode_image_path)
                        if barcode_value:
                            st.success(f"Barcode detected: {barcode_value}")
                        else:
                            st.error("No barcode detected in the image")
                    except Exception as e:
                        st.error(f"Error scanning barcode: {str(e)}")
    else:  # Manual entry
        barcode_value = st.text_input("Enter barcode number")
    
    # Fetch product information if we have a barcode
    if barcode_value and st.button("Fetch Product Information"):
        with st.spinner("Fetching product information..."):
            product_info = barcode_scanner.get_product_info(barcode_value)
            
            if product_info["success"]:
                nutrition_info, additional_info = extract_nutritional_info_from_barcode(product_info)
                
                # Display product details
                st.subheader(additional_info.get("Product Name", "Product Information"))
                st.write(f"**Brand:** {additional_info.get('Brand', 'Unknown')}")
                
                # Display product image if available
                if additional_info.get("Image URL"):
                    st.image(additional_info["Image URL"], caption="Product Image", width=300)
                
                # Display nutritional information
                st.subheader("Nutritional Information")
                for key, value in nutrition_info.items():
                    st.write(f"**{key}:** {value}")
            else:
                st.error(f"Error: {product_info.get('error', 'Failed to fetch product information')}")