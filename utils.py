import json

"""
This module provides some functions you may find useful.
"""

def mention(user) -> str:
    """
    Creates a mention string from a discord user.

    :param user: Target discord user.
    :return: Mention string.
    """
    return '<@' + user.id + '>'


def load_json(path: str):
    """
    Loads JSON from a file.

    :param path: Filepath to load JSON from.abs
    :return: JSON from file.
    """
    with open(path) as f:
        return json.load(f)


def save_json(path: str, json_obj): 
    """
    Saves JSON to a file. 

    :param path: Filepath to save JSON to.
    :param json_obj: JSON object to save.
    """
    with open(path, 'w') as f:
        json.dump(json_obj, f, indent=4)