# TIMESTAMP: 2026-05-27T19:50:00.000Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Gemini-CLI-Architect
# MANDATE: Secure genetic and economic data transfers.

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

class MetropolisCryptographer:
    def __init__(self):
        # In a real scenario, this key would be derived from a secure vault or DePIN block
        self.key = b'Metropolis_Genesis_Key_32_Bytes!' # 32 bytes for AES-256
        self.backend = default_backend()

    def encrypt(self, plaintext: str) -> str:
        """Encrypts data using AES-256 CBC."""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        
        # Padding
        pad_len = 16 - (len(plaintext) % 16)
        padded_data = plaintext + (chr(pad_len) * pad_len)
        
        ciphertext = encryptor.update(padded_data.encode()) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext).decode()

    def decrypt(self, ciphertext_b64: str) -> str:
        """Decrypts data using AES-256 CBC."""
        data = base64.b64decode(ciphertext_b64)
        iv = data[:16]
        ciphertext = data[16:]
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        
        padded_plaintext = (decryptor.update(ciphertext) + decryptor.finalize()).decode()
        
        # Unpadding
        pad_len = ord(padded_plaintext[-1])
        return padded_plaintext[:-pad_len]

# Global instance
metropolis_vault = MetropolisCryptographer()
