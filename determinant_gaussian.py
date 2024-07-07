def determinant_gaussian(matrix):
    matrix = [[float(element) for element in row] for row in matrix]
    n = len(matrix)
    det = 1

    for i in range(n):
        pivot = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[pivot][i]):
                pivot = j

        if matrix[pivot][i] == 0:
            return 0

        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
            det *= -1

        det *= matrix[i][i]

        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            matrix[j][i:] = [matrix[j][k] - factor * matrix[i][k] for k in range(i, n)]

    det = round(det) if abs(det - round(det)) < 1e-9 else det
    return det


if __name__ == '__main__':
    matrix = []
    n = int(input())
    for i in range(n):
        line = input().split()
        matrix.append([float(number) for number in line])
    det = determinant_gaussian(matrix)
    print(int(det))
