import os
import logging
import markdown
import pdfplumber
import pandas as pd
import extract_msg
from docx import Document
from tabulate import tabulate

logger = logging.getLogger('markdown-extractor')

class MarkdownExtractor:
    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = input_folder
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
        logger.info('MarkdownExtractor initialized')

    def extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
        return text

    def extract_text_from_docx(self, file_path: str) -> str:
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
        return text

    def extract_text_from_txt(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
        return text

    def extract_text_from_xlsx(self, file_path: str) -> str:
        text = ""
        try:
            df_sheets = pd.read_excel(file_path, sheet_name=None)  # Load all sheets

            for sheet_name, df in df_sheets.items():
                if df.empty:
                    continue

                text += f"\n### Sheet: {sheet_name}\n\n"
                text += df.to_markdown(index=False) + "\n\n"


        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
        return text

    def extract_text_from_msg(self, file_path: str) -> str:
        text = ""
        try:
            msg = extract_msg.Message(file_path)
            text = f"Subject: {msg.subject}\nFrom: {msg.sender}\nTo: {msg.to}\nDate: {msg.date}\n\n{msg.body}"
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
        return text

    def convert_to_markdown(self, text: str) -> str:
        md_text = markdown.markdown(text)
        return md_text

    def process_documents(self):
        for filename in os.listdir(self.input_folder):
            file_path = os.path.join(self.input_folder, filename)

            if filename.endswith(".pdf"):
                extracted_text = self.extract_text_from_pdf(file_path)
            elif filename.endswith(".docx"):
                extracted_text = self.extract_text_from_docx(file_path)
            elif filename.endswith(".txt"):
                extracted_text = self.extract_text_from_txt(file_path)
            elif filename.endswith(".xlsx"):
                extracted_text = self.extract_text_from_xlsx(file_path)
            elif filename.endswith(".msg"):
                extracted_text = self.extract_text_from_msg(file_path)
            else:
                logger.warning(f"Unsupported file format: {filename}")
                continue

            md_text = self.convert_to_markdown(extracted_text)
            output_path = os.path.join(self.output_folder, filename + ".md")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_text)

            logger.info(f"Processed and saved: {output_path}")

    def get_markdown_content(self):
        markdown_content = ""
        for filename in os.listdir(self.output_folder):
            file_path = os.path.join(self.output_folder, filename)
            print(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_content += f"\n## {filename}\n" + f.read() + "\n"

        return markdown_content
