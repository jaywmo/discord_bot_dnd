import numpy as np


def _roll(size=1, limit=20, add_type=None, add=0, repeat=1):
    # returns result as array in string form and result_sum as integer
    result = np.random.randint(1, limit + 1, size=(repeat, size))
    if add_type == 'r+':
        result_sum = np.sum(result + add, axis=1)
    else:
        result_sum = np.sum(result, axis=1) + add

    result = np.array([np.array2string(rolls, separator=', ') for rolls in result], dtype=str)
    return result, result_sum
