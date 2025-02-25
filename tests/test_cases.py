import unittest
from unittest.mock import patch, MagicMock
from src.operations.ask import LLMAsker
from src.operations.search import SearchEngine
from src.operations.embed import EmbedService
from src.operations.extract import MarkdownExtractor
from src.__init__ import App

class TestApplication(unittest.TestCase):

    @patch('src.__init__.EmbedService.embed_documents')
    def test_index_files(self, mock_embed):
        mock_embed.return_value = None

        app = App()
        app.load_files()

        mock_embed.assert_called_once()


    @patch('src.operations.search.SearchEngine.search', return_value=[("doc1.md", 0.9), ("doc2.md", 0.8)])
    def test_search(self, mock_search):
        app = App()
        with patch('builtins.print') as mock_print:
            app.search("test query")
            mock_search.assert_called_once_with("test query")
            mock_print.assert_any_call("Top matching documents:")

    @patch('src.operations.ask.LLMAsker.ask', return_value="Sample AI response with sources")
    def test_ask_question(self, mock_ask):
        app = App()
        with patch('builtins.print') as mock_print:
            app.ask_question("What is the contract term?")
            mock_ask.assert_called_once_with("What is the contract term?")
            mock_print.assert_called_once_with("Sample AI response with sources")

    @patch('src.operations.extract.MarkdownExtractor.get_markdown_content', return_value="# Sample Markdown Content")
    def test_get_markdown(self, mock_markdown):
        app = App()
        with patch('builtins.print') as mock_print:
            app.get_markdown()
            mock_markdown.assert_called_once()

if __name__ == '__main__':
    unittest.main()
