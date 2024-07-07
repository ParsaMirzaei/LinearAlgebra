def get_submatrix(matrix, row, col):
    return [matrix[i][:col] + matrix[i][col + 1:] for i in range(len(matrix)) if i != row]


def swap_rows(matrix, row1, row2):
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    return matrix


def recursive_determinant(matrix):
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    M11 = get_submatrix(matrix, 0, 0)
    M1n = get_submatrix(matrix, 0, n - 1)
    Mn1 = get_submatrix(matrix, n - 1, 0)
    Mnn = get_submatrix(matrix, n - 1, n - 1)

    M11nn = get_submatrix(get_submatrix(matrix, 0, 0), n - 2, n - 2)

    det_M11 = recursive_determinant(M11)
    det_M1n = recursive_determinant(M1n)
    det_Mn1 = recursive_determinant(Mn1)
    det_Mnn = recursive_determinant(Mnn)

    det_M11nn = recursive_determinant(M11nn)

    if det_M11nn == 0:
        # Try swapping rows to avoid division by zero
        for i in range(1, n):
            if matrix[i][0] != 0:
                matrix = swap_rows(matrix, 0, i)
                break

        M11 = get_submatrix(matrix, 0, 0)
        M1n = get_submatrix(matrix, 0, n - 1)
        Mn1 = get_submatrix(matrix, n - 1, 0)
        Mnn = get_submatrix(matrix, n - 1, n - 1)
        M11nn = get_submatrix(get_submatrix(matrix, 0, 0), n - 2, n - 2)

        det_M11 = recursive_determinant(M11)
        det_M1n = recursive_determinant(M1n)
        det_Mn1 = recursive_determinant(Mn1)
        det_Mnn = recursive_determinant(Mnn)
        det_M11nn = recursive_determinant(M11nn)

        # Because row changing
        det_M11nn *= -1

        if det_M11nn == 0:
            return 0
    det = (det_M11 * det_Mnn - det_M1n * det_Mn1) / det_M11nn

    return det


if __name__ == '__main__':
    matrix = []
    n = int(input())
    for i in range(n):
        line = input().split()
        matrix.append([float(number) for number in line])
    det = recursive_determinant(matrix)
    print(int(det))
