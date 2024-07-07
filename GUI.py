import tkinter as tk
from tkinter import messagebox


def hill_cipher_encrypt(plaintext, key):
    n = len(key)
    plaintext = plaintext.upper().replace(" ", "_")
    plaintext += '_' * (-len(plaintext) % n)

    char_to_number = {chr(i + ord('A')): i for i in range(26)}
    char_to_number['_'] = 26

    plaintext_numbers = [char_to_number[char] for char in plaintext]
    ciphertext = []

    for i in range(0, len(plaintext_numbers), n):
        block = plaintext_numbers[i:i + n]
        encrypted_block = [(sum(key[i][j] * block[j] for j in range(n)) % 27) for i in range(n)]
        ciphertext.extend(encrypted_block)

    ciphertext = ''.join(chr(num + ord('A')) if num < 26 else '_' for num in ciphertext)
    return ciphertext


def hill_cipher_decrypt(ciphertext, key):
    n = len(key)
    ciphertext = ciphertext.upper().replace(" ", "")

    key_inv = matrix_mod_inverse(key, 27)
    ciphertext_numbers = [ord(char) - ord('A') if char != '_' else 26 for char in ciphertext]
    plaintext = []

    for i in range(0, len(ciphertext_numbers), n):
        block = ciphertext_numbers[i:i + n]
        decrypted_block = [(sum(key_inv[i][j] * block[j] for j in range(n)) % 27) for i in range(n)]
        plaintext.extend(decrypted_block)

    number_to_char = {i: chr(i + ord('A')) for i in range(26)}
    number_to_char[26] = '_'

    plaintext = ''.join(number_to_char[num] for num in plaintext)
    return plaintext.rstrip('_')


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
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def matrix_mod_inverse(matrix, mod):
    n = len(matrix)
    det = determinant_gaussian(matrix) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        return None

    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[matrix[m][k] for k in range(n) if k != j] for m in range(n) if m != i]
            adjugate[j][i] = ((-1) ** (i + j) * determinant_gaussian(minor)) % mod

    inverse = [[(adjugate[i][j] * det_inv) % mod for j in range(n)] for i in range(n)]
    return inverse


def is_valid_key(key, mod):
    try:
        inv_key = matrix_mod_inverse(key, mod)
        return inv_key is not None
    except Exception:
        return False


def encrypt_decrypt_handler():
    try:
        n = int(n_entry.get())
        key_text = key_text_widget.get("1.0", tk.END).strip()
        key = [[int(num) for num in row.split()] for row in key_text.split('\n') if row]

        if len(key) != n or any(len(row) != n for row in key):
            raise ValueError("Key matrix dimensions do not match the specified size n.")

        if not is_valid_key(key, 27):
            result_label.config(text="NO_VALID_KEY")
            return

        plaintext = plaintext_entry.get().strip()

        if encrypt_decrypt_var.get() == "Encrypt":
            ciphertext = hill_cipher_encrypt(plaintext, key)
            result_label.config(text=f"Ciphertext: {ciphertext}")
        elif encrypt_decrypt_var.get() == "Decrypt":
            plaintext = hill_cipher_decrypt(plaintext, key)
            result_label.config(text=f"Plaintext: {plaintext}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


if __name__ == '__main__':
    # GUI Setup
    root = tk.Tk()
    root.title("Hill Cipher Encryption and Decryption")

    tk.Label(root, text="Enter size of matrix n:").pack()
    n_entry = tk.Entry(root)
    n_entry.pack()

    tk.Label(root, text="Key Matrix (enter rows separated by newlines):").pack()
    key_text_widget = tk.Text(root, height=8, width=40)
    key_text_widget.pack()

    tk.Label(root, text="Enter Plaintext/Ciphertext:").pack()
    plaintext_entry = tk.Entry(root)
    plaintext_entry.pack()

    tk.Label(root, text="Select operation:").pack()
    encrypt_decrypt_var = tk.StringVar()
    encrypt_decrypt_var.set("Encrypt")
    tk.Radiobutton(root, text="Encrypt", variable=encrypt_decrypt_var, value="Encrypt").pack()
    tk.Radiobutton(root, text="Decrypt", variable=encrypt_decrypt_var, value="Decrypt").pack()

    encrypt_decrypt_button = tk.Button(root, text="Encrypt/Decrypt", command=encrypt_decrypt_handler)
    encrypt_decrypt_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()
