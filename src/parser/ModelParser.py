import ast
from typing import List, Tuple
from src.dataclasses.Attribute import Attribute
from src.parser.FileParser import FileParser
from src.dataclasses.Model import Model
from src.utils import get_short_description

class ModelParser(FileParser):
    """Parse a file that is inside of the "models" folder
    """

    def parse_file(self, file_path: str) -> Model:
        tree = self.get_tree(file_path)
        class_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        ret = Model()
        for node in class_nodes:
            ret.name = node.name
            ret.class_definition = f"class {node.name}"
            class_docstring = ast.get_docstring(node)
            if class_docstring:
                ret.short_description = get_short_description(class_docstring)
                ret.long_description = class_docstring
            self.add_attributes_from_class_to_list(ret.attributes, node.body)

        return ret
