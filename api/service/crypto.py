from cryptography.fernet import Fernet
import os
import base64
# key = Fernet.generate_key()

class CryptoService:
    def __init__(self) -> None:
        key = os.getenv('SECRET_KEY')
        self.cipher = Fernet(key)

    def encrypt(self, plaintext):
        bytearray = self.cipher.encrypt(str.encode(plaintext))
        return str(bytearray, 'utf-8')
    
    def decrypt(self, ciphertext):
        return str(self.cipher.decrypt(ciphertext), 'utf-8')