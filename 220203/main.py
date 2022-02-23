import numpy as np
import os
from matrix import Matrix
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
    with open(os.path.join(ARTIFACT_FOLDER, 'matrix+.txt'), 'w+') as file:
        file.write(str(a @ b))


def check_matrix_elem_mult():
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))
    if not os.path.exists(ARTIFACT_FOLDER):
        os.makedirs(ARTIFACT_FOLDER)
    with open(os.path.join(ARTIFACT_FOLDER, 'matrix@.txt'), 'w+') as file:
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




if __name__ == '__main__':
    np.random.seed(0)
    check_sum()
    check_matrix_mult()
    check_matrix_elem_mult()
    check_numbers()