from numba import njit
import numpy as np


@njit
def _find_matching_ngrams(left, right, min_n=5):
    """
    Helper function for `find_matching_ngrams`
    This does the actual computation, operating on numpy arrays
    """
    found_values = []
    lidx = 0
    while lidx < len(left):
        for ridx in range(len(right)):
            length = 0
            while right[ridx + length] == left[lidx + length]:
                length += 1
            if length >= min_n:
                found_values.append((lidx, ridx, length))
                lidx += length - 1
        lidx += 1
    found = np.array(found_values)
    return found[:, 0], found[:, 1], found[:, 2]

