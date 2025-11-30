from typing import List, Dict, Any


class GoExtractor:
    """Go-specific AST extraction logic"""

    @staticmethod
    def extract_functions(tree, source_code: str, node_text_func) -> List[Dict[str, Any]]:
        """Extract Go function and method declarations"""
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

            elif node.type == "method_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    name = node_text_func(name_node, source_code)
                    params_node = node.child_by_field_name("parameters")
                    receiver_node = node.child_by_field_name("receiver")
                    params = node_text_func(params_node, source_code) if params_node else None
                    receiver = node_text_func(receiver_node, source_code) if receiver_node else None

                    functions.append({
                        "name": name,
                        "type": "method",
                        "receiver": receiver,
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
        """Extract Go type specifications (structs and interfaces)"""
        classes = []

        def walk(node):
            if node.type == "type_spec":
                name_node = node.child_by_field_name("name")
                type_node = node.child_by_field_name("type")
                if name_node and type_node:
                    name = node_text_func(name_node, source_code)
                    type_kind = type_node.type

                    if type_kind == "struct_type":
                        classes.append({
                            "name": name,
                            "type": "struct",
                            "start_line": node.start_point[0] + 1,
                            "end_line": node.end_point[0] + 1,
                            "source": node_text_func(node, source_code),
                        })
                    elif type_kind == "interface_type":
                        classes.append({
                            "name": name,
                            "type": "interface",
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
        """Extract Go import specifications"""
        imports = []

        def walk(node):
            if node.type == "import_spec":
                for child in node.children:
                    if child.type == "interpreted_string_literal":
                        text = node_text_func(child, source_code).strip('"')
                        imports.append(text)

            for child in node.children:
                walk(child)

        walk(tree.root_node)
        return imports
