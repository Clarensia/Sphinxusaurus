from src.parser.FileParser import FileParser
from src.dataclasses.model.Model import Model

class ModelParser(FileParser):
    """Parse a file that is inside of the "models" folder
    """

    def parse_file(self, file_path: str) -> Model:
        pass
