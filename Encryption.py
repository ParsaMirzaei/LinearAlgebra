def hill_cipher_encrypt(plaintext, key):
    """Encrypt plaintext using Hill cipher with given key matrix"""
    n = len(key)
    plaintext = plaintext.upper().replace(" ", "_")
    plaintext += '_' * (-len(plaintext) % n)  # Ensure plaintext length is divisible by n

    # Map characters to numbers including '_'
    char_to_number = {chr(i + ord('A')): i for i in range(26)}
    char_to_number['_'] = 26

    plaintext_numbers = [char_to_number[char] for char in plaintext]
    ciphertext = []

    # Encrypt each block of size n
    for i in range(0, len(plaintext_numbers), n):
        block = plaintext_numbers[i:i + n]
        encrypted_block = [(sum(key[i][j] * block[j] for j in range(n)) % 27) for i in range(n)]  # Use 27 for mod
        ciphertext.extend(encrypted_block)

    ciphertext = ''.join(chr(num + ord('A')) if num < 26 else '_' for num in ciphertext)  # Map back to characters
    return ciphertext


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


def isInverseAble(matrix, mod):
    """Find the inverse of a nxn matrix under modulo mod"""
    det = determinant_gaussian(matrix) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        return False
    return True


if __name__ == '__main__':
    key_matrix = []
    n = int(input())
    for i in range(n):
        line = input().split()
        key_matrix.append([int(number) for number in line])
    if isInverseAble(key_matrix, 27):
        plaintext = input()
        ciphertext = hill_cipher_encrypt(plaintext, key_matrix)
        print(ciphertext)
    else:
        print("NO_VALID_KEY")
