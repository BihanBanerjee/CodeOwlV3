from typing import List, Dict, Any


class JavaScriptExtractor:
    """JavaScript/TypeScript-specific AST extraction logic"""

    @staticmethod
    def extract_functions(tree, source_code: str, node_text_func, lang_name: str) -> List[Dict[str, Any]]:
        """Extract JavaScript/TypeScript function declarations"""
        functions = []

        def walk(node):
            if node.type == "function_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    name = node_text_func(name_node, source_code)
                    params_node = node.child_by_field_name("parameters")
                    params = node_text_func(params_node, source_code) if params_node else None

                    functions.append({
                        "name": name,
                        "type": "function",
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                        "parameters": params,
                        "signature": node_text_func(node, source_code),
                        "source": node_text_func(node, source_code),
                    })

            for child in node.children:
                walk(child)

        walk(tree.root_node)
        return functions

    @staticmethod
    def extract_classes(tree, source_code: str, node_text_func) -> List[Dict[str, Any]]:
        """Extract JavaScript/TypeScript class declarations"""
        classes = []

        def walk(node):
            if node.type == "class_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    name = node_text_func(name_node, source_code)
                    classes.append({
                        "name": name,
                        "type": "class",
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                        "source": node_text_func(node, source_code),
                    })

            for child in node.children:
                walk(child)

        walk(tree.root_node)
        return classes

    @staticmethod
    def extract_imports(tree, source_code: str, node_text_func) -> List[str]:
        """Extract JavaScript/TypeScript import statements"""
        imports = []

        def walk(node):
            if node.type == "import_statement":
                for child in node.children:
                    if child.type == "string":
                        text = node_text_func(child, source_code).strip('"').strip("'")
                        imports.append(text)

            for child in node.children:
                walk(child)

        walk(tree.root_node)
        return imports
