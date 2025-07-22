# Шифр Цезаря сдвигает каждую букву в открытом тексте на фиксированное количество позиций вниз по алфавиту.
# Это базовый шифр подстановки, в котором один и тот же ключ (значение сдвига) используется как для шифрования, так и для дешифрования.
# Однако из-за своей простоты он очень уязвим для атак методом перебора и частотного анализа.
# Этот алгоритм пропускает числа
import re
from re import Match


def is_valid(s):
    reg_exp = re.compile(r"^[\u0401\u0451\u0410-\u044fa-zA-Z0-9?><; ,{}[\]\-_+=!@#$%^&*|']*$")
    return reg_exp.match(s)


def is_russian(s):
    reg_exp = re.compile(r"^[\u0401\u0451\u0410-\u044f0-9?><; ,{}[\]\-_+=!@#$%^&*|']*$")
    return reg_exp.match(s)


def cae_enc(string: str, key) -> str:
    ret: list[str] = []
    for char in string:
        ret.append(encrypt(char, key))
    return ''.join(ret)


def cae_dec(string: str, key) -> str:
    ret: list[str] = []
    for char in string:
        ret.append(decrypt(char, key))
    return ''.join(ret)


def encrypt(message, key):
    if is_russian(message) is not None:
        alphabet_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        alphabet_upper = alphabet_lower.upper()

        def shift_char(char, shift, alphabet):
            if char in alphabet:
                new_pos = (alphabet.index(char) + shift) % len(alphabet)
                return alphabet[new_pos]
            else:
                return char

        # Encrypt the text
        encrypted_text = ''
        for char in message:
            if char in alphabet_lower:
                encrypted_text += shift_char(char, key, alphabet_lower)
            elif char in alphabet_upper:
                encrypted_text += shift_char(char, key, alphabet_upper)
            else:
                encrypted_text += char

        return encrypted_text
    else:
        assert is_valid(message)

        encrypted_message = ""
        for char in message:
            if char.isupper():
                encrypted_char = chr((ord(char) - 65 + key) % 26 + 65)
            elif char.islower():
                encrypted_char = chr((ord(char) - 97 + key) % 26 + 97)
            else:
                encrypted_char = char
            encrypted_message += encrypted_char
        return encrypted_message


def decrypt(encrypted_message, key):
    assert is_valid(encrypted_message)
    if is_russian(encrypted_message) is not None:
        alphabet_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        alphabet_upper = alphabet_lower.upper()

        def shift_char(char, shift, alphabet):
            if char in alphabet:
                new_pos = (alphabet.index(char) - shift) % len(alphabet)
                return alphabet[new_pos]
            else:
                return char

        # Decrypt the text
        decrypted_text = ''
        for char in encrypted_message:
            if char in alphabet_lower:
                decrypted_text += shift_char(char, key, alphabet_lower)
            elif char in alphabet_upper:
                decrypted_text += shift_char(char, key, alphabet_upper)
            else:
                decrypted_text += char

        return decrypted_text
    else:
        decrypted_message = ""
        for char in encrypted_message:
            if char.isupper():
                decrypted_char = chr((ord(char) - 65 - key) % 26 + 65)
            elif char.islower():
                decrypted_char = chr((ord(char) - 97 - key) % 26 + 97)
            else:
                decrypted_char = char
            decrypted_message += decrypted_char
        return decrypted_message
