from dataclasses import dataclass, field
from typing import List

from src.dataclasses.model.ModelAttribute import ModelAttribute


@dataclass
class Model:
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

    attributes: List[ModelAttribute] = field(default_factory=list)
