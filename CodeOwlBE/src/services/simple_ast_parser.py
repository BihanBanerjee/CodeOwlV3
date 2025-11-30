# This file has been modularized into src/services/ast/
# Import from the new location for backward compatibility

from .ast import SimpleASTParser, LANGUAGE_MAP, LANGUAGE_MODULES

__all__ = ["SimpleASTParser", "LANGUAGE_MAP", "LANGUAGE_MODULES"]
