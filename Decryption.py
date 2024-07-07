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
    return int(det)


def mod_inverse(a, m):
    """Find the modular inverse of an under modulo m"""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def matrix_mod_inverse(matrix, mod):
    """Find the inverse of a nxn matrix under modulo mod"""
    n = len(matrix)
    det = determinant_gaussian(matrix) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        raise ValueError("Matrix is not invertible")

    # Create the adjugate matrix
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[matrix[m][k] for k in range(n) if k != j] for m in range(n) if m != i]
            adjugate[j][i] = ((-1) ** (i + j) * determinant_gaussian(minor)) % mod

    # Multiply adjugate matrix by the modular inverse of the determinant
    inverse = [[(adjugate[i][j] * det_inv) % mod for j in range(n)] for i in range(n)]
    return inverse


def hill_cipher_decrypt(ciphertext, key):
    """Decrypt ciphertext using Hill cipher with given key matrix"""
    n = len(key)
    ciphertext = ciphertext.upper().replace(" ", "")

    key_inv = matrix_mod_inverse(key, 27)  # Use 27 for mod
    ciphertext_numbers = [ord(char) - ord('A') if char != '_' else 26 for char in ciphertext]  # Map to numbers
    plaintext = []

    for i in range(0, len(ciphertext_numbers), n):
        block = ciphertext_numbers[i:i + n]
        decrypted_block = [(sum(key_inv[i][j] * block[j] for j in range(n)) % 27) for i in range(n)]  # Use 27 for mod
        plaintext.extend(decrypted_block)

    # Map numbers back to characters including '_'
    number_to_char = {i: chr(i + ord('A')) for i in range(26)}
    number_to_char[26] = '_'

    plaintext = ''.join(number_to_char[num] for num in plaintext)
    return plaintext.rstrip('_')  # Remove padding if any


if __name__ == '__main__':
    key_matrix = []
    n = int(input())
    for i in range(n):
        line = input().split()
        key_matrix.append([int(number) for number in line])
    ciphertext = input()
    decrypted_text = hill_cipher_decrypt(ciphertext, key_matrix)
    print(decrypted_text)
