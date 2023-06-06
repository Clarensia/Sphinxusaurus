import ast
from typing import List, Tuple
from src.dataclasses.model.ModelAttribute import ModelAttribute
from src.parser.FileParser import FileParser
from src.dataclasses.model.Model import Model
from src.utils import get_short_description

class ModelParser(FileParser):
    """Parse a file that is inside of the "models" folder
    """

    def _get_attribute_nodes(self, body: List[ast.Expr | ast.AnnAssign]) -> Tuple[ast.AnnAssign, ast.Expr]:
        """Inside of the class body, there is our definition of the attribute
        and there is also the documentation.
        
        The goal of this function is to pair the definition and the description.
        
        A definition is for example:
        blockchain: str
        
        A description is the docstring that is below it, for example:
        '''The id of the blockchain
        
        Example: ethereum
        '''

        All description looks like in the example description above

        :param body: The body that we get from the class node
        :type body: List[ast.Expr  |  ast.AnnAssign]
        :return: At first the definition node and as second the expression node that
                 contains the description of the attribute
        :rtype: Tuple[ast.AnnAssign, ast.Expr]
        """
        ret = []
        for i in range(1, len(body), 2):
            # We know that the first docstring is always the documentation of the class
            # the attributes starts from the second one
            ret.append((body[i], body[i + 1]))
        return ret

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
            attributes_desc = self._get_attribute_nodes(node.body)
            for definition, description in attributes_desc:
                attribute = ModelAttribute()
                attribute.name = definition.target.id
                if isinstance(definition.annotation, ast.Name):
                    attribute.attribute_type = definition.annotation.id
                elif isinstance(definition.annotation, ast.Str):  # Handle str type for Python 3.7
                    attribute.attribute_type = definition.annotation.s
                elif isinstance(definition.annotation, ast.Subscript):
                    attribute.attribute_type = ast.unparse(definition.annotation)
                else:
                    raise Exception(f"Unknown annotation type: {type(definition.annotation)}")

                doc_lines = description.value.value.split("\n\n    Example:")
                attribute.attribute_description = doc_lines[0]
                attribute.example = doc_lines[1]

        return ret
