import os
from google.cloud import documentai_v1beta3 as documentai
from google.oauth2 import service_account

class DocumentOCR:
    def __init__(self, project_id, processor_id):
        credentials = service_account.Credentials.from_service_account_file("credentials.json")
        self.client = documentai.DocumentProcessorServiceClient(credentials=credentials)
        self.project_id = project_id
        self.processor_id = processor_id

    def process_document(self, image_path):
        """Processes the document using Google Document AI and extracts structured data."""
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()

        # Create a raw document request
        raw_document = documentai.RawDocument(content=image_content, mime_type="image/png")

        # Define the processor resource
        name = f"projects/{self.project_id}/locations/us/processors/{self.processor_id}"

        # Call the API
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)
        result = self.client.process_document(request=request)

        # Extract structured fields
        return self._extract_fields(result.document)

    def _extract_fields(self, document):
        """Extracts custom fields from the Document AI processor output."""
        nutrition_data = {
            "Protein": None,
            "Carbohydrate": None,
            "Total Sugar": None,
            "Added Sugar": None,
            "Sodium": None
        }

        # Iterate over document fields
        for entity in document.entities:
            field_name = entity.type_
            if field_name in nutrition_data:
                nutrition_data[field_name] = entity.mention_text

        return nutrition_data
