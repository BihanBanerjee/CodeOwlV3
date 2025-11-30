from typing import Any, Dict, List, Tuple

import tree_sitter_go as tsgo
import tree_sitter_javascript as tsjs
import tree_sitter_python as tspython
import tree_sitter_rust as tsrust
import tree_sitter_typescript as tsts

from .base_parser import BaseParser
from .extractors import PythonExtractor, JavaScriptExtractor, GoExtractor, RustExtractor


# Language modules mapping
LANGUAGE_MODULES = {
    "python": tspython,
    "javascript": tsjs,
    "typescript": tsts,
    "go": tsgo,
    "rust": tsrust,
}

# File extension to language mapping
LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".go": "go",
    ".rs": "rust",
}

# Extractor mapping
EXTRACTORS = {
    "python": PythonExtractor,
    "javascript": JavaScriptExtractor,
    "typescript": JavaScriptExtractor,  # JS and TS use same extractor
    "go": GoExtractor,
    "rust": RustExtractor,
}


class SimpleASTParser(BaseParser):
    """
    Simplified AST parser focused on core functionality only.
    Removes all the complex analysis from the original.
    """

    def __init__(self, language: str = "python"):
        if language not in LANGUAGE_MODULES:
            raise ValueError(f"Unsupported language: {language}")

        lang_module = LANGUAGE_MODULES[language]
        super().__init__(lang_module, language)
        self.extractor = EXTRACTORS[language]

    def extract_functions(self, tree, source_code: str) -> List[Dict[str, Any]]:
        """Extract function definitions using language-specific extractor"""
        if self.lang_name in ("javascript", "typescript"):
            return self.extractor.extract_functions(
                tree, source_code, self.node_text, self.lang_name
            )
        return self.extractor.extract_functions(tree, source_code, self.node_text)

    def extract_classes(self, tree, source_code: str) -> List[Dict[str, Any]]:
        """Extract class definitions using language-specific extractor"""
        return self.extractor.extract_classes(tree, source_code, self.node_text)

    def extract_imports(self, tree, source_code: str) -> List[str]:
        """Extract import statements using language-specific extractor"""
        return self.extractor.extract_imports(tree, source_code, self.node_text)

    def extract_semantic_analysis(
        self, tree, source_code: str, file_path: str
    ) -> Dict[str, Any]:
        """Extract complete semantic analysis for a file"""
        return {
            "file_path": file_path,
            "language": self.lang_name,
            "functions": self.extract_functions(tree, source_code),
            "classes": self.extract_classes(tree, source_code),
            "imports": self.extract_imports(tree, source_code),
            "analysis_method": "simplified_ast",
        }
