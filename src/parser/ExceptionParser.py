import ast
from src.dataclasses.Attribute import Attribute
from src.dataclasses.ExceptionModel import ExceptionModel
from src.parser.FileParser import FileParser
from src.utils import get_short_description


class ExceptionParser(FileParser):
    """Parse exceptions from the file
    """

    def parse_file(self, file_path: str) -> ExceptionModel:
        tree = self.get_tree(file_path)
        class_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        ret = ExceptionModel
        for node in class_nodes:
            ret.class_definition = ast.unparse(node).split(':')[0] + ':'
            ret.is_abstract = "ABC)" in ret.class_definition
            exception_docstring = ast.get_docstring(node)
            if exception_docstring:
                ret.short_description = get_short_description(exception_docstring)
                ret.long_description = exception_docstring

            self.add_attributes_from_class_to_list(ret.attributes, node.body)

        return ret
