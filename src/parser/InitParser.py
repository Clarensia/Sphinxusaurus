import ast
from src.dataclasses.ModuleInit import ModuleInit
from src.parser.FileParser import FileParser


class InitParser(FileParser):

    def parse_file(self, path) -> ModuleInit:
        ret = ModuleInit()
        tree = self.get_tree(path)
        module_docstring = ast.get_docstring(tree)
        if module_docstring:
            ret.short_description = module_docstring.split("\n\n", 1)[0]
            ret.long_description = module_docstring
        return ret
