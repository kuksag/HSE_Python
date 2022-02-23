import numpy as np
from copy import copy
from functools import lru_cache


class PerfectHash:
    """
    hash(matrix) = 3 * |rows| + 5 * |cols| + 13
    """

    def __eq__(self, other):
        return np.array_equal(self.data, other.data)

    def __hash__(self):
        return 3 * self.data.shape[0] + 5 * self.data.shape[1] + 13


class Matrix(PerfectHash):
    @staticmethod
    def _check_dimensions(value):
        flag = True
        for row in value:
            flag &= len(row) == len(value)
        if not flag:
            raise ValueError("Bad dimensions")

    def __init__(self, data):
        self._check_dimensions(data)
        self.data = np.asarray(data)

    __hash__ = PerfectHash.__hash__

    def __repr__(self):
        return 'Matrix' + str(self.data)

    def __add__(self, other):
        if self.data.shape != other.data.shape:
            raise ValueError("Different dimensions")
        result = copy(self.data)
        for i, row in enumerate(other.data):
            result[i] += row
        return Matrix(result)

    def __matmul__(self, other):
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Different dimensions")
        result = copy(self.data)
        return Matrix(result * other.data)

    def __mul__(self, other):
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Different dimensions")
        result = copy(self.data)
        for i, row in enumerate(other.data):
            result[i] *= row
        return Matrix(result)


cache = dict()


def cached_mult(lhs: Matrix, rhs: Matrix) -> Matrix:
    if hash((lhs, rhs)) not in cache:
        cache[hash((lhs, rhs))] = lhs @ rhs
    return cache[hash((lhs, rhs))]
