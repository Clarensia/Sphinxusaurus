from dataclasses import dataclass, field
from typing import List

from src.dataclasses.ModelAttribute import ModelAttribute


@dataclass
class ExceptionModel:
    """The model that describe an expression
    """

    definition: str | None = None
    """The definition of the Exception class.
    
    For example:
    class BLockchainNotSupportedException(BlockchainAPIsException):
    """

    short_description: str | None = None
    """The short description that will be inside of the meta parameters
    """
    
    long_description: str | None = None
    """The long description that will be written inside of the file
    """

    attributes: List[ModelAttribute] = field(default_factory=list)
    """The list of attributes that we have for the exception.
    
    Usually, we only have:
    - status_code
    - detail
    """
