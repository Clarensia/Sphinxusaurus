from abc import ABC, abstractmethod
import ast
from typing import Any


class FileParser(ABC):
    """An abstract parser that has helper methods in order to parse
    a file
    """

    def get_tree(self, path: str) -> ast.Module:
        with open(path, "r") as source:
            return ast.parse(source.read())

    @abstractmethod
    def parse_file(self, file_path: str) -> Any:
        pass
