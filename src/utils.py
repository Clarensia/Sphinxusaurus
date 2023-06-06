def get_short_description(long_description: str) -> str:
    """Get the short description from a long description.
    
    The short description is the text that is before a "\n\n"

    :param long_description: The long description that we have
    :type long_description: str
    :return: The short description extracted
    :rtype: str
    """
    return long_description.split("\n\n", 1)[0].replace("\n", "")
