import os

from src.dataclasses.Project import Project
from src.dataclasses.main_class.MainClass import MainClass
from src.utils import create_folder_name


class Writer:

    def __init__(self, dest_path: str):
        self._dest_path = dest_path
        self._verify_folder()

    def _verify_folder(self):
        if os.path.exists(self._dest_path):
            print(f"Destination path: {self._dest_path} exists, can't run the program")
            os.exit(1)

    def _create_folder_in_dest(self, folder: str):
        os.mkdir(os.path.join(self._dest_path, folder))

    def _create_dest_folder(self):
        os.mkdir(self._dest_path)
        self._create_folder_in_dest("models")
        self._create_folder_in_dest("exceptions")

    def _get_metadata(self, title: str, description: str, sidebar_class_name: str | None) -> str:
        """Create the metadata header for the given file

        :param title: The title of the file
        :type title: str
        :param description: The short description
        :type description: str
        :param sidebar_class_name: If we are in a description of th main file, we put the
                                   class name here. If not, then we create a normal header
        :type sidebar_class_name: str | None
        :return: The metadata that we wrote
        :rtype: str
        """
        ret = "---\n"
        ret += f"title: {title}\n"
        ret += f"description: {description}"
        if sidebar_class_name is not None:
            ret += "sidebar_position: 3\n"
            ret += f"sidebar_class_name: {sidebar_class_name}\n"
        ret += "---\n"
        
        return ret

    def _create_module_main_file(self, folder_name: str, class_name: str, short_description: str, long_description: str):
        to_write = self._get_metadata(class_name, short_description, f"sidebar-{folder_name}")
        to_write += "\n"

        to_write += long_description

        with open(os.path.join(self._dest_path, folder_name, f"{folder_name}.md"), "w+") as f:
            f.write(to_write)

    def _write_main_class(self, main_class: MainClass):
        folder_name = create_folder_name(main_class.name)
        self._create_folder_in_dest(folder_name)
        self._create_module_main_file(self,
                                      folder_name,
                                      main_class.name,
                                      main_class.short_description,
                                      main_class.long_description)
        

    def write(self, project: Project):
        self._create_dest_folders()
        for main_class in project.main_classes:
            self._write_main_class(main_class)
