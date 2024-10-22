# crypt_utils.py
from cryptography.fernet import Fernet
import os

def generate_key():
    """Generates a new Fernet key and saves it to a file."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Loads the Fernet key from a file, generates a new one if the file doesn't exist."""
    if not os.path.exists("secret.key"):
        print("Key file not found. Generating a new key...")
        return generate_key()  # Generate and return the new key
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """Encrypts the given message using the loaded key."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message):
    """Decrypts the given encrypted message using the loaded key."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()
