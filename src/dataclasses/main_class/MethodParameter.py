from dataclasses import dataclass


@dataclass()
class MethodParameter:
    """Each method from the MainClass have some parameter that the user
    have to specify (example: the blockchain, the exchanges...)
    """

    name: str
    """The name of the parameter
    """

    description: str
    """The description of the parameter
    """

    param_type: str
    """The Python type of the variable
    """
    
    example: str
    """The example that we write down.
    
    It is gathered as an str even if it is an integer because
    when we write our display, we don't care if it is an int or
    an str.
    """
