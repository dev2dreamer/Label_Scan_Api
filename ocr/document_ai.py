import os
from google.cloud import documentai_v1beta3 as documentai
from google.oauth2 import service_account

class DocumentOCR:
    def __init__(self, project_id, processor_id):
        credentials = service_account.Credentials.from_service_account_file("credentials.json")
        self.client = documentai.DocumentUnderstandingServiceClient(credentials=credentials)
        self.project_id = project_id
        self.processor_id = processor_id

    def process_document(self, image_path):
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()

        request = {
            "name": f"projects/{self.project_id}/locations/us/processors/{self.processor_id}",
            "raw_document": {"content": image_content, "mime_type": "image/png"},
        }

        result = self.client.process_document(request=request)
        document_text = result.document.text
        return document_text
