
def dictionary_path(dictionary: dict, path: str):
    """Get value from dictionary using path"""
    for key in path.split("/"):
        dictionary = dictionary[key]
    return dictionary