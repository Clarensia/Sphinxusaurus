from dataclasses import dataclass, field
from typing import List

from src.dataclasses.Attribute import Attribute


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

    is_abstract: bool = False
    """If the class is an abstract class or not
    
    The abstract class is usually the parent class of every other
    exceptions, this way, the client can simply catch the parent
    exception to know that the exception comes from our client and
    not from somewhere else
    """

    attributes: List[Attribute] = field(default_factory=list)
    """The list of attributes that we have for the exception.
    
    Usually, we only have:
    - status_code
    - detail
    """
