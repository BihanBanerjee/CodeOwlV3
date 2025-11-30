from typing import List, Dict, Any


class RustExtractor:
    """Rust-specific AST extraction logic"""

    @staticmethod
    def extract_functions(tree, source_code: str, node_text_func) -> List[Dict[str, Any]]:
        """Extract Rust function items"""
        functions = []

        def walk(node):
            if node.type == "function_item":
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
        """Extract Rust structs, impls, and traits"""
        classes = []

        def walk(node):
            if node.type == "struct_item":
                name_node = node.child_by_field_name("name")
                if name_node:
                    name = node_text_func(name_node, source_code)
                    classes.append({
                        "name": name,
                        "type": "struct",
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                        "source": node_text_func(node, source_code),
                    })

            elif node.type == "impl_item":
                type_node = node.child_by_field_name("type")
                trait_node = node.child_by_field_name("trait")
                if type_node:
                    name = node_text_func(type_node, source_code)
                    impl_type = "impl"
                    if trait_node:
                        trait_name = node_text_func(trait_node, source_code)
                        name = f"{trait_name} for {name}"
                        impl_type = "trait_impl"

                    classes.append({
                        "name": name,
                        "type": impl_type,
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                        "source": node_text_func(node, source_code),
                    })

            elif node.type == "trait_item":
                name_node = node.child_by_field_name("name")
                if name_node:
                    name = node_text_func(name_node, source_code)
                    classes.append({
                        "name": name,
                        "type": "trait",
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
        """Extract Rust use declarations"""
        imports = []

        def walk(node):
            if node.type == "use_declaration":
                arg_node = node.child_by_field_name("argument")
                if arg_node:
                    import_path = node_text_func(arg_node, source_code)
                    imports.append(import_path)

            for child in node.children:
                walk(child)

        walk(tree.root_node)
        return imports
