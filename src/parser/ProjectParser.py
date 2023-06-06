from os import listdir
from os.path import isfile, join

from src.dataclasses.Project import Project
from src.parser.InitParser import InitParser
from src.parser.MainClassParser import MainClassParser


class ProjectParser:
    def __init__(self):
        self._main_class_parser = MainClassParser()
        self._module_init_parser = InitParser()
    
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
                pass

        return ret
