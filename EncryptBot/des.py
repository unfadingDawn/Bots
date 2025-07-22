# DES (Стандарт шифрования данных) - это алгоритм симметричного блочного шифрования. Он разделяет данные на блоки фиксированного размера и
# применяет несколько циклов замен и перестановок на основе 56-битного ключа. Несмотря на свою историческую
# важно отметить, что DES теперь уязвим для атак методом перебора из-за своей короткой длины ключа.

from pyDes import des, PAD_PKCS5
import binascii


def encrypt(key, word):
    cipher = des(key, padmode=PAD_PKCS5)

    word_bytes = word.encode('utf-8')

    encrypted_bytes = cipher.encrypt(word_bytes)

    encrypted_hex = binascii.hexlify(encrypted_bytes)

    return encrypted_hex.decode('utf-8')


def decrypt(key, encrypted_word):
    cipher = des(key, padmode=PAD_PKCS5)

    encrypted_hex = encrypted_word

    encrypted_bytes = binascii.unhexlify(encrypted_hex)

    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    decrypted_word = decrypted_bytes.decode('utf-8')

    return decrypted_word
