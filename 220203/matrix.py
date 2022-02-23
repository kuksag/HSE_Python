from attrs import define, field
from copy import copy


def _check_dimensions(instance, attribute, value):
    flag = True
    for row in value:
        flag &= len(row) == len(value)
    if not flag:
        raise ValueError("Bad dimensions")


@define(frozen=True)
class Matrix:
    data = field(validator=_check_dimensions)

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
