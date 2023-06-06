import ast
from src.dataclasses.model.ModelAttribute import ModelAttribute
from src.parser.FileParser import FileParser
from src.dataclasses.model.Model import Model
from src.utils import get_short_description

class ModelParser(FileParser):
    """Parse a file that is inside of the "models" folder
    """

    def parse_file(self, file_path: str) -> Model:
        tree = self.get_tree(file_path)
        class_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        ret = Model()
        for node in class_nodes:
            ret.class_definition = f"class {node.name}"
            class_docstring = ast.get_docstring(node)
            if class_docstring:
                ret.short_description = get_short_description(class_docstring)
                ret.long_description = class_docstring
            for child_node in node.body:
                if isinstance(child_node, ast.Assign) and isinstance(child_node.targets[0], ast.Name):
                    attribute = ModelAttribute()
                    attribute.name = child_node.name
                    if isinstance(child_node.annotation, ast.Name):
                        attribute.attribute_type = child_node.annotation.id
                    elif isinstance(child_node.annotation, ast.Str):  # Handle str type for Python 3.7
                        attribute.attribute_type = child_node.annotation.s
                    else:
                        raise Exception(f"Unknown annotation type: {type(child_node.annotation)}")

                    docstring = ast.get_docstring(child_node)
                    if docstring:
                        docstring_lines = docstring.split("\nExample:")
                        attribute.description = docstring_lines[0]
                        attribute.example = docstring_lines[1]

                    ret.attributes.append(attribute)

        return ret
