from dataclasses import dataclass, field
from typing import List

from src.dataclasses.MainClassMethod import MainClassMethod


@dataclass()
class MainClass:
    """Represent the main class that is parsed
    """

    name: str = None
    """The name of the main class
    """
    
    short_description: str = None
    """The short description that we will use inside of the metadata
    """
    
    long_description: str = None
    """The long description of the class
    """

    methods: List[MainClassMethod] = field(default_factory=list)
    """The list of methods that are defined inside of the class
    """
