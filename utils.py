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


def edit_dist(w1, w2):
    """
    finds levenshtein distance between two strings by flood filling a matrix
    :param w1: first word
    :param w2: second word
    :return: edit distance (alignment?)
    """
    # create a m + 1 X n + 1 matrix for word alignment
    matrix = []
    line = [0 for x in range(len(w1) + 1)]
    for y in range(len(w2) + 1):
        matrix.append(line.copy())

    # fill in the first bits
    for x in range(1, len(w1) + 1):
        matrix[0][x] = x
    for y in range(1, len(w2) + 1):
        matrix[y][0] = y

    # flood fill the matrix
    for y in range(1, len(w2) + 1):
        for x in range(1, len(w1) + 1):
            if w1[x - 1] == w2[y - 1]:
                matrix[y][x] = matrix[y - 1][x - 1]
            else:
                matrix[y][x] = min(matrix[y - 1][x], matrix[y - 1][x - 1],
                                   matrix[y][x - 1]) + 1

    return matrix[len(w2)][len(w1)]


def spellcheck(word, w_dict):
    """
    returns the best match from w_dict based on edit distance
    :param word: word to check for
    :param w_dict: dictionary containing the words we want
    :return: best match, or word if it exists
    """
    if word in w_dict:
        return word

    # generate lev distances for each word in w_dict, sort them based on score
    # and subsort alphabetically before returning first item
    else:
        matches = [(x, edit_dist(word, x)) for x in w_dict.keys()]
        try:
            sorted(matches, key=lambda x: (x[1], x[0]))[0][0]
        except Exception as e:
            return e


