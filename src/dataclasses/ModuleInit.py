from dataclasses import dataclass


@dataclass
class ModuleInit:
    """Represent the description of an __init__.py file
    
    Can be None if no docstring where found inside of the __init__.py file
    """

    short_description: str = None
    """The short description.
    
    Usually the first few lines of the description
    """

    long_description: str = None
    """All of the docstring of the __init__.py file
    """
