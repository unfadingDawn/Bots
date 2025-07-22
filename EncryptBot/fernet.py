# Шифр Фернет - это симметричный алгоритм шифрования, основанный на AES.
# Он шифрует данные с помощью ключа, полученного из парольной фразы, и включает аутентификацию для обеспечения целостности данных.
# Каждый токен содержит временную метку для предотвращения повторных атак.
# Он прост в использовании и популярен в приложениях на Python благодаря своему включению в криптографическую библиотеку.

from cryptography.fernet import Fernet


def encrypt(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message


def decrypt(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message
