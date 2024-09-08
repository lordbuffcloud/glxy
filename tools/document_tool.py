import os

class DocumentTool:
    def __init__(self, save_path="./docs"):
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    def save_document(self, file):
        with open(os.path.join(self.save_path, file.filename), 'wb') as f:
            f.write(file.file.read())
        return f"Document {file.filename} saved successfully."

    def process_document_for_rag(self, document_path):
        # Placeholder for real RAG processing logic
        return f"Document at {document_path} processed for RAG."
