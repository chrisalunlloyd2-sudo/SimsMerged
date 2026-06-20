# TIMESTAMP: 2026-05-27T19:50:00.000Z
# PROJECT_ID: SimsMerged-v1.3
# AGENT_ID: Gemini-CLI-Architect
# MANDATE: Secure genetic and economic data transfers.

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import os
import base64

class MetropolisCryptographer:
    def __init__(self):
        self.key = b'Metropolis_Genesis_Key_32_Bytes!'
        self.backend = default_backend()
        from .config import SSD_SANDBOX_PATH
        self.keys_dir = os.path.join(SSD_SANDBOX_PATH, "agent_keys")
        os.makedirs(self.keys_dir, exist_ok=True)

    def get_agent_key(self, agent_id):
        """Retrieves or generates a persistent RSA key for an agent."""
        key_path = os.path.join(self.keys_dir, f"{agent_id}.pem")
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                return serialization.load_pem_private_key(f.read(), password=None, backend=self.backend)

        # Generate new key
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=self.backend)
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        return private_key

    def sign_data(self, agent_id, data: str) -> str:
        """Signs a string using the agent's private RSA key."""
        private_key = self.get_agent_key(agent_id)
        signature = private_key.sign(
            data.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()

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
