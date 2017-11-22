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