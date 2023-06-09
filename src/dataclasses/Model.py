from dataclasses import dataclass, field
from typing import List

from src.dataclasses.Attribute import Attribute


@dataclass
class Model:
    name: str | None = None
    """The name of the model
    
    For example: AmountIn
    """

    class_definition: str | None = None
    """The defintion of the class.
    
    It should be:
    class [ClassName]:
    
    For example:
    class AmountIn:
    """

    short_description: str | None = None
    """The short description of the class that will go inside of the metadata
    """

    long_description: str | None = None
    """The long description of the class that will go inside of the description
    of the category inside of the documentation
    """

    attributes: List[Attribute] = field(default_factory=list)
