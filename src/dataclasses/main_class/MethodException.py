from dataclasses import dataclass


@dataclass()
class MethodException:
    """Represent the exceptions that a method can throw
    """
    
    exception: str
    """The name of the exception
    """
    
    description: str
    """The description of the exception
    """
