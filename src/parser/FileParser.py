from abc import ABC, abstractmethod
import ast
from typing import Any, List, Tuple

from src.dataclasses.Attribute import Attribute


class FileParser(ABC):
    """An abstract parser that has helper methods in order to parse
    a file
    """

    def add_attributes_from_class_to_list(self, attributes: List[Attribute], body: List[ast.Expr | ast.AnnAssign]):
        """Add the attributes of the class to the given list in-place

        :param attributes: The list of attributes that we have to fill
        :type attributes: List[Attribute]
        :param body: The body of the node of the class
        :type body: List[ast.Expr  |  ast.AnnAssign]
        """
        attributes_desc = self.get_attribute_nodes(body)
        for definition, description in attributes_desc:
            attribute = Attribute()
            attribute.name = definition.target.id
            attribute.attribute_type = ast.unparse(definition.annotation)
            doc_lines = description.value.value.split("\n\n    Example:")
            attribute.attribute_description = doc_lines[0]
            attribute.example = doc_lines[1]
            attributes.attributes.append(attribute)

    def get_attribute_nodes(self, body: List[ast.Expr | ast.AnnAssign]) -> Tuple[ast.AnnAssign, ast.Expr]:
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

    def get_tree(self, path: str) -> ast.Module:
        with open(path, "r") as source:
            return ast.parse(source.read())

    @abstractmethod
    def parse_file(self, file_path: str) -> Any:
        pass
