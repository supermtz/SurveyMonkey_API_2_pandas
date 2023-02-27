
# def dictionary_path(dictionary: dict, path: str):
#     """Get value from dictionary using path"""
#     for key in path.split("/"):
#         dictionary = dictionary[key]
#     return dictionary

def get_nested_value(data: dict, path: str) -> str | int | list | dict:
    """Get a value from a nested path"""
    path = path.split("/")

    for key in path:
        if isinstance(data, list):
            data = data[int(key)]
        else:
            data = data[key]

    return data

def get_values(data: dict, *args) -> tuple[str | int | list | dict]:
    """Get values from a nested dictionary"""
    values = []

    for arg in args:
        values.append(get_nested_value(data, arg))

    return tuple(values)