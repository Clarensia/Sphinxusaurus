from dataclasses import dataclass, field
from typing import List

from src.dataclasses.main_class.MainClass import MainClass


@dataclass
class Project:
    """dataclass that represent the entire Project
    """

    main_classes: List[MainClass] = field(default_factory=list)
    """The main classes that we use to interact with the API.
    
    These mainclasses are located at the root of the folder
    """

    
