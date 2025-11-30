# This file has been modularized into src/services/ast/graph_builder.py
# Import from the new location for backward compatibility

from .ast.graph_builder import build_simple_graph, analyze_cross_file_imports

__all__ = ["build_simple_graph", "analyze_cross_file_imports"]
