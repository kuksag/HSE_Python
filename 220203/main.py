import numpy as np
import os
from matrix import Matrix, cached_mult
from number import ArrayLike

ARTIFACT_FOLDER = 'artifact'


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
    with open(os.path.join(ARTIFACT_FOLDER, 'matrix@.txt'), 'w+') as file:
        file.write(str(a @ b))


def check_matrix_elem_mult():
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    if not os.path.exists(ARTIFACT_FOLDER):
        os.makedirs(ARTIFACT_FOLDER)
    with open(os.path.join(ARTIFACT_FOLDER, 'matrix*.txt'), 'w+') as file:
        file.write(str(a * b))


def check_numbers():
    a = ArrayLike(2)
    b = ArrayLike(3)
    if not os.path.exists(ARTIFACT_FOLDER):
        os.makedirs(ARTIFACT_FOLDER)
    a.dump(os.path.join(ARTIFACT_FOLDER, 'numbers_dump.txt'))

    with open(os.path.join(ARTIFACT_FOLDER, 'numbers_dump.txt'), 'a') as fd:
        print(str(a + b), file=fd)
        print(str(a - b), file=fd)
        print(str(a * b), file=fd)
        print(str(a / b), file=fd)


def create_collision():
    a = Matrix([[1, 2],
                [3, 4]])
    b = d = Matrix([[5, 6],
                    [7, 8]])
    c = Matrix([[9, 10],
                [11, 12]])

    assert hash(a) == hash(c)
    assert a != c
    assert (b == d)
    assert (a @ b != c @ d)

    if not os.path.exists(ARTIFACT_FOLDER):
        os.makedirs(ARTIFACT_FOLDER)

    with open(os.path.join(ARTIFACT_FOLDER, 'A.txt'), 'w+') as fd:
        print(a, file=fd)

    with open(os.path.join(ARTIFACT_FOLDER, 'B.txt'), 'w+') as fd:
        print(b, file=fd)

    with open(os.path.join(ARTIFACT_FOLDER, 'C.txt'), 'w+') as fd:
        print(c, file=fd)

    with open(os.path.join(ARTIFACT_FOLDER, 'D.txt'), 'w+') as fd:
        print(d, file=fd)

    with open(os.path.join(ARTIFACT_FOLDER, 'AB.txt'), 'w+') as fd:
        print(a @ b, file=fd)

    with open(os.path.join(ARTIFACT_FOLDER, 'CD.txt'), 'w+') as fd:
        print(c @ d, file=fd)

    with open(os.path.join(ARTIFACT_FOLDER, 'hash.txt'), 'w+') as fd:
        print(hash(a @ b), file=fd)
        print(hash(c @ d), file=fd)


if __name__ == '__main__':
    np.random.seed(0)
    check_sum()
    check_matrix_mult()
    check_matrix_elem_mult()
    check_numbers()
    create_collision()
