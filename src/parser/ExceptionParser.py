from src.dataclasses.exception.ExceptionModel import ExceptionModel
from src.parser.FileParser import FileParser


class ExceptionParser(FileParser):
    """Parse exceptions from the file
    """

    def parse_file(self, file_path: str) -> ExceptionModel:
        pass
