from dataclasses import dataclass


@dataclass
class Attribute:
    """Represent the attribute of a class
    """

    name: str | None = None
    """The name of the field that we use
    """

    attribute_description: str | None = None
    """The description of the attribute
    """

    attribute_type: str | None = None
    """The type of the attribute written as string
    """

    example: str | None = None
    """An example for the given attribute
    """
