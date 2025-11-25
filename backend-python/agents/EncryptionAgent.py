# EncryptionAgent.py
# Agent responsible for handling encryption and decryption of data

from cryptography.fernet import Fernet

class EncryptionAgent:
    def __init__(self, key: bytes = None):
        self.name = "EncryptionAgent"
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
        print(f"[EncryptionAgent] Initialized with key: {self.key.decode()}")

    def encrypt(self, data: bytes) -> bytes:
        encrypted = self.cipher.encrypt(data)
        print(f"[EncryptionAgent] Data encrypted")
        return encrypted

    def decrypt(self, token: bytes) -> bytes:
        try:
            decrypted = self.cipher.decrypt(token)
            print(f"[EncryptionAgent] Data decrypted")
            return decrypted
        except Exception as e:
            print(f"[EncryptionAgent] Decryption failed: {e}")
            return b""

    async def handle_request(self, request: dict):
        action = request.get("action")
        data = request.get("data", b"")
        if action == "encrypt":
            return {"encrypted": self.encrypt(data)}
        elif action == "decrypt":
            return {"decrypted": self.decrypt(data)}
        else:
            return {"error": "Invalid action"}

    async def recover(self, error):
        print(f"[EncryptionAgent] Recovered from error: {error}")
