from os import listdir
from os.path import isfile, join

from src.dataclasses.Project import Project
from src.parser.ExceptionParser import ExceptionParser
from src.parser.InitParser import InitParser
from src.parser.MainClassParser import MainClassParser
from src.parser.ModelParser import ModelParser


class ProjectParser:
    def __init__(self):
        self._main_class_parser = MainClassParser()
        self._module_init_parser = InitParser()
        self._model_parser = ModelParser()
        self._exception_parser = ExceptionParser()
    
    def parse_project(self, folder_location: str) -> Project:
        """Parse the given folder that contains our module to a
        Project that contains extracted documentation

        :param folder_location: The location of the folder that we have to parse
        :type folder_location: str
        :return: The Project which has extracted docstrings
        :rtype: Project
        """
        ret = Project()
        main_files_paths = [join(folder_location, f) for f in listdir(folder_location) if isfile(join(folder_location, f))]
        for main_file in main_files_paths:
            ret.main_classes.append(self._main_class_parser.parse_file(main_file))

        models_folder = join(folder_location, "models")
        models_files = [f for f in listdir(models_folder) if isfile(join(models_folder, f))]
        for model_file in models_files:
            curr_model_path = join(models_folder, model_file)
            if model_file == "__init__.py":
                ret.init_doc["models"] = self._module_init_parser.parse_file(curr_model_path)
            else:
                ret.models.append(self._model_parser.parse_file(curr_model_path))

        exceptions_folder = join(folder_location, "exceptions")
        exceptions_files = [f for f in listdir(exceptions_folder) if isfile(join(exceptions_folder, f))]
        for exception_file in exceptions_files:
            curr_exception_path = join(exceptions_folder, exception_file)
            if exception_file == "__init__.py":
                ret.init_doc["exceptions"] = self._module_init_parser.parse_file(curr_exception_path)
            else:
                ret.exceptions.append(self._exception_parser.parse_file(curr_exception_path))

        return ret
