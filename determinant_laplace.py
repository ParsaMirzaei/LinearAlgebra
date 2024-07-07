def determinant_laplace(matrix, memo=None):
    if memo is None:
        memo = {}
    # Convert matrix to a tuple of tuples to make it hashable for memoization
    matrix_tuple = tuple(map(tuple, matrix))
    if matrix_tuple in memo:
        return memo[matrix_tuple]

    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for col in range(len(matrix)):
        sub_matrix = [row[:col] + row[col + 1:] for row in matrix[1:]]
        sign = (-1) ** col
        det += sign * matrix[0][col] * determinant_laplace(sub_matrix, memo)

    memo[matrix_tuple] = det
    return det


if __name__ == '__main__':
    matrix = []
    n = int(input())
    for i in range(n):
        line = input().split()
        matrix.append([float(number) for number in line])
    det = determinant_laplace(matrix)
    print(int(det))
