from attrs import define, field
from copy import copy
import numpy as np
import os


ARTIFACT_FOLDER = 'artifact'


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

    def __mul__(self, other):
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Different dimensions")
        result = copy(self.data)
        return Matrix(result * other.data)

    def __mod__(self, other):
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Different dimensions")
        result = copy(self.data)
        for i, row in enumerate(other.data):
            result[i] *= row
        return Matrix(result)


def check_sum():
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    if not os.path.exists(ARTIFACT_FOLDER):
        os.makedirs(ARTIFACT_FOLDER)
    with open(os.path.join(ARTIFACT_FOLDER, 'matrix+.txt'), 'w+') as file:
        file.write(str(a + b))


def check_matrix_mult():
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    if not os.path.exists(ARTIFACT_FOLDER):
        os.makedirs(ARTIFACT_FOLDER)
    with open(os.path.join(ARTIFACT_FOLDER, 'matrix+.txt'), 'w+') as file:
        file.write(str(a + b))


def check_matrix_elem_mult():
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    if not os.path.exists(ARTIFACT_FOLDER):
        os.makedirs(ARTIFACT_FOLDER)
    with open(os.path.join(ARTIFACT_FOLDER, 'matrix@.txt'), 'w+') as file:
        file.write(str(a % b))


if __name__ == '__main__':
    np.random.seed(0)
    check_sum()
    check_matrix_mult()
    check_matrix_elem_mult()