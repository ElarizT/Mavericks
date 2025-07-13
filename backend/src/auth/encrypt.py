import cryptocode
from src.core.settings import get_settings

settings = get_settings()


def encrypt_secret(secret: str) -> str:
    return cryptocode.encrypt(secret, settings.SECRET_KEY)


def decrypt_secret(encrypted_secret: str) -> str:
    decrypted_secret = cryptocode.decrypt(encrypted_secret, settings.SECRET_KEY)
    if not decrypted_secret:
        raise ValueError("Decryption failed. Invalid key or data.")
    return decrypted_secret
