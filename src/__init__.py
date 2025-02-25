import logging
from src.operations.ask import LLMAsker
from src.operations.search import SearchEngine
from src.operations.embed import EmbedService
from src.operations.extract import MarkdownExtractor
import argparse

class App:
  """ The main class of the application. """

  def __init__(self):
    pass

  def run(self):
    parser = argparse.ArgumentParser(description='Ask questions about the files of a case.')

    # Add optional "mode" argument (with values "load-files" and "ask-question" (default))
    parser.add_argument('--mode', choices=['index-files', 'ask-question', 'search', 'get-markdown'], default='ask-question', help='The mode of the application.')

    # Add question argument as required positional argument if mode is "ask-question"
    parser.add_argument('question', nargs='?', type=str, help='The question to ask about the files of a case.')

    args = parser.parse_args()

    if args.mode == 'index-files':
      self.load_files()
    elif args.mode == 'ask-question':
      question = args.question
      if not question or question.isspace():
        parser.error('The question argument is required in "ask-question" mode.')
      self.ask_question(question)
    elif args.mode == 'search':
      question = args.question
      if not question or question.isspace():
        parser.error('The query argument is required in "search" mode.')
      self.search(question)
    elif args.mode == 'get-markdown':
      self.get_markdown()

  def load_files(self):
    logging.info("Extracting and embedding files...")

    embedder = EmbedService("data/output", "data/embeddings.json")
    embedder.embed_documents()

    logging.info("Indexing completed.")

  def search(self, query):
    logging.info(f"Searching for query: {query}")

    search_engine = SearchEngine("data/embeddings.json")
    results = search_engine.search(query)

    print("Top matching documents:")
    for doc, score in results:
        print(f"{doc}: {score:.4f}")

  def get_markdown(self):
    logging.info(f"Generating Markdown files...")

    extractor = MarkdownExtractor("documents/", "data/output")
    extractor.process_documents()
    markdown_content = extractor.get_markdown_content()

  def ask_question(self, question):
    logging.info(f'Asking question: {question}')

    operator = LLMAsker("data/embeddings.json")
    response = operator.ask(question)

    print(response)
