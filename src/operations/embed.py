import os
import json
from typing import List
from src.api import embed_texts
import logging

logger = logging.getLogger('embed')

class EmbedService:
    def __init__(self, input_folder: str, output_file: str):
        self.input_folder = input_folder
        self.output_file = output_file

    def load_markdown_files(self):
        documents = {}
        for filename in os.listdir(self.input_folder):
            file_path = os.path.join(self.input_folder, filename)
            if filename.endswith(".md"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                    if text:
                        documents[filename] = text
                    else:
                        logger.warning(f"Skipping empty document: {filename}")
        return documents

    def embed(self, text: str) -> List[float]:
        response = embed_texts([text], 'document')
        if "embeddings" in response and isinstance(response["embeddings"], list) and response["embeddings"]:
            return response["embeddings"][0]
        else:
            logger.error("Invalid response from embedding API")
            return []

    def embed_documents(self):
        documents = self.load_markdown_files()
        embeddings = {}

        for filename, text in documents.items():
            try:
                embedding = self.embed(text)
                if embedding:
                    embeddings[filename] = embedding
                else:
                    logger.error(f"Failed to generate embedding for {filename}")
            except Exception as e:
                logger.error(f"Error embedding {filename}: {e}")

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(embeddings, f)

        logger.info(f"Embeddings saved to {self.output_file}")
