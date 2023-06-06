from dataclasses import dataclass, field
from typing import Dict, List

from src.dataclasses.ModuleInit import ModuleInit
from src.dataclasses.main_class.MainClass import MainClass
from src.dataclasses.modelModel import Model


@dataclass
class Project:
    """dataclass that represent the entire Project
    """

    main_classes: List[MainClass] = field(default_factory=list)
    """The main classes that we use to interact with the API.
    
    These mainclasses are located at the root of the folder
    """

    models: List[Model] = field(default_factory=list)
    """The list of models in order"""

    init_doc: Dict[str, ModuleInit] = field(default_factory=dict)    
    """The documentation file for each module.
    
    normaly we should have as key:
    models
    exceptions
    main
    
    As value, we have a ModuleInit that has a short description and long description
    
    We usualy ignore the main __init__.py file
    """
