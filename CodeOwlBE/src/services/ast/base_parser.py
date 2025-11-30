from typing import Any, Tuple
from tree_sitter import Language, Parser


class BaseParser:
    """Base class for AST parsing with common utilities"""

    def __init__(self, language_module, language_name: str):
        self.language = Language(language_module.language())
        self.parser = Parser(self.language)
        self.lang_name = language_name

    def parse_file(self, file_path: str) -> Tuple[Any, str]:
        """Parse a file and return (tree, source_code)"""
        with open(file_path, "rb") as f:
            source_code = f.read()

        tree = self.parser.parse(source_code)

        if isinstance(source_code, bytes):
            source_code = source_code.decode("utf-8")

        return tree, source_code

    @staticmethod
    def node_text(node, source_code: str) -> str:
        """Extract text from a node"""
        try:
            return source_code[node.start_byte:node.end_byte]
        except Exception:
            return ""