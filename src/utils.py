import re

def get_short_description(long_description: str) -> str:
    """Get the short description from a long description.
    
    The short description is the text that is before a "\n\n"

    :param long_description: The long description that we have
    :type long_description: str
    :return: The short description extracted
    :rtype: str
    """
    return long_description.split("\n\n", 1)[0].replace("\n", "")

def camel_to_dash_case(camel_case_name: str) -> str:
    """Transform a CamelCase name to a name with dashes.
    
    For example:
    CamelCase -> camel-case

    :param camel_case_name: The name of the string to transform in CamelCase
    :type camel_case_name: str
    :return: The name of the string in lowercase with hyphen separation: camel-case
    :rtype: str
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', camel_case_name).lower()

def is_native_type(obj: str) -> bool:
    """Verify if the given string object is a native type or not.
    
    A native type is for example:
    - "int"
    - "str"

    :param obj: The object that we are willing to write
    :type obj: str
    :return: `True` if the given object is a native type, `False` otherwise
    :rtype: bool
    """
    return obj == "int" or obj == "str"
