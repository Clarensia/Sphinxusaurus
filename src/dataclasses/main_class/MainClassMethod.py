from dataclasses import dataclass, field
from typing import List
from src.dataclasses.MethodException import MethodException
from src.dataclasses.MethodParameter import MethodParameter

@dataclass()
class MainClassMethod:
    """The main class will have multiple methods
    
    These methods are the one that interact with our API
    """

    definition: str = None
    """The definition of the method
    
    For example:
    async def amount_out(self, blockchain: str, tokenIn: str, tokenOut: str, amountIn: int, exchange: str | None = None) -> List[AmountOut]:
    """

    short_description: str = None
    """The small description of the method.
    
    We will put this value inside of the metadata of the page as description
    """
    
    long_description: str = None
    """The long description of the method
    
    This description is longer than the short one and may include multiple lines
    """

    parameters: List[MethodParameter] = field(default_factory=list)
    """Each method have multiple parameters, this list will contain them
    in the right order.
    """

    return_type: str = None
    """The returned type
    """

    example_response: str = None
    """An example of a possible response from the API.
    
    For example:
```json
[
    {
        "blockchain": "avalanche",
        "exchange": "lydia_finance_avalanche",
        "tokenIn": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
        "tokenOut": "0xde3A24028580884448a5397872046a019649b084",
        "amountIn": 1000000000000000000,
        "amountOut": 11088529
    }
]
```
    
    (we include the: ```json because it is part of the description)
    
    Please note that the example response have no space at the begining of the line
    """

    return_description: str = None
    """The description that we will put for each return value
    """

    exceptions: List[MethodException] = field(default_factory=list)
    """The exception that the method can throw
    """
