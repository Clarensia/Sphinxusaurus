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

def create_folder_name(camel_case_class: str) -> str:
    """Transform a CamelCase class name to a name with a hyphen.
    
    For example:
    CamelCase -> camel-case

    :param camel_case_class: The name of the class in CamelCase
    :type camel_case_class: str
    :return: The name of the class in lowercase with hyphen separation: camel-case
    :rtype: str
    """
    s = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camel_case_class)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', camel_case_class).lower()
